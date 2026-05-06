import socket
from urllib.parse import urlparse

from port_scanner import scan_ports
from header_check import check_headers
from ssl_check import check_ssl
from vulnerability_scan import check_sql_injection
from xss_detector import detect_xss
from subdomain_scanner import scan_subdomains
from whois_lookup import get_whois
from safety_score import calculate_score


# Function to extract hostname
def get_hostname(url):
    parsed_url = urlparse(url)
    return parsed_url.hostname


def main():

    print("\n========== Website Security Analysis Tool ==========\n")

    url = input("Enter Website URL (Example: https://example.com): ")

    try:
        hostname = get_hostname(url)

        if hostname is None:
            print("Invalid URL! Please enter a valid website.")
            return

        domain = hostname.replace("www.", "")

        # Get IP Address
        ip_address = socket.gethostbyname(hostname)

        print("\nScanning Website...\n")

        # Run Modules
        ports = scan_ports(ip_address)
        headers = check_headers(url)
        ssl_status = check_ssl(hostname)
        sql_vuln = check_sql_injection(url)
        xss_vuln = detect_xss(url)
        subdomains = scan_subdomains(domain)
        whois_info = get_whois(domain)

        # Calculate Safety Score
        score = calculate_score(ports, headers, ssl_status, sql_vuln, xss_vuln)

        # Display Report
        print("========== SECURITY REPORT ==========\n")
        print(f"Website: {url}")
        print(f"IP Address: {ip_address}")
        print(f"Open Ports: {ports}")
        print(f"Security Headers: {headers}")
        print(f"SSL Enabled: {ssl_status}")
        print(f"SQL Injection Risk: {sql_vuln}")
        print(f"XSS Risk: {xss_vuln}")
        print(f"Subdomains Found: {subdomains}")
        print(f"WHOIS Info: {whois_info}")
        print(f"\nWebsite Safety Score: {score}%")

    except Exception as e:
        print("Error Occurred:", e)


if __name__ == "__main__":
    main()
