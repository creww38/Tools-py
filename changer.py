import subprocess

def change_mac(interface, new_mac):
    subprocess.run(['ifconfig', interface, 'down'])
    subprocess.run(['ifconfig', interface, 'hw', 'ether', new_mac])
    subprocess.run(['ifconfig', interface, 'up'])

interface = 'eth0'
new_mac = '00:11:22:33:44:55'
change_mac(interface, new_mac)
print(f'Changed MAC address of {interface} to {new_mac}')
