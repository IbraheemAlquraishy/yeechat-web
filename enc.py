from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt
from Crypto import Random
import rsa

def createkey(passphrase):
    salt = b'salt' # this will be changed when the app is deployed
    key = scrypt(passphrase.encode(), salt, key_len=32, N=16384, r=8, p=1)
    return key

def encry(key, message):
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(message)
    return ciphertext, cipher.nonce, tag

def decry(key, ciphertext, nonce, tag):
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    return plaintext

def createsessionkey():
    key = Random.get_random_bytes(32)
    return key

def creatersakey():
    publickey,privatekey=rsa.newkeys(2048)
    pub=publickey.save_pkcs1("PEM")
    pri=privatekey.save_pkcs1("PEM")
    return pri,pub

def encrsa(publickey, message):
    pub=rsa.PublicKey.load_pkcs1(publickey)
    e=rsa.encrypt(message, pub)
    return e

def decrsa(privatekey, message):
    pri=rsa.PrivateKey._load_pkcs1_pem(privatekey)
    e=rsa.decrypt(message, pri)
    return e

