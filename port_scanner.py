import socket

# Commonly used web server ports
COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    8080: "HTTP-Proxy"
}

def scan_ports(target_ip):
    
    open_ports = []

    print("\nScanning Target:", target_ip)
    print("Please wait...\n")

    for port, service in COMMON_PORTS.items():
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            
            result = sock.connect_ex((target_ip, port))
            
            if result == 0:
                open_ports.append({
                    "port": port,
                    "service": service
                })
            
            sock.close()
        
        except socket.gaierror:
            print("Hostname could not be resolved.")
            return []
        
        except socket.error:
            print("Server not responding.")
            return []
        
        except Exception as e:
            pass

    return open_ports
