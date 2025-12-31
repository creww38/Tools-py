import socket
import struct

def dns_spoofer(domain, ip_address):
    with open('/etc/hosts', 'a') as hosts_file:
        hosts_file.write(f'{ip_address} {domain}\n')

domain = 'example.com'
ip_address = '192.168.1.100'
dns_spoofer(domain, ip_address)
print(f'Spoofed {domain} to {ip_address}')
