
import json
import re
from Crypto.Hash import keccak

contract_call = [] # stack recording function/contract call

def keccak256(signature: str) -> str:
    k = keccak.new(digest_bits=256)
    k.update(signature.encode('ASCII'))
    return k.hexdigest()

actions= {
    "0xd78ad95fa46c994b6551d0da85fc275fe613ce37657fb8d5e3d130840159d822": "UniSwapv2.swap",
    # "Swap(address,uint256,uint256,uint256,uint256,address)"
    "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef": "Transfer"
    # "Transfer(address,address,uint256)"
}

def get_trace():
    # with open("./trace2.json") as f:
    #     data = json.load(f)
    #
    # txids = [x['txHash'] for x in data['result']]
    # txs = [x['result']['structLogs'] for x in data['result']]
    with open("./one_tx.json") as f:
        data = json.load(f)
    txs = [data['result:']]

    for TXID in range(0,1):
        for item in txs[TXID]:
            if(re.match(r"^LOG.*$", item['op'])):
                # print(f"pc:{item['pc']},op:{item['op']},depth:{item['depth']},stack:{item['stack']},memory:{item['memory']}")
                parse_log(item)
            if(re.match(r".*CALL$", item['op'])):
                # print(f"pc:{item['pc']},op:{item['op']},depth:{item['depth']},stack:{item['stack']},memory:{item['memory']}")
                parse_call(item)
            if(item['op'] == "RETURN"):
                parse_return(item)

def parse_log(item: dict):
    log_num = int(item['op'][-1])
    offset = item['stack'][-1]
    len = item['stack'][-2]
    topics = item['stack'][-2 - log_num:-2] # topic2,topic1,topic0

    signature = topics[-1]
    mem = get_mem(item['memory'], len, offset)
    # print(item['op'], signature)

    match signature:
        case "0xd78ad95fa46c994b6551d0da85fc275fe613ce37657fb8d5e3d130840159d822":
            sender = topics[-2]
            to = topics[-3]
            [amount0In,amount1In,amount0Out,amount1Out] = [eval('0x' + x ) for x in mem]
            print(f"action: {actions[signature]}, contract: {contract_call[-1]}, amount0In: {amount0In}, amount1Out: {amount1Out}")
        # case _:

def parse_call(item: dict):
    global contract_call
    contract = item['stack'][-2]
    contract_call.append(contract)
    # print(item['op'], contract)
    return
def parse_return(item: dict):
    global contract_call
    contract_call.pop()
    return 

def get_mem(_mem: list, _len: str, _offset: str) -> list:
    slot = 32 # bytes
    offset = eval(_offset) # bytes
    len = eval(_len) # bytes
    mem = ''.join(_mem)
    mem = mem[offset * 2: offset * 2 + len * 2]
    return [mem[i : i + slot * 2] for i in range(0, len * 2, slot * 2)]

if __name__ == "__main__":
    get_trace()

