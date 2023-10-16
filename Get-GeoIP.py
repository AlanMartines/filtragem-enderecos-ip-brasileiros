import requests
import ipaddress

urls = [
    "https://geoip.site/download/MaxMind/GeoIP.acl",
    "https://geoip.site/download/IP2Location/GeoIP.acl",
    "https://geoip.site/download/DB-IP/GeoIP.acl"
]

ipv4_networks = set()
ipv6_networks = set()

for url in urls:
    response = requests.get(url)
    lines = response.text.split('\n')
    in_br_block = False
    for line in lines:
        if "acl BR" in line:
            in_br_block = True
        elif "}" in line:
            in_br_block = False
        elif in_br_block:
            ip = line.strip().strip(';')
            try:
                ip_obj = ipaddress.ip_network(ip, strict=False)
                if ip_obj.version == 4:
                    ipv4_networks.add(ip_obj)
                elif ip_obj.version == 6:
                    ipv6_networks.add(ip_obj)
            except ValueError:
                pass

# Filtrar redes de maior abrangência
def filter_supernets(networks):
    filtered = set()
    for net in networks:
        if not any(net.subnet_of(supernet) for supernet in networks if net != supernet):
            filtered.add(net)
    return filtered

ipv4_networks = filter_supernets(ipv4_networks)
ipv6_networks = filter_supernets(ipv6_networks)

# Salvar as redes filtradas
with open('br_ipv4.txt', 'w') as f:
    for net in sorted(ipv4_networks):
        f.write(f"{net}\n")

with open('br_ipv6.txt', 'w') as f:
    for net in sorted(ipv6_networks):
        f.write(f"{net}\n")
