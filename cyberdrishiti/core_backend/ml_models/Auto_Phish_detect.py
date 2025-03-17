import re
import sqlite3
from itertools import product
from datetime import datetime
from typing import Set, List, Dict, Optional

# Constants
HOMOGLYPH_MAP = {
    'a': ['а', 'ɑ', 'ɒ', 'à', 'á', 'â', 'ã', 'ä', 'å'],
    'b': ['Ь', 'ʙ', 'ƅ'],
    'c': ['ϲ', 'с', 'ƈ', 'ç', 'ć', 'č'],
    'd': ['ԁ', 'ɗ', 'đ', 'ď'],
    'e': ['е', 'є', 'é', 'ê', 'ë', 'ē', 'ė', 'ę'],
    'f': ['ғ', 'ꜰ', 'ƒ'],
    'g': ['ɡ', 'ɢ', 'ğ', 'ģ', 'ĝ'],
    'h': ['һ', 'հ', 'ĥ'],
    'i': ['і', 'ɪ', 'ɩ', 'í', 'ì', 'î', 'ï'],
    'j': ['ϳ', 'ʝ', 'ĵ'],
    'k': ['κ', 'ᴋ', 'ķ'],
    'l': ['ⅼ', 'ʟ', 'ḷ', 'ł', 'ľ', 'ĺ'],
    'm': ['м', 'ᴍ', 'ṃ'],
    'n': ['п', 'ɴ', 'ń', 'ň', 'ñ'],
    'o': ['о', 'ᴏ', 'օ', 'ó', 'ò', 'ô', 'õ', 'ö', 'ø'],
    'p': ['р', 'ᴘ', 'ƥ', 'þ'],
    'q': ['զ', 'Ɋ', 'ʠ'],
    'r': ['г', 'ʀ', 'ŕ', 'ř'],
    's': ['ѕ', 'ꜱ', 'ś', 'š', 'ş'],
    't': ['т', 'ᴛ', 'ţ', 'ť'],
    'u': ['υ', 'ᴜ', 'ú', 'ù', 'û', 'ü'],
    'v': ['ѵ', 'ᴠ', 'ʋ'],
    'w': ['ѡ', 'ᴡ', 'ŵ'],
    'x': ['х', 'х', 'ẋ', '×'],
    'y': ['у', 'ʏ', 'ý', 'ÿ', 'ŷ'],
    'z': ['ᴢ', 'ʐ', 'ź', 'ž', 'ż'],
    '1': ['l', 'i', 'ɪ', 'Ꭵ'],
    '0': ['o', 'O', 'Ο', 'О'],
}

SUSPICIOUS_TLDS = ['ru', 'top', 'biz', 'cc',
                   'xyz', 'tk', 'ml', 'ga', 'cf', 'gq']


def generate_typosquatting_domains(domain: str) -> Set[str]:
    """Generates typosquatting variations of a domain."""
    variations = set()
    n = len(domain)
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789-'

    # Insertion
    for i in range(n + 1):
        for char in chars:
            variations.add(domain[:i] + char + domain[i:])

    # Deletion
    for i in range(n):
        variations.add(domain[:i] + domain[i+1:])

    # Substitution
    for i in range(n):
        original_char = domain[i]
        for char in chars:
            if char != original_char:
                variations.add(domain[:i] + char + domain[i+1:])

    # Transposition
    for i in range(n - 1):
        if domain[i] != domain[i+1]:
            variations.add(domain[:i] + domain[i+1] + domain[i] + domain[i+2:])

    return variations


def generate_homoglyph_domains(domain: str, homoglyph_map: Dict[str, List[str]]) -> Set[str]:
    """Generates homoglyph variations of a domain."""
    variations = {domain}
    for i, char in enumerate(domain):
        if char in homoglyph_map:
            for replacement in homoglyph_map[char]:
                new_domain = domain[:i] + replacement + domain[i+1:]
                variations.add(new_domain)
    return variations


