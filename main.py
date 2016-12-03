from bitstring import Bits
import random
import numpy as np
import math


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


def primes_below(a):
    return np.array([i for i in range(2, a) if is_prime(i)])


def form_signature(prime_border):
    primes = primes_below(prime_border)
    # xi1 - prime number
    xi1 = random.choice(primes)
    # xi2 - prime number
    xi2 = random.choice(primes)
    m = xi1 * xi2
    return int(m), int(xi1), int(xi2)


def calc_alpha(m):
    # choose alpha 1 < alpha < m-1
    return random.randint(1, m)


def calc_beta(alpha, m):
    return (alpha**2) % m


def calc_bitsize(num):
    try:
        log = math.log2(num)
    except ValueError:
        log = 0
    ceil_log = math.ceil(log)
    return ceil_log+1 if ceil_log == log else ceil_log


def bits_from_uint(num):
    return Bits(uint=num, length=calc_bitsize(num))


def calc_hash(mu, num):
    bits=None
    if isinstance(mu, str):
        bits = Bits(bytes=mu.encode())
    elif isinstance(mu, Bits):
        bits = mu
    bits += bits_from_uint(num)
    ones = bits.count(1)
    return bits_from_uint(ones), ones


def gen_a(l, m):
    a = []
    while len(a) < l:
        v = random.randint(1, m)
        if are_coprime(v, m):
            a.append(v)
    return a


def find_b(a, l, m):
    b = []
    for i in range(l):
        ai_q = a[i]**2
        for x in range(m):
            if ai_q*x%m == 1:
                b.append(x)
                break
    return b


def calc_t(s, alpha, a, l, m):
    t = 1
    for i in range(l):
        if s[i]:
            t *= a[i]
    t *= alpha
    return t%m


def calc_w(t, b, s, l, m):
    w = 1
    t_squ = t**2
    for i in range(l):
        if s[i]:
            w *= b[i]
    w *= t_squ
    return w%m


if __name__ == "__main__":
    mu = "If you going to San Francisco..."

    #mu = Bits('0b1110011110001000')

    signature = form_signature(50)
    m, xi1, xi2 = signature
    alpha = calc_alpha(m)
    beta = calc_beta(alpha, m)
    print("(alpha,beta): ({},{})".format(alpha, beta))
    # h(mu, beta)
    s, s_num = calc_hash(mu=mu, num=beta)
    print("s: {},{}".format(s.bin, s_num))
    l = calc_bitsize(s_num)
    print("l: {}".format(l))
    a = gen_a(l, m)
    print("a: {}".format(a))
    t = calc_t(s=s, alpha=alpha, a=a, l=l, m=m)
    b = find_b(a=a, l=l, m=m)
    print("b: {}".format(b))
    print("(s,t): ({},{})".format(s_num, t))

    # check signature
    w = calc_w(t=t, b=b, s=s, l=l, m=m)
    print("w: {}".format(w))
    # h(mu, w)
    s1, s_num1 = calc_hash(mu=mu, num=w)
    print("s1: {}, {}".format(s1.bin, s_num1))

    if s == s1:
        print("hash function values are equal")
    else:
        print("data transfer is not reliable")
