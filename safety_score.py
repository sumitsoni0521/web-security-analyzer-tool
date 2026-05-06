def calculate_score(ports, headers, ssl_status, sql_vuln, xss_vuln):

    score = 100

    # Deduct score for open ports
    if len(ports) >= 1 and len(ports) <= 2:
        score -= 10
    elif len(ports) > 2:
        score -= 20

    # Deduct score if SSL not enabled
    if not ssl_status:
        score -= 25

    # Deduct score for missing security headers
    missing_headers = [h for h, v in headers.items() if not v]

    if len(missing_headers) == 1:
        score -= 5
    elif len(missing_headers) == 2:
        score -= 10
    elif len(missing_headers) >= 3:
        score -= 15

    # Deduct score if SQL Injection vulnerability found
    if sql_vuln:
        score -= 25

    # Deduct score if XSS vulnerability found
    if xss_vuln:
        score -= 25

    # Ensure score doesn't go below 0
    if score < 0:
        score = 0

    return score
