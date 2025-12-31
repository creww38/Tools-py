import socket
import struct
import textwrap

def sniff_packet(iface):
    sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))
    sock.bind((iface, 0))
    while True:
        packet, _ = sock.recvfrom(65535)
        parse_packet(packet)

def parse_packet(packet):
    eth_length = 14
    eth_header = packet[:eth_length]
    eth = struct.unpack('!6s6sH', eth_header)
    print(f'Eth Header - Destination: {eth[0].hex()} Source: {eth[1].hex()} Type: {eth[2]}')
    # Add more parsing logic as needed

iface = 'eth0'
sniff_packet(iface)
