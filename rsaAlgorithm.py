# rsa.py - demo of the RSA algorithm
import math, random
encryptedList = []

def main():
    n = e = d = 0
    while 1:
        print("""
    1. Set Public Key 
    2. Encrypt
    3. Decrypt
    0. Quit
    Your choice? """, end = "")
        choice = int(input())
        if not choice:
            return
        if choice == 1:
            n, e, d = set_keys()
        if choice == 2:
            encrypt(n, e)
        if choice == 3:
            decrypt(d, n)

def set_keys():
    """This fuction asks for 2 primes. 
    It sets a public key and an encoding number, 'e'."""
    print("\n\nmust be 11 or greater p and q cannot be the same.")
    p = int(input("p: "))
    q = int(input("q: "))
    n = p * q
    mod = (p - 1) * (q - 1)
    e = get_e(mod)
    d = get_d(e, mod)
    while d < 0:
        d += mod
    print("N = ", n,"\nO(",n,")","=",mod,"\ne = ", e)
    return [n, e, d]

def get_e(mod):
    """Finds an e coprime with m."""
    e = random.randint(1, mod)
    
    while gcd(e, mod) != 1:
        e += 1
    return e

def gcd(a,b):
    """Takes two integers and returns gcd."""
    while b > 0:
        a, b = b, a % b
    return a

def get_d(e, m):
    """Takes encoding number, 'e' and the value for 'mod' (p-1) * (q-1).
    Returns a decoding number."""
    x = lasty = 0 
    lastx = y = 1
    while m != 0: 
        q = e // m 
        e, m = m, e % m 
        x, lastx = lastx - q*x, x
        y, lasty = lasty - q*y, y
    return lastx

def encrypt(n, e):
    """This function asks for a message and encodes it using 'n' and 'e'."""
    s = input("Message to encrypt: ")
    r = [ord(c) for c in s]

    for i in r:
        print(pow(i, e, n), end="")
        encryptedList.append(pow(i, e, n))
    if not s:
        return

def decrypt(d, n):
    """This function asks for a number and decodes it using 'd' and 'n'."""

    if not encryptedList:
        return
    else:
        for i in encryptedList:
            r = pow(i, d, n)
            print(chr(r), end="")


if __name__ == "__main__":
    main()
