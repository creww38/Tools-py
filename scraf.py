import requests
from bs4 import BeautifulSoup

def scrape_contact_info(profile_url):
    response = requests.get(profile_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # Ekstrak info yang Anda butuhkan, misal nama, lokasi, dll.
        name = soup.find('span', {'class': 'name'}).text if soup.find('span', {'class': 'name'}) else 'N/A'
        location = soup.find('span', {'class': 'location'}).text if soup.find('span', {'class': 'location'}) else 'N/A'
        return {
            'name': name,
            'location': location
        }
    else:
        return None

# Contoh penggunaan
profile_url = 'https://example.com/profile/1234567890'  # Ganti dengan URL profil media sosial yang ingin Anda scrape
info = scrape_contact_info(profile_url)
if info:
    print(f'Informasi kontak: {info}')
else:
    print('Tidak dapat mendapatkan informasi kontak.')
