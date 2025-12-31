import requests
from bs4 import BeautifulSoup

def scrape_webpage(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup.prettify()

url = 'https://example.com'
page_content = scrape_webpage(url)
print(page_content)
