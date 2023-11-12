
import sqlite3
import pandas as pd

class Contract:
    def __init__(self, name ,repo, field, homepage, whitepaper):
        self.name = name;
        self.repo = repo;
        self.field = field;
        self.homepage = homepage;
        self.whitepaper = whitepaper;

map = {
    "UniswapConnector03": Contract("UniswapConnector03","asdfasdf",None,None,None)
}


def get_info():
    con = sqlite3.connect('./defi_sok.db')
    df = pd.read_sql_query("SELECT contract_name FROM VulnerableContract", con)
    con.close()

    (rows,cols) = df.shape
    df.insert(cols,"repo",[None] * rows)
    df.insert(cols + 1, "field", [None] * rows)
    df.insert(cols + 2, "homepage", [None] * rows)
    df.insert(cols + 3, "whitepaper", [None] * rows)

    for i in range(rows):
        contract = df.loc[i,'contract_name']
        if(contract in map.keys()):
            print(contract)
            print(map[contract].repo)
            df.loc[i,'repo'] = map[contract].repo
            df.loc[i,'field'] = map[contract].field
            df.loc[i,'homepage'] = map[contract].homepage
            df.loc[i,'whitepaper'] = map[contract].whitepaper
    # df.to_csv('defi.csv')

if __name__ == "__main__":
    get_info()

