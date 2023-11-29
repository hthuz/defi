
import json
import matplotlib.pyplot as plt

def get_jared():
    files = []
    items = []
    for i in range(6, 13):
        files.append(f"./jared{i}.json")
    for file in files:
        with open(file) as f:
            data = json.load(f)
            items += data['result']
    print(len(items))
    return items;
def get_coffee():
    with open("./c0ffeebabe.json") as f:
        data = json.load(f)
    items = data['result']
    print(len(items))
    return items

def aggregate(items):
    block_dict = {}
    for item in items:
        if(item['blockNumber'] not in block_dict.keys()):
            block_dict[item['blockNumber']] = [item['hash']]
            continue
        block_dict[item['blockNumber']].append(item['hash'])

    # Draw
    x = list(block_dict.keys())
    y = [len(x) for x in block_dict.values()]
    print("draw")
    fig,ax = plt.subplots()
    ax.bar(x=x,height=y)
    plt.savefig("c0ffee.png")


if __name__ == "__main__":
    items = get_coffee()
    aggregate(items)

