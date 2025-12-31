from twilio.rest import Client
import random

# Twilio account SID dan auth token dari console Twilio Anda
account_sid = 'your_account_sid'
auth_token = 'your_auth_token'
client = Client(account_sid, auth_token)

# Nomor pengirim WhatsApp dalam format E.164
whats_app_from = 'whatsapp:+14155238886'

# Daftar nomor telepon pengirim dalam format E.164
penerima = [
    'whatsapp:+1234567890',
    'whatsapp:+0987654321',
    # Tambahkan penerima lainnya di sini
]

# Fungsi untuk membuat OTP acak 6 digit
def buat_otp():
    return str(random.randint(100000, 999999))

# Fungsi untuk mengirim OTP melalui WhatsApp
def kirim_otp(phone_number, otp):
    pesan = client.messages.create(
        from_=whats_app_from,
        body=f'OTP Anda adalah {otp}.',
        to=phone_number
    )
    print(f'Pesan dikirim ke {phone_number}: {pesan.sid}')

# Buat dan kirim OTP kepada semua penerima
for penerima in penerima:
    otp = buat_otp()
    kirim_otp(penerima, otp)
