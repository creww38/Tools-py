import requests

def download_file(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as file:
        file.write(response.content)

url = 'https://example.com/file.zip'
filename = 'downloaded_file.zip'
download_file(url, filename)
print(f'Downloaded {filename} from {url}')
