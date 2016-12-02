from bitstring import Bits, BitArray, BitStream, BitString
import sys
import random
import hashlib

# НОД
def gsd(a, b):
    while b:
        a, b = b, a % b
    return a


# НОД(a,b)=1
def are_coprime(a, b):
    return gsd(a, b) == 1


def are_mod_comparable(a, b, n):
    return a % n == b

def is_prime(n):
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n and n % d != 0:
        d += 2
    return d * d > n

if __name__ == "__main__":
    #print(hashlib.algorithms_available)
    msg = "Hello World"
    hash_obj = hashlib.md5(msg.encode())
    print(hash_obj.digest())
    bs = BitString(bytes=hash_obj.digest())
    print(bs.bin)