
import requests
from bs4 import BeautifulSoup

def scrape():
    r = requests.get('https://eigenphi.io/mev/ethereum/tx/0x8512471989804b5c11bfcd2052b2fa16db2bf2af9dd149ffa306a9dacbcb7e20')
    soup = BeautifulSoup(r.content, 'html.parser')
    title = soup.find('title')
    print(title)
    print(title.string)


if __name__ == "__main__":
    scrape()


