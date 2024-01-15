
import sys
from Crypto.Hash import keccak

def keccak256(signature: str) -> str:
    k = keccak.new(digest_bits=256)
    k.update(signature.encode('ASCII'))
    return k.hexdigest()

if len(sys.argv) != 2:
    print("python keccak256.py signature")
    exit(1)
print(keccak256(sys.argv[1]))
