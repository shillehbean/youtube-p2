import requests
from bs4 import BeautifulSoup

# Sub in your Pi IP address
proxies = {
    'http': 'http://<IP ADDRESS of PI>:3128',
    'https': 'http://<IP ADDRESS of PI>:3128',
}

url = 'https://www.ebay.com/sch/i.html?_nkw=laptops'

response = requests.get(url, proxies=proxies)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    print(soup)
else:
    print(f'Failed to retrieve the webpage: Status code {response.status_code}')
