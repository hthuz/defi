
import json
import re

def get_trace():
    with open("./trace2.json") as f:
        data = json.load(f)

    txids = [x['txHash'] for x in data['result']]
    txs = [x['result']['structLogs'] for x in data['result']]
    TXID=1;
    print(txids[TXID])
    for item in txs[TXID]:
        # print(item.keys())
        # break
        if(re.match(r"^LOG.*$", item['op'])):
            # Show op LOG* only
            print(f"pc:{item['pc']},op:{item['op']},depth:{item['depth']},stack:{item['stack']},memory:{item['memory']}")
    print(txids[TXID])



if __name__ == "__main__":
    get_trace()

