
import json
import re
from Crypto.Hash import keccak

class ActionRecognizer:
    def __init__(self, tx_trace: list):
        self.tx_trace = tx_trace
        self.actions= {
            "0xd78ad95fa46c994b6551d0da85fc275fe613ce37657fb8d5e3d130840159d822": "UniSwapv2.swap",
            # "Swap(address,uint256,uint256,uint256,uint256,address)"
            "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef": "Transfer"
            # "Transfer(address,address,uint256)"
        }
        self.contract_call = []

    def parse(self):
        for item in self.tx_trace:
            if(re.match(r"^LOG.*$", item['op'])):
                # print(f"pc:{item['pc']},op:{item['op']},depth:{item['depth']},stack:{item['stack']},memory:{item['memory']}")
                self.__parse_log(item)
            if(re.match(r".*CALL$", item['op'])):
                # print(f"pc:{item['pc']},op:{item['op']},depth:{item['depth']},stack:{item['stack']},memory:{item['memory']}")
                self.__parse_call(item)
            if(item['op'] == "RETURN"):
                self.__parse_return(item)
        return
    
    def __parse_log(self, item: dict):
        log_num = int(item['op'][-1])
        offset = item['stack'][-1]
        len = item['stack'][-2]
        topics = item['stack'][-2 - log_num:-2] # topic2,topic1,topic0

        signature = topics[-1]
        mem = self.__get_mem(item['memory'], len, offset)
        # print(item['op'], signature)

        match signature:
            case "0xd78ad95fa46c994b6551d0da85fc275fe613ce37657fb8d5e3d130840159d822":
                sender = topics[-2]
                to = topics[-3]
                [amount0In,amount1In,amount0Out,amount1Out] = [eval('0x' + x ) for x in mem]
                print(f"action: {self.actions[signature]}, contract: {self.contract_call[-1]}, amount0In: {amount0In}, amount1Out: {amount1Out}")
            # case _:

    def __parse_call(self, item: dict):
        contract = item['stack'][-2]
        self.contract_call.append(contract)
        # print(item['op'], contract)
        return

    def __parse_return(self, item: dict):
        self.contract_call.pop()
        return 
    def __get_mem(self, _mem: list, _len: str, _offset: str) -> list:
        slot = 32 # bytes
        offset = eval(_offset) # bytes
        len = eval(_len) # bytes
        mem = ''.join(_mem)
        mem = mem[offset * 2: offset * 2 + len * 2]
        return [mem[i : i + slot * 2] for i in range(0, len * 2, slot * 2)]

def keccak256(signature: str) -> str:
    k = keccak.new(digest_bits=256)
    k.update(signature.encode('ASCII'))
    return k.hexdigest()


if __name__ == "__main__":
    with open("./trace2.json") as f:
        data = json.load(f)

    txids = [x['txHash'] for x in data['result']]
    txs = [x['result']['structLogs'] for x in data['result']]

    for i in range(0,len(txids)):
        print(txids[i])

    # for i in range(0,len(txs)):
    #     print(txids[i])
    #     recognizer = ActionRecognizer(txs[i])
    #     recognizer.parse()

    # with open("./one_tx.json") as f:
    #     data = json.load(f)
    # txs = data['result:']



