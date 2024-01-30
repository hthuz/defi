
import json
import re
import os
from tree import Tree

class ActionRecognizer:
    def __init__(self, tx_hash: str, tx_trace: dict):
        self.tx_hash = tx_hash
        self.tx_trace = tx_trace
        self.actions = {
            # "Swap(address,uint256,uint256,uint256,uint256,address)"
            "0xd78ad95fa46c994b6551d0da85fc275fe613ce37657fb8d5e3d130840159d822": "UniSwapv2.swap",
            # "Swap(address,address,int256,int256,uint160,uint128,int24)" 
            # sender, recipient, amount0, amount1, sqrtPriceX96, liquidity, tick
            "0xc42079f94a6350d7e6235f29174924f928cc2ac818eb64fed8004e115fbcca67": "UniSwapV3.swap",
            # "Transfer(address,address,uint256)" src, dst, wad
            "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef": "Transfer"}

        self.output = []

    def parse(self):
        print(self.tx_hash)
        print(self.tx_trace.keys())
        tree = Tree(self.tx_trace)
        events = tree.events
        for event in events:
            self.__parse_event(event)

        return
    def __parse_event(self, event: dict):
        topic = event['topics']
        print(event)

        # signature = os.popen(f"cast 4byte-event {topic[0]}").read()
        # if "Error" in signature:
        #     print("No match")
        # print(signature)

        # General match
        match topic[0]:
            case "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef":
                src = topic[1]
                dst = topic[2]
                amount = hex2dec(event['data'][2:])
                self.output.append({"action": self.actions[topic[0]], "contract": event['addr'],
                                    "src": src, "dst": dst, "amount": amount})


        # Action specific match
        match topic[0]:
            # Swap, uniswapv2
            case "0xd78ad95fa46c994b6551d0da85fc275fe613ce37657fb8d5e3d130840159d822":
                sender = topic[1]
                recipient = topic[2]
                data = self.__split_data(event['data'][2:])
                [amount0In,amount1In,amount0Out,amount1Out] = [hex2dec(x) for x in data]
                # actions are from perspective of user who make swaps
                self.output.append({"action":self.actions[topic[0]], "contract": event['addr'],
                                    "sender": sender, "recipient": recipient,
                                    "poolin": amount1In if amount0In == 0 else amount0In,
                                    "poolout": amount1Out if amount0Out == 0 else amount0Out})
            # swap, uniswapv3
            case "0xc42079f94a6350d7e6235f29174924f928cc2ac818eb64fed8004e115fbcca67":
                sender = topic[1]
                recipient = topic[2]
                data = self.__split_data(event['data'][2:])
                print("DATA",data)
                # Note here amount0, amount1 may be negative
                [amount0, amount1, sqrtPriceX96, liquidity, tick] = [hex2dec(x,signed=True) for x in data]
                self.output.append({"action":self.actions[topic[0]], "contract": event['addr'],
                                    "sender":sender, "recipient": recipient,
                                    "poolin": amount0 if amount0 > 0 else amount1,
                                    "poolout": -amount0 if amount0 < 0 else -amount1})

        return
    def __split_data(self, data: str) -> list:
        slot = 32 # bytes
        length = len(data)
        print("LENGTH",length)
        return [data[i : i + slot * 2] for i in range(0, length, slot * 2)]
                


# hex: hex string without 0x
def hex2dec(hex: str, signed=False, num_bits=256) -> int:
    if(signed):
        ans = int(hex,16)
        if(ans > (1 << (num_bits - 1))):
            ans -= (1 << num_bits)
        return ans
    return int(hex,16)


if __name__ == "__main__":
    with open("./trace3.json") as f:
        data = json.load(f)['result']


    recognizer = ActionRecognizer(data[0]['txHash'], data[0]['result'])
    recognizer.parse()


