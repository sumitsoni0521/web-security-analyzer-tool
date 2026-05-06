import requests
from urllib.parse import urlparse, urlencode, urlunparse, parse_qs

# Common XSS Payloads
xss_payloads = [
    "<script>alert('XSS')</script>",
    "\"><script>alert('XSS')</script>",
    "<img src=x onerror=alert('XSS')>",
    "<svg/onload=alert('XSS')>",
    "'><script>alert(1)</script>"
]

def detect_xss(url):

    try:
        response = requests.get(url)
    except:
        return False

    parsed_url = urlparse(url)
    query = parse_qs(parsed_url.query)

    # If URL has no parameters, create one
    if not query:
        query = {"q": "test"}

    for key in query:
        for payload in xss_payloads:

            test_query = query.copy()
            test_query[key] = payload

            new_query = urlencode(test_query, doseq=True)

            test_url = urlunparse((
                parsed_url.scheme,
                parsed_url.netloc,
                parsed_url.path,
                parsed_url.params,
                new_query,
                parsed_url.fragment
            ))

            try:
                test_response = requests.get(test_url, timeout=5)

                # Check if payload reflected in response
                if payload.lower() in test_response.text.lower():
                    return True

            except:
                continue

    return False
