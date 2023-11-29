
import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_txn():
    fields = ['Txhash']
    df = pd.read_csv('../etherscan/c0ffeebabe.csv', usecols=fields)
    return df.Txhash
    print(list(df.Txhash))


def scrape():
    maps = {}
    txns = get_txn()
    # txns = ['0xf0a5d6618673d9944dfbe302725f08d224738120b257a3e8c301dbe6d304d2e5']
    for txn in txns:
        r = requests.get(f"https://eigenphi.io/mev/ethereum/tx/{txn}")
        soup = BeautifulSoup(r.content, 'html.parser')
        title = soup.find('title')
        mev_type = title.string.split(' ')[0]
        print(txn, mev_type)
        maps[txn] = mev_type

    # save as a table
    df = pd.DataFrame(maps.items(), columns=['Txhash','Type'])
    df.to_csv('./mev_type.csv')

if __name__ == "__main__":
    # get_txn()
    scrape()