def detect_subdomain_spoofing(domain: str, trusted_domains: List[str]) -> bool:
    """Detects subdomain spoofing attempts."""
    parts = domain.split('.')
    main_domain = '.'.join(parts[-2:]) if len(parts) >= 2 else domain

    # Check if main domain is trusted but different
    if main_domain in trusted_domains:
        return False  # It's the actual trusted domain

    # Check subdomain parts for trusted domains
    for part in parts[:-2]:  # Exclude main domain parts
        if part in trusted_domains:
            return True
        # Check for hyphen-separated subparts
        for subpart in part.split('-'):
            if subpart in trusted_domains:
                return True

    return False


def analyze_domain(
    domain: str,
    trusted_domains: List[str],
    known_suspicious_domains: Optional[List[str]] = None
) -> Dict:
    """Analyzes a domain for phishing indicators."""
    report = {
        "domain": domain,
        "is_suspicious": False,
        "reasons": []
    }

    # Typosquatting and Homoglyph checks
    for trusted in trusted_domains:
        # Typosquatting
        typosquat_vars = generate_typosquatting_domains(trusted)
        if domain in typosquat_vars and domain != trusted:
            report["is_suspicious"] = True
            report["reasons"].append(f"Typosquatting of '{trusted}'")

        # Homoglyph
        homoglyph_vars = generate_homoglyph_domains(trusted, HOMOGLYPH_MAP)
        if domain in homoglyph_vars and domain != trusted:
            report["is_suspicious"] = True
            report["reasons"].append(f"Homoglyph attack mimicking '{trusted}'")

    # Subdomain Spoofing
    if detect_subdomain_spoofing(domain, trusted_domains):
        report["is_suspicious"] = True
        report["reasons"].append("Subdomain spoofing detected")

    # Bulk Registration Check
    if known_suspicious_domains and domain in known_suspicious_domains:
        report["is_suspicious"] = True
        report["reasons"].append("Listed in known suspicious domains")

    # TLD Analysis
    domain_parts = domain.split('.')
    if len(domain_parts) >= 2:
        tld = domain_parts[-1]
        if tld in SUSPICIOUS_TLDS:
            base_domain = '.'.join(domain_parts[:-1])
            # Check if base resembles any trusted domain
            for trusted in trusted_domains:
                trusted_base = trusted.split('.')[0]
                if trusted_base in base_domain and tld not in trusted:
                    report["is_suspicious"] = True
                    report["reasons"].append(
                        f"Suspicious TLD '{tld}' for '{trusted_base}'")
                    break

    return report


def save_to_db(results: List[Dict], db_name: str = "phishing_analysis.db"):
    """Saves analysis results to SQLite database."""
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    # Create table if not exists. Using TEXT for timestamp (ISO 8601 format)
    c.execute('''CREATE TABLE IF NOT EXISTS analysis_results
                 (id INTEGER PRIMARY KEY,
                  domain TEXT,
                  is_suspicious BOOLEAN,
                  reasons TEXT,
                  timestamp TEXT)''')

    # Insert data
    for result in results:
        c.execute('''INSERT INTO analysis_results 
                     (domain, is_suspicious, reasons, timestamp)
                     VALUES (?, ?, ?, ?)''',
                  (result["domain"],
                   result["is_suspicious"],
                   ', '.join(result["reasons"]),
                   datetime.now().isoformat()))
    conn.commit()
    conn.close()


