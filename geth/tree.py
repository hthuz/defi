
class Node:
    def __init__(self,_value):
        self.children = []
        self.parent = None
        self.value = _value
    def addChild(self,child):
        self.children.append(child)
        child.parent = self
    
class Tree:
    def __init__(self, call: dict):
        self.root = self.trace_to_tree(call)

    def trace_to_tree(self, call: dict) -> Node:
        node = Node({'from':call['from'],
                    'to':call['to'],
                     'type':call['type']})

        if 'calls' in call.keys():
            for subcall in call['calls']:
                child = self.trace_to_tree(subcall)
                node.addChild(child)

        if 'logs' in call.keys():
            for log in call['logs']:
                node.addChild(Node({'addr': log['address'],
                                    'topics': log['topics'],
                                    'data': log['data'],
                                    'type': 'EVENT'}))
        return node
    def print_tree(self):
        _print_tree(self.root,[True]*(10),0)


def test_tree():
    root = Node(0)
    root.addChild(Node(1))
    root.addChild(Node(2))
    root.addChild(Node(3))
    root.children[0].addChild(Node(4))
    root.children[0].addChild(Node(5))
    root.children[1].addChild(Node(11))
    root.children[2].addChild(Node(6))
    root.children[2].addChild(Node(7))
    root.children[2].addChild(Node(8))
    root.children[2].children[1].addChild(Node(9))
    root.children[2].children[1].addChild(Node(10))

    _print_tree(root,[True]*(10),0)

def _print_tree(node: Node,exploring: list, depth: int):
    if(node == None):
        return
    for i in range(depth):
        if(i == depth - 1):
            # print(f"+---",end="")
            print(f"{depth}---",end="")
        elif exploring[i]:
            print("|   ",end="")
        else:
            print("    ",end="")
    # print(node.value['type'], node.value['from'][0:5], "->", node.value['to'][0:5])
    print(node.value['type'])
    for child in node.children:
        exploring[depth] = True;
        # visiting last children
        if(child == node.children[-1]):
            exploring[depth] = False;
        _print_tree(child, exploring, depth + 1)

if __name__ == "__main__":
    test_tree()
        

