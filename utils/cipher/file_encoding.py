from cryptography.hazmat.primitives.ciphers import Cipher, algorithms

from utils.backend import backend


def cifrar_archivo(archivo, metadatos, key):
    algorithm = algorithms.ChaCha20(key, metadatos)
    cipher = Cipher(algorithm, mode=None, backend=backend)
    encryptor = cipher.encryptor()
    return encryptor.update(archivo.read())


def descifrar_archivo(archivo_cifrado, metadatos, key):
    algorithm = algorithms.ChaCha20(key, metadatos)
    cipher = Cipher(algorithm, mode=None, backend=backend)
    encryptor = cipher.decryptor()
    return encryptor.update(archivo_cifrado.read())
