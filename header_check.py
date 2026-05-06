import requests

def check_headers(url):

    security_headers = {
        "Content-Security-Policy": "CSP",
        "Strict-Transport-Security": "HSTS",
        "X-Content-Type-Options": "NoSniff",
        "X-Frame-Options": "ClickJacking Protection",
        "X-XSS-Protection": "XSS Protection",
        "Referrer-Policy": "Referrer Policy"
    }

    header_status = {}

    try:
        response = requests.get(url, timeout=5)

        for header in security_headers:
            if header in response.headers:
                header_status[header] = True
            else:
                header_status[header] = False

    except requests.exceptions.RequestException:
        for header in security_headers:
            header_status[header] = "Error"

    return header_status
