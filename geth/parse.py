
import json
import re

signatures= {
    "0xd78ad95fa46c994b6551d0da85fc275fe613ce37657fb8d5e3d130840159d822": "UniSwapv2.swap",
}

def get_trace():
    with open("./trace2.json") as f:
        data = json.load(f)

    txids = [x['txHash'] for x in data['result']]
    txs = [x['result']['structLogs'] for x in data['result']]
    TXID=1;
    for TXID in range(0,len(txs)):
        print(txids[TXID])
        for item in txs[TXID]:
            if(re.match(r"^LOG.*$", item['op'])):
                # Show op LOG* only
                # print(f"pc:{item['pc']},op:{item['op']},depth:{item['depth']},stack:{item['stack']},memory:{item['memory']}")
                parse_item(item)
    # print(txids[TXID])

def parse_item(item):
    signature = item['stack'][-3]
    if signature in signatures.keys():
        print(signatures[signature])
    


if __name__ == "__main__":
    get_trace()

