import socket
import fcntl
import struct
import socket
import fcntl
import struct
import ipaddress
import netifaces

def get_ip_address(ifname):
    # obtenir le nom de l'interface réseau
    interface = ifname 

    # récupérer l'adresse IP locale de l'interface réseau
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip_address = socket.inet_ntoa(fcntl.ioctl(
        sock.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', interface[:15].encode('utf-8'))
    )[20:24])

    # afficher l'adresse IP
    print("L'adresse IPv4 locale de l'interface", interface, "est :", ip_address)
    return ip_address


def get_net_cidr(interface):

    # récupérer l'adresse IP locale et le masque de sous-réseau de l'interface réseau
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip_address = socket.inet_ntoa(fcntl.ioctl(
        sock.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', interface[:15].encode('utf-8'))
    )[20:24])
    netmask = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['netmask']

    # obtenir l'adresse IP réseau et le masque de sous-réseau en notation CIDR
    ip_network = ipaddress.ip_network(ip_address+"/"+netmask, strict=False)
    network_cidr = str(ip_network)

    # afficher la notation CIDR de l'adresse IP réseau
    return network_cidr