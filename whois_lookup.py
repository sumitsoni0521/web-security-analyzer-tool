import whois

def get_whois(domain):

    try:
        info = whois.whois(domain)

        creation = info.creation_date
        expiry = info.expiration_date

        if isinstance(creation, list):
            creation = creation[0]

        if isinstance(expiry, list):
            expiry = expiry[0]

        whois_data = {
            "Domain Name": info.domain_name,
            "Registrar": info.registrar,
            "Creation Date": str(creation).split(" ")[0],
            "Expiration Date": str(expiry).split(" ")[0],
            "Country": info.country,
            "Name Servers": info.name_servers
        }

        return whois_data

    except Exception as e:
        return {"Error": str(e)}
