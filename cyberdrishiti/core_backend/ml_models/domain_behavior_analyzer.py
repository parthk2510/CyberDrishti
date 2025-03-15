import dns.resolver
import whois
from datetime import datetime


class PhishingDetector:
    """
    Analyzes a domain’s DNS records and provided traffic data to compute a threat score.
    """

    def __init__(self, domain, traffic_data=None):
        self.domain = domain
        self.traffic_data = traffic_data if traffic_data is not None else {}
        self.resolver = dns.resolver.Resolver()
        self.threat_score = 0
        self.mx_exists = False
        self.spf_exists = False
        self.dmarc_exists = False
        self.a_record_count = 0
        self.domain_age_score = 0
        self.traffic_spike = False
        self.failed_connections_ratio = 0.0
        self.unusual_geolocations = False

    def check_dns(self):
        """Checks DNS records for MX, SPF, DMARC, A records and calculates the domain age score."""
        self._check_mx()
        self._check_spf()
        self._check_dmarc()
        self._check_a_records()
        self._get_domain_age_score()

    def _check_mx(self):
        """Checks if MX records exist for the domain."""
        try:
            mx_records = self.resolver.resolve(self.domain, 'MX')
            self.mx_exists = len(mx_records) > 0
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.exception.Timeout):
            self.mx_exists = False

    def _check_spf(self):
        """Checks if an SPF record is present in the TXT records."""
        try:
            txt_records = self.resolver.resolve(self.domain, 'TXT')
            for record in txt_records:
                if 'v=spf1' in str(record):
                    self.spf_exists = True
                    break
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.exception.Timeout):
            self.spf_exists = False

    def _check_dmarc(self):
        """Checks for the presence of a DMARC record."""
        dmarc_domain = f'_dmarc.{self.domain}'
        try:
            txt_records = self.resolver.resolve(dmarc_domain, 'TXT')
            for record in txt_records:
                if 'v=DMARC1' in str(record):
                    self.dmarc_exists = True
                    break
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.exception.Timeout):
            self.dmarc_exists = False

    def _check_a_records(self):
        """Checks the number of A records for the domain."""
        try:
            a_records = self.resolver.resolve(self.domain, 'A')
            self.a_record_count = len(a_records)
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.exception.Timeout):
            self.a_record_count = 0

    def _get_domain_age_score(self):
        """Calculates a score based on the age of the domain."""
        try:
            domain_info = whois.whois(self.domain)
            creation_date = domain_info.creation_date
            if isinstance(creation_date, list):
                creation_date = creation_date[0]
            if creation_date:
                # Convert to datetime if not already a datetime object
                if not isinstance(creation_date, datetime):
                    try:
                        creation_date = datetime.strptime(
                            str(creation_date), "%Y-%m-%d")
                    except ValueError:
                        creation_date = datetime.fromisoformat(
                            str(creation_date))
                age_days = (datetime.now() - creation_date).days
                # Domain age scoring: 3 for less than 30 days, 1 for less than a year, else 0.
                self.domain_age_score = 3 if age_days < 30 else 1 if age_days < 365 else 0
            else:
                self.domain_age_score = 0
        except Exception:
            self.domain_age_score = 0

    def analyze_traffic(self):
        """
        Analyzes traffic data:
          - Sets traffic_spike if current traffic is at least 3× the average.
          - Checks failed connection ratio and unusual geolocations.
        """
        avg = self.traffic_data.get('avg_traffic', 1)
        current = self.traffic_data.get('current_traffic', 0)
        if avg > 0 and (current / avg) >= 3:
            self.traffic_spike = True
        self.failed_connections_ratio = self.traffic_data.get(
            'failed_connections', 0)
        top_locations = self.traffic_data.get('top_locations', [])
        current_locations = self.traffic_data.get('current_locations', [])
        if top_locations and current_locations and not set(current_locations).intersection(top_locations[:3]):
            self.unusual_geolocations = True

    def calculate_threat_score(self):
        """
        Calculates the overall threat score based on:
          - Domain age score
          - Missing SPF and DMARC records
          - Excess A records
          - Traffic anomalies
        """
        self.threat_score = self.domain_age_score
        if not self.spf_exists:
            self.threat_score += 2
        if not self.dmarc_exists:
            self.threat_score += 2
        if self.a_record_count > 2:
            self.threat_score += (self.a_record_count - 2)
        if self.traffic_spike:
            self.threat_score += 2
        if self.failed_connections_ratio > 0.2:
            self.threat_score += 2
        if self.unusual_geolocations:
            self.threat_score += 1
        return self.threat_score

    def get_threat_level(self):
        """Returns 'Low', 'Medium', or 'High' based on the threat score."""
        if self.threat_score <= 4:
            return "Low"
        elif self.threat_score <= 7:
            return "Medium"
        else:
            return "High"


def main():
    """Main function to run the phishing domain analysis."""
    domain = input("Enter the domain: ")
    detector = PhishingDetector(domain)
    detector.check_dns()

    threat_score = detector.calculate_threat_score()
    threat_level = detector.get_threat_level()

    print(f"Domain: {domain}")
    print(f"Threat Score: {threat_score}")
    print(f"Threat Level: {threat_level}")


if __name__ == "__main__":
    main()
