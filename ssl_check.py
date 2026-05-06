import ssl
import socket
from datetime import datetime

def check_ssl(hostname):

    context = ssl.create_default_context()

    ssl_info = {
        "status": False,
        "issuer": None,
        "expiry_date": None,
        "days_remaining": None
    }

    try:
        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:

                cert = ssock.getpeercert()

                ssl_info["status"] = True

                issuer = dict(x[0] for x in cert['issuer'])
                ssl_info["issuer"] = issuer.get('organizationName')

                expiry = cert['notAfter']
                expiry_date = datetime.strptime(expiry, '%b %d %H:%M:%S %Y %Z')
                ssl_info["expiry_date"] = expiry_date.strftime('%Y-%m-%d')

                days_remaining = (expiry_date - datetime.now()).days
                ssl_info["days_remaining"] = days_remaining

    except:
        pass

    return ssl_info
