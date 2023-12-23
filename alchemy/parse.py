
import json

def get_tx():
    with open("./c0ffeebabe_tx.json") as f:
        data = json.load(f)
    tx = data['result']['transfers']
    txid = [x['hash'] for x in tx]
    print(len(txid))
    print(txid[0])
    # print(txid)

if __name__ == "__main__":
    get_tx()


