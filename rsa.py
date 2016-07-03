#!/usr/bin/env python
#RSA Encryption
##Import(s) #

import sys, random,pickle

def print_usage(command=''):
    if command == 'init':
        print 'init <key_filename> <prime_length>'
    elif command == 'encrypt':
        print 'encrypt <keys_filename> <plaintext_filename> <ciphertext_filename>'
    elif command == 'decrypt':
        print 'decrypt <keys_filename> <ciphertext_filename> <decrypted_filename>'
    else:
        
        print 'Usage:'
        print '\tinit -rsa setup -> takes keys_filename and prime_length as inputs'
        print '\tencrypt -> takes keys_filename, plaintext_filename, and ciphertext_filename as inputs'
        print '\tdecrypt -> takes keys_filename, ciphertext_filename,  and decrypted_filename as inputs'

def miller_rabin_test(a, s, d, n):
    atop = pow(a, d, n)
    if atop == 1:
        return True
    for i in xrange(s -1 ):
        if atop == n-1:
            return True
        atop = (atop * atop ) % n
    return atop == n -1

def miller_rabin(n, confidence):
    d = n - 1
    s = 0
    while d % 2 == 0:
        d >> 1
        s += 1
    for i in range(confidence):
        a = 0
        while a == 0:
            a = random.randchange(n)
        if not miller_rabin_test(a, s, d, n):
            return False
    return True

def euclid_gcd(a,b):
    if a < b:
        a, b = b, a
    while b != 0:
        a, b = b, a % b
    return a

def ext_euclid(a, b):
    if b == 0:
        return 1, 0, a
    else:
        x, y,gcd = ext_euclid(b, a % b)
        return y, x - y *(a // b), gcd
def inverse_mod(a, m):
    x, y, gcd = ext_euclid(a, m)
    if gcd == 1:
        return x %  m
    else:
        return None

class RSAKey(object):
    meta = dict()
    primality_confidence = 20
    
    def gen_keys(self, filename, nbits):
        #generate p (nbits-bit prime)
        while 1:
            p = random.getrandbits(nbits)
            if miller_rabin(p, self.primality_confidence):
                self.meta.update({'p':p})
                break
        #generate q (nbits-bit, prime)
        while 1:
            q = random.getrandbits(nbits)
            if miller_rabin(q, self.primality_confidence):
                self.meta.update({'q': q})
                break
        #compute modulus: (p * q)
        modulus = long(self.meta['p'] * self.meta['q'])
        self.meta.update({'modulus': modulus})
        
        #computer phi: (( p - 1 ) ( q -1))
        phi = long((self.meta['p'] - 1) * (self.meta['q'] -1))
        self.meta.update({'phi':phi})
        #choose e s.t 1< e < phi and euclid_gcd(e, phi) = 1
        while 1:
            while 1:
                e = random.randrange(phi)
                if e == 0: continue
                if euclid_gcd(e, phi) == 1:
                    self.meta.update({'e':e})
                    self.meta.update({'pub_key' : (modulus, e)})
                    break
            #compute d:
            d = long(inverse_mod(long(self.meta['e']), phi))
            if d is None: continue
            else:
                self.meta.update({'d':d})
                self.meta.update({'priv_key': (modulus, d)})
                break
        self.dump(filename)
        
    def encrypt(self, keys_fn, plaintext_fn, ciphertext_fn):
        self.load(keys_fn)
        plaintext_handle = open(plaintext_fn, 'r')
        plaintext = plaintext_handle.read()
        plaintext_handle.close()
        pub_key = self.meta['pub_key']
        ciphertext = ''
        for char in plaintext:
            ciphertext += str(pow(ord(char), pub_key[1], pub_key[0])) + '\n'
        ciphertext_handle = open(ciphertext_fn, 'r')
        ciphertext = ciphertext_handle.read().split()
        priv_key = self.meta['priv_key']
        decrypted = ''
        for chunk in ciphertext:
            decrypted += chr(pow(long(chunk), priv_key[1], priv_key[0]))
        decrypted_hanlde = open(decrypted_fn, 'w')
        decrypted_handle.write(decrypted)
        decrypted_handle 
