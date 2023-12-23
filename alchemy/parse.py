
import json

def get_tx():
    with open("./c0ffeebabe_tx.json") as f:
        data = json.load(f)
    tx = data['result']['transfers']
    txid = [x['hash'] for x in tx]
    print(len(txid))

    with open("./tx_list.json",'w') as out_f:
        json.dump({"tx":txid}, out_f)
    # print(txid)

if __name__ == "__main__":
    get_tx()


