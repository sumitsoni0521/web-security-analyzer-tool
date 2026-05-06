import dns.resolver


# Common subdomain wordlist
subdomain_list = [
    "www",
    "mail",
    "ftp",
    "localhost",
    "webmail",
    "smtp",
    "blog",
    "test",
    "dev",
    "admin",
    "portal",
    "api",
    "beta",
    "ns1",
    "ns2",
    "secure",
    "server",
    "vpn",
    "m",
    "shop"
]

def scan_subdomains(domain):

    discovered = []

    resolver = dns.resolver.Resolver()
    resolver.timeout = 2
    resolver.lifetime = 2

    for sub in subdomain_list:

        subdomain = sub + "." + domain

        try:
            resolver.resolve(subdomain, "A")
            discovered.append(subdomain)

        except dns.resolver.NXDOMAIN:
            continue
        except dns.resolver.NoAnswer:
            continue
        except dns.resolver.Timeout:
            continue
        except dns.resolver.NoNameservers:
            continue
        except:
            continue

    return discovered
