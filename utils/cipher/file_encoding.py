from cryptography.hazmat.primitives.ciphers import Cipher, algorithms

from utils.backend import backend
from utils.cipher.hash import generar_hash


def cifrar_archivo(archivo, metadatos, key):
    key = bytes.fromhex(key)
    metadatos = str(metadatos)
    metadatos = generar_hash(valor=metadatos, tipo="128")
    algorithm = algorithms.ChaCha20(key, metadatos)
    cipher = Cipher(algorithm, mode=None, backend=backend)
    encryptor = cipher.encryptor()
    return encryptor.update(archivo)


def descifrar_archivo(archivo_cifrado, metadatos, key):
    key = bytes.fromhex(key)
    metadatos = str(metadatos)
    metadatos = generar_hash(valor=metadatos, tipo="128")
    algorithm = algorithms.ChaCha20(key, metadatos)
    cipher = Cipher(algorithm, mode=None, backend=backend)
    encryptor = cipher.decryptor()
    return encryptor.update(archivo_cifrado)
