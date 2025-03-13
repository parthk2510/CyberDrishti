import ssl
import socket
import logging
from urllib.parse import urlparse
from datetime import datetime
from collections import defaultdict
import ipaddress

# Set up logging configuration
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s')


class SSLCertificateAnalyzer:
    def __init__(self):
        pass

    def analyze_certificate(self, url, tls_check=False):
        
        result = {
            'certificate_valid': False,
            'hostname_match': False,
            'tls_valid': False,
            'cert_details': {},
            'validation_score': 1.0,
            'error': None
        }

        try:
            parsed_url = self._validate_url(url)
            if not parsed_url:
                result['error'] = "Invalid URL format"
                result['validation_score'] = 0.7
                return result

            context = self._create_ssl_context()
            cert_info = self._fetch_certificate(parsed_url.hostname, context)

            if not cert_info:
                result['error'] = "No certificate retrieved"
                result['validation_score'] = 0.9
                return result

            # Process certificate details
            result['cert_details'] = self._parse_certificate_details(cert_info)
            result['hostname_match'] = self._check_hostname_match(
                parsed_url.hostname,
                result['cert_details']['subject'],
                result['cert_details']['extensions'].get('subjectAltName', [])
            )

            # TLS version check
            tls_status = self._check_tls_version(
                cert_info['tls_version'], tls_check)
            result['tls_valid'] = tls_status['valid']
            if tls_status['message']:
                result['cert_details']['tls_warning'] = tls_status['message']

            # Calculate final validation score
            result['certificate_valid'] = result['hostname_match'] and result['tls_valid']
            result['validation_score'] = self._calculate_score(
                result['hostname_match'],
                result['tls_valid'],
                result['cert_details']['validity_status']
            )

        except (socket.timeout, socket.gaierror) as e:
            result['error'] = f"Connection error: {str(e)}"
            result['validation_score'] = 0.9
        except ssl.SSLError as e:
            result['error'] = f"SSL error: {str(e)}"
            result['validation_score'] = 0.9
        except Exception as e:
            result['error'] = f"Unexpected error: {str(e)}"
            result['validation_score'] = 0.5
            logging.exception("Unexpected error occurred")

        return result

    def _validate_url(self, url):
        """Validate and parse input URL."""
        parsed = urlparse(url)
        if not parsed.scheme or parsed.scheme not in ('http', 'https'):
            parsed = urlparse(f'https://{url}')

        if not parsed.hostname:
            raise ValueError("Invalid URL or missing hostname")

        try:
            # Check if hostname is an IP address
            ipaddress.ip_address(parsed.hostname)
        except ValueError:
            # Valid domain name
            pass
        else:
            logging.warning(
                "Hostname is an IP address - certificate validation may be limited")

        return parsed

    def _create_ssl_context(self):
        """Create SSL context with modern security settings."""
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        context.options |= ssl.OP_NO_SSLv2 | ssl.OP_NO_SSLv3 | ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
        return context

    def _fetch_certificate(self, hostname, context):
        """Retrieve SSL certificate details from server."""
        try:
            with socket.create_connection((hostname, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    return {
                        'cert': ssock.getpeercert(),
                        'tls_version': ssock.version(),
                        'cipher': ssock.cipher(),
                        'issuer': ssock.getpeercert().get('issuer', []),
                        'subject': ssock.getpeercert().get('subject', []),
                        'san': self._get_subject_alt_names(ssock.getpeercert()),
                        'valid_from': ssock.getpeercert().get('notBefore'),
                        'valid_to': ssock.getpeercert().get('notAfter'),
                        'serial': ssock.getpeercert().get('serialNumber', '')
                    }
        except Exception as e:
            logging.error("Connection failed: %s", str(e))
            raise

    def _parse_certificate_details(self, cert_info):
        """Parse raw certificate information into structured format."""
        details = {
            'subject': self._parse_rdns(cert_info['subject']),
            'issuer': self._parse_rdns(cert_info['issuer']),
            'tls_version': cert_info['tls_version'],
            'cipher': cert_info['cipher'],
            'extensions': {
                'subjectAltName': cert_info['san']
            },
            'validity': self._parse_validity(
                cert_info['valid_from'],
                cert_info['valid_to']
            ),
            'serial_number': self._parse_serial(cert_info['serial'])
        }
        details['validity_status'] = self._check_validity(details['validity'])
        return details

    def _parse_rdns(self, rdns):
        """Parse certificate subject/issuer RDNs into structured format."""
        attributes = defaultdict(list)
        for rdn in rdns:
            for attr, value in rdn:
                key = attr.lower().replace(' ', '')
                attributes[key].append(value)
        return dict(attributes)

    def _get_subject_alt_names(self, cert):
        """Extract subject alternative names from certificate."""
        return [name[1] for name in cert.get('subjectAltName', ())
                if name[0].lower() == 'dns']

    def _parse_validity(self, not_before, not_after):
        """Parse certificate validity dates into datetime objects."""
        def parse_date(date_str):
            try:
                return datetime.strptime(date_str, '%b %d %H:%M:%S %Y %Z')
            except ValueError:
                return None

        return {
            'not_before': parse_date(not_before),
            'not_after': parse_date(not_after),
            'epoch': {
                'not_before': ssl.cert_time_to_seconds(not_before),
                'not_after': ssl.cert_time_to_seconds(not_after)
            }
        }

    def _parse_serial(self, serial_str):
        """Convert serial number from hex string to integer."""
        try:
            return int(serial_str.replace(':', ''), 16)
        except (ValueError, AttributeError):
            return None

    def _check_validity(self, validity):
        """Check certificate validity period."""
        now = datetime.now()
        valid_from = validity['not_before']
        valid_to = validity['not_after']

        if not valid_from or not valid_to:
            return 'invalid'

        if now < valid_from:
            return 'not_yet_valid'
        if now > valid_to:
            return 'expired'
        return 'valid'

    def _check_hostname_match(self, hostname, subject, sans):
        """Verify hostname matches certificate subject or SANs."""
        hostname = hostname.lower()
        cn_match = any(self._match_pattern(hostname, cn.lower())
                       for cn in subject.get('commonname', []))
        san_match = any(self._match_pattern(hostname, san.lower())
                        for san in sans)
        return cn_match or san_match

    def _match_pattern(self, hostname, pattern):
        """Match hostname against certificate pattern with wildcards."""
        if pattern.startswith('*.'):
            domain = pattern[2:]
            return hostname == domain or hostname.endswith('.' + domain)
        return hostname == pattern

    def _check_tls_version(self, version, tls_check_enabled):
        """Validate TLS version meets modern security standards."""
        result = {'valid': True, 'message': None}
        insecure_versions = ['SSLv2', 'SSLv3', 'TLSv1', 'TLSv1.1']

        if version in insecure_versions:
            result['valid'] = False
            result['message'] = f'Insecure protocol version: {version}'
        elif tls_check_enabled and version not in ['TLSv1.2', 'TLSv1.3']:
            result['valid'] = False
            result['message'] = f'Unapproved TLS version: {version}'

        return result

    def _calculate_score(self, host_valid, tls_valid, validity_status):
        """Calculate comprehensive validation score."""
        score = 1.0

        if not host_valid:
            score *= 0.5
        if not tls_valid:
            score *= 0.7
        if validity_status != 'valid':
            score *= 0.8

        return round(score, 2)


if __name__ == '__main__':
    analyzer = SSLCertificateAnalyzer()
    target_url = input("Enter URL to analyze: ").strip()

    analysis = analyzer.analyze_certificate(target_url, tls_check=True)

    print("\n=== SSL/TLS Analysis Report ===")
    print(f"URL: {target_url}")
    print(f"Validation Score: {analysis['validation_score']}/1.0")

    if analysis['error']:
        print(f"\nError: {analysis['error']}")
    else:
        print("\nCertificate Details:")
        print(
            f"Subject: {analysis['cert_details']['subject'].get('commonname', ['N/A'])[0]}")
        print(
            f"Issuer: {analysis['cert_details']['issuer'].get('commonname', ['N/A'])[0]}")
        print(
            f"Validity: {analysis['cert_details']['validity_status'].upper()}")
        print(f"TLS Version: {analysis['cert_details']['tls_version']}")
        print(f"Cipher Suite: {analysis['cert_details']['cipher'][0]}")

        if 'tls_warning' in analysis['cert_details']:
            print(f"\nSecurity Warnings:")
            print(f"* {analysis['cert_details']['tls_warning']}")
