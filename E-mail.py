import smtplib
from email.mime.text import MIMEText

def send_spoofed_email(to_address, from_address, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_address
    msg['To'] = to_address

    with smtplib.SMTP('smtp.example.com', 587) as server:
        server.starttls()
        server.login('your_email@example.com', 'your_password')
        server.sendmail(from_address, [to_address], msg.as_string())

to_address = 'recipient@example.com'
from_address = 'spoofed@example.com'
subject = 'Test Email'
body = 'This is a spoofed email.'
send_spoofed_email(to_address, from_address, subject, body)
print('Spoofed email sent')
