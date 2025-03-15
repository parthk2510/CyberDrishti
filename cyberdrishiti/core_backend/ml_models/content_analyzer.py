from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urlparse
import whois
import re
import requests


class PhishingContentAnalyzer:
    def __init__(self, url):
        self.url = url
        self.domain = urlparse(url).netloc
        self.content = None
        self.keywords = ['login', 'verify', 'account',
                         'password', 'banking', 'secure', 'update', 'confirm']
        self.threat_score = 0
        self.ssl_valid = False
        self.domain_age = 0
        self.suspicious_elements = 0

    def fetch_content(self):
        try:
            response = requests.get(self.url, timeout=10, verify=True)
            self.ssl_valid = response.ok
            if response.status_code == 200:
                self.content = response.text
                return True
            return False
        except (requests.exceptions.SSLError, requests.exceptions.ConnectionError):
            self.ssl_valid = False
            return False
        except Exception:
            return False

    def check_ssl(self):
        self.threat_score += 0 if self.ssl_valid else 5

    def check_domain_age(self):
        try:
            domain_info = whois.whois(self.domain)
            creation_date = domain_info.creation_date
            if isinstance(creation_date, list):
                creation_date = creation_date[0]
            self.domain_age = (datetime.now() - creation_date).days
            if self.domain_age < 180:
                self.threat_score += 3
        except Exception:
            self.threat_score += 3

    def analyze_content(self):
        if not self.content:
            return
        try:
            soup = BeautifulSoup(self.content, 'html.parser')
            forms = soup.find_all('form')
            hidden_inputs = soup.find_all('input', {'type': 'hidden'})
            scripts = soup.find_all(
                'script', {'src': re.compile(r'^https?://')})
            iframes = soup.find_all('iframe')

            self.suspicious_elements = len(
                hidden_inputs) + len(scripts) + len(iframes)
            self.threat_score += min(self.suspicious_elements * 0.5, 4)

            for form in forms:
                if form.find_all(['input', 'password']):
                    self.threat_score += 2

            text = soup.get_text().lower()
            for keyword in self.keywords:
                if re.search(rf'\b{keyword}\b', text):
                    self.threat_score += 1.5
        except Exception:
            pass

    def check_url_structure(self):
        parsed = urlparse(self.url)
        if re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', parsed.netloc):
            self.threat_score += 4
        if '@' in parsed.path or '//' in parsed.path:
            self.threat_score += 3
        if len(parsed.path.split('/')) > 4:
            self.threat_score += 1.5

    def calculate_threat_score(self):
        self.fetch_content()
        self.check_ssl()
        self.check_domain_age()
        self.analyze_content()
        self.check_url_structure()
        return min(self.threat_score, 20)

    def get_threat_level(self):
        score = self.calculate_threat_score()
        print(score)
        if score <= 7:
            return "Low"
        elif score <= 14:
            return "Medium"
        else:
            return "High"


def main():
    link = input("Enter the URL ")
    analyzer = PhishingContentAnalyzer(link)
    threat_level = analyzer.get_threat_level()
    print(f"Phishing Threat Level: {threat_level}")


if __name__ == "__main__":
    main()
