
import json
import re
from Crypto.Hash import keccak

class ActionRecognizer:
    def __init__(self, tx_trace: list):
        self.tx_trace = tx_trace
        self.actions = {
            # "Swap(address,uint256,uint256,uint256,uint256,address)"
            "0xd78ad95fa46c994b6551d0da85fc275fe613ce37657fb8d5e3d130840159d822": "UniSwapv2.swap",
            # "Swap(address,address,int256,int256,uint160,uint128,int24)" 
            # sender, recipient, amount0, amount1, sqrtPriceX96, liquidity, tick
            "0xc42079f94a6350d7e6235f29174924f928cc2ac818eb64fed8004e115fbcca67": "UniSwapV3.swap",
            # "Transfer(address,address,uint256)" src, dst, wad
            "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef": "Transfer",

        }
        self.contract_call = ['called contract']
        self.output = []

    def parse(self):
        for item in self.tx_trace:
            # print(item)
            if(re.match(r"^LOG.*$", item['op'])):
                # print(f"pc:{item['pc']},op:{item['op']},depth:{item['depth']},stack:{item['stack']}")
                self.__parse_log(item)
                # print(self.contract_call)
            if(re.match(r".*CALL$|CALLCODE", item['op'])):
                # print(f"pc:{item['pc']},op:{item['op']},depth:{item['depth']},stack:{item['stack']},memory:{item['memory']}")
                # print(f"pc:{item['pc']},op:{item['op']},depth:{item['depth']},stack:{item['stack']}")
                self.__parse_call(item)
                # print(self.contract_call)
            if(item['op'] == "RETURN"):
                # print(f"pc:{item['pc']},op:{item['op']},depth:{item['depth']}")
                self.__parse_return(item)
                # print(self.contract_call)
        for x in self.output:
            print(x)
        return
    
    def __parse_log(self, item: dict):
        log_num = int(item['op'][-1])
        offset = item['stack'][-1]
        len = item['stack'][-2]
        topic = item['stack'][-2 - log_num:-2] # topic2,topic1,topic0

        signature = topic[-1]
        mem = self.__get_mem(item['memory'], len, offset)
        # print(item['op'], signature)

        match signature:
            # Swap
            case "0xd78ad95fa46c994b6551d0da85fc275fe613ce37657fb8d5e3d130840159d822":
                sender = topic[-2]
                recipient = topic[-3]
                [amount0In,amount1In,amount0Out,amount1Out] = [hex2dec(x) for x in mem]
                # actions are from perspective of user who make swaps
                self.output.append({"action":self.actions[signature], "contract": self.contract_call[-1],
                                    "sender": sender, "recipient": recipient,
                                    "send_amount": amount1In if amount0In == 0 else amount0In,
                                    "recv_amount": amount1Out if amount0Out == 0 else amount0Out})
            case "0xc42079f94a6350d7e6235f29174924f928cc2ac818eb64fed8004e115fbcca67":
                sender = topic[-2]
                recipient = topic[-3]
                # Note here amount0, amount1 may be negative
                [amount0, amount1, sqrtPriceX96, liquidity, tick] = [hex2dec(x,signed=True) for x in mem]
                self.output.append({"action":self.actions[signature], "contract": self.contract_call[-1],
                                    "sender":sender, "recipient": recipient,
                                   "send_amount": amount0 if amount0 > 0 else amount1,
                                    "recv_amount": -amount0 if amount0 < 0 else -amount1})

            case "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef":
                src = topic[-2]
                dst = topic[-3]
                [wad] = [hex2dec(x) for x in mem]
                self.output.append({"action": self.actions[signature], "contract": self.contract_call[-1],
                                    "src": src, "dst": dst, "amount": wad})
                
                
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

def hex2dec(hex: str, signed=False, num_bits=256) -> int:
    if(signed):
        ans = int(hex,16)
        if(ans > (1 << (num_bits - 1))):
            ans -= (1 << num_bits)
        return ans
    return int(hex,16)

# Used for test
def output_tx_from_block(txid):
    with open("./trace2.json") as f:
        data = json.load(f)

    txs = [x['result']['structLogs'] for x in data['result']]
    with open(f"./one_tx{txid}.json",'w') as f:
        json.dump({"result:":txs[txid]}, f)
        


if __name__ == "__main__":
    # with open("./trace2.json") as f:
    #     data = json.load(f)
    # txids = [x['txHash'] for x in data['result']]
    # txs = [x['result']['structLogs'] for x in data['result']]
    #
    # for i in range(0,len(txids)):
    #     print(txids[i])
    with open("./one_tx0.json") as f:
        data = json.load(f)
    txs = [data['result:']]

    for i in range(0,len(txs)):
        # print(txids[i])
        recognizer = ActionRecognizer(txs[i])
        recognizer.parse()


    # print(keccak256("Swap(address,address,int256,int256,uint160,uint128,int24)"))