def main():
    # Internal trusted domains remain hardcoded
    TRUSTED_DOMAINS = [
        "google.com",
        "microsoft.com",
        "amazon.com",
        "apple.com",
        "cloudflare.com",
        "paypal.com",
        "bankofamerica.com",
        "chase.com",
        "wellsfargo.com",
        "citibank.com",
        "visa.com",
        "mastercard.com",
        "americanexpress.com",
        "nytimes.com",
        "bbc.com",
        "reuters.com",
        "ap.org",
        "usa.gov",
        "gov.uk",
        "canada.ca",
        "europa.eu",
        "harvard.edu",
        "mit.edu",
        "ox.ac.uk",
        "cam.ac.uk",
        "stanford.edu",
        "ieee.org",
        "w3.org",
        "ietf.org",
        "mozilla.org",
        "github.com",
        "gitlab.com",
        "wikipedia.org",
        "who.int",
        "redcross.org",
        "un.org",
        "nasa.gov",
        "weather.gov",
        "cdc.gov",
        "nih.gov",
        "fbi.gov",
        "cisa.gov",
        "dhs.gov",
        "sec.gov",
        "irs.gov",
        "justice.gov",
        "state.gov",
        "treasury.gov",
        "commerce.gov",
        "energy.gov",
        "defense.gov",
        "education.gov",
        "health.gov",
        "hhs.gov",
        "hud.gov",
        "doi.gov",
        "dol.gov",
        "dot.gov",
        "usda.gov",
        "va.gov",
        "census.gov",
        "nist.gov",
        "nsf.gov",
        "nps.gov",
        "gsa.gov",
        "sba.gov",
        "socialsecurity.gov",
        "uspto.gov",
        "usps.com",
        "fedex.com",
        "ups.com",
        "dhl.com",
        "bmw.com",
        "mercedes-benz.com",
        "toyota.com",
        "honda.com",
        "ford.com",
        "volkswagen.com",
        "siemens.com",
        "ge.com",
        "ibm.com",
        "intel.com",
        "oracle.com",
        "sap.com",
        "cisco.com",
        "adobe.com",
        "salesforce.com",
        "zoom.us",
        "slack.com",
        "reddit.com",
        "linkedin.com",
        "twitter.com",
        "instagram.com",
        "youtube.com",
        "twitch.tv",
        "discord.com",
        "airbnb.com",
        "booking.com",
        "expedia.com",
        "tripadvisor.com",
        "uber.com",
        "lyft.com",
        "spotify.com",
        "netflix.com",
        "hulu.com",
        "disneyplus.com",
        "hbomax.com",
        "vimeo.com",
        "medium.com",
        "wordpress.org",
        "drupal.org",
        "joomla.org",
        "apache.org",
        "nginx.org",
        "python.org",
        "java.com",
        "php.net",
        "ruby-lang.org",
        "rust-lang.org",
        "golang.org",
        "nodejs.org",
        "angular.io",
        "reactjs.org",
        "vuejs.org",
        "docker.com",
        "kubernetes.io",
        "aws.amazon.com",
        "azure.microsoft.com",
        "cloud.google.com",
        "digitalocean.com",
        "linode.com",
        "oracle.com",
        "salesforce.com",
        "sap.com",
        "servicenow.com",
        "shopify.com",
        "squarespace.com",
        "wix.com",
        "mailchimp.com",
        "constantcontact.com",
        "eventbrite.com",
        "meetup.com",
        "coursera.org",
        "edx.org",
        "udacity.com",
        "udemy.com",
        "khanacademy.org",
        "nationalgeographic.com",
        "smithsonianmag.com",
        "scientificamerican.com",
        "nature.com",
        "sciencemag.org",
        "cnet.com",
        "techcrunch.com",
        "wired.com",
        "pcmag.com",
        "theverge.com",
        "arsTechnica.com",
        "engadget.com",
        "bloomberg.com",
        "wsj.com",
        "ft.com",
        "economist.com",
        "forbes.com",
        "fortune.com",
        "cnbc.com",
        "foxnews.com",
        "msnbc.com",
        "npr.org",
        "pbs.org",
        "cbc.ca",
        "abc.net.au",
        "aljazeera.com",
        "dw.com",
        "france24.com",
        "nikkei.com",
        "yale.edu",
        "princeton.edu",
        "caltech.edu",
        "ethz.ch",
        "ucla.edu",
        "berkeley.edu",
        "mcgill.ca",
        "utoronto.ca",
        "kyoto-u.ac.jp",
        "tokyo.ac.jp",
        "weforum.org",
        "imf.org",
        "worldbank.org",
        "oecd.org",
        "nato.int",
        "interpol.int",
        "icrc.org",
        "amnesty.org",
        "hrw.org",
        "eff.org",
        "fsf.org",
        "opensource.org",
        "apache.org",
        "linuxfoundation.org",
        "w3c.org",
        "iso.org",
        "ansi.org",
        "itu.int",
        "iec.ch",
        "nist.gov",
        "bsigroup.com",
        "ul.com",
        "ieee.org",
        "google.com",
        "youtube.com",
        "facebook.com",
        "twitter.com",
        "linkedin.com",
        "microsoft.com",
        "apple.com",
        "icloud.com",
        "github.com",
        "gitlab.com",
        "bitbucket.org",
        "stackoverflow.com",
        "reddit.com",
        "amazon.com",
        "aws.amazon.com",
        "gmail.com",
        "yahoo.com",
        "hotmail.com",
        "outlook.com",
        "bing.com",
        "duckduckgo.com",
        "mozilla.org",
        "opera.com",
        "wordpress.org",
        "nytimes.com",
        "bbc.co.uk",
        "cnn.com",
        "theguardian.com",
        "washingtonpost.com",
        "reuters.com",
        "bloomberg.com",
        "forbes.com",
        "cnbc.com",
        "foxnews.com",
        "nbcnews.com",
        "time.com",
        "usatoday.com",
        "thehindu.com",
        "indiatimes.com",
        "aljazeera.com",
        "france24.com",
        "wikipedia.org",
        "harvard.edu",
        "mit.edu",
        "stanford.edu",
        "ox.ac.uk",
        "cam.ac.uk",
        "berkeley.edu",
        "ucla.edu",
        "umich.edu",
        "utoronto.ca",
        "nus.edu.sg",
        "purdue.edu",
        "edx.org",
        "coursera.org",
        "udemy.com",
        "khanacademy.org",
        "usa.gov",
        "whitehouse.gov",
        "senate.gov",
        "nasa.gov",
        "nps.gov",
        "europa.eu",
        "gov.uk",
        "canada.ca",
        "india.gov.in",
        "australia.gov.au",
        "gov.za",
        "gov.sg",
        "visa.com",
        "mastercard.com",
        "paypal.com",
        "stripe.com",
        "coinbase.com",
        "chase.com",
        "bankofamerica.com",
        "wellsfargo.com",
        "hsbc.com",
        "barclays.co.uk",
        "ing.com",
        "citibank.com",
        "goldmansachs.com",
        "americanexpress.com",
        "icicibank.com",
        "hdfcbank.com",
        "ebay.com",
        "etsy.com",
        "alibaba.com",
        "aliexpress.com",
        "walmart.com",
        "target.com",
        "costco.com",
        "bestbuy.com",
        "homedepot.com",
        "ikea.com",
        "macys.com",
        "dropbox.com",
        "slack.com",
        "zoom.us",
        "skype.com",
        "salesforce.com",
        "adobe.com",
        "cloudflare.com",
        "spotify.com",
        "netflix.com",
        "hulu.com",
        "disneyplus.com",
        "zoom.com",  
        "airbnb.com",
        "booking.com",
        "tripadvisor.com",
        "uber.com",
        "lyft.com",
        "tesla.com",
        "ford.com",
        "nike.com",
        "adidas.com",
        "samsung.com",
        "lg.com",
        "sony.com",
        "panasonic.com",
    ]

    print("Choose input method:")
    print("1. Enter domains manually (comma separated)")
    print("2. Provide a file path to a txt file (one domain per line)")
    choice = input("Enter 1 or 2: ").strip()

    domains = []
    if choice == '1':
        domain_input = input(
            "Enter suspicious domain(s), separated by commas: ")
        domains = [d.strip() for d in domain_input.split(',') if d.strip()]
    elif choice == '2':
        file_path = input(
            "Enter the path to the txt file containing domains: ").strip()
        try:
            with open(file_path, 'r') as f:
                domains = [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(f"Error reading file: {e}")
            return
    else:
        print("Invalid option.")
        return

    if not domains:
        print("No valid domains provided.")
        return

    # Analyze provided domains
    results = []
    print("\nAnalysis Results:")
    for domain in domains:
        try:
            analysis = analyze_domain(
                domain, TRUSTED_DOMAINS, known_suspicious_domains=[])
            results.append(analysis)
            status = "SUSPICIOUS" if analysis["is_suspicious"] else "CLEAN"
            print(f"{status}: {domain}")
            if analysis["reasons"]:
                print("   Reasons:", " | ".join(analysis["reasons"]))
        except Exception as e:
            print(f"Error analyzing {domain}: {str(e)}")

    # Save analysis results to SQLite DB (suitable for retrieval by a React dashboard)
    try:
        save_to_db(results)
        print("\nResults saved to database.")
    except Exception as e:
        print(f"Database error: {e}")


if __name__ == "__main__":
    main()
