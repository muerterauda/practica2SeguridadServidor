from cryptography.hazmat.primitives.ciphers import Cipher, algorithms
from cryptography.hazmat.backends import default_backend
import os
import shutil

path = '.'
path_secure = './secure/'
path_unsecure = './unsecure/'

shutil.rmtree(path_secure, ignore_errors=True)
shutil.rmtree(path_unsecure, ignore_errors=True)
os.mkdir(path_secure)
os.mkdir(path_unsecure)

files = []
for r, d, f in os.walk(path):
    for file in f:
        if '.txt' in file:
            files.append(os.path.join(r, file))

for f in files:
    print(f)

chunk_size = 256

nonce = bytes("0123456789012345", 'utf-8')
key = bytes("01234567890123456789012345678901", 'utf-8')

algorithm = algorithms.ChaCha20(key, nonce)
cipher = Cipher(algorithm, mode=None, backend=default_backend())
encryptor = cipher.encryptor()

file_to_put = "ejemplo.txt"
with open(file_to_put, "rb") as source, open(path_secure + file_to_put, "wb+") as sink:
    byte = source.read(chunk_size)
    while byte:
        sink.write(encryptor.update(byte))
        byte = source.read(chunk_size)
    source.close()
    sink.close()

decryptor = cipher.decryptor()

file_to_get = "ejemplo.txt"
with open(path_secure + file_to_get, "rb") as source, open(path_unsecure + file_to_get, "wb+") as sink:
    byte = source.read(chunk_size)
    while byte:
        sink.write(decryptor.update(byte))
        byte = source.read(chunk_size)
    source.close()
    sink.close()
