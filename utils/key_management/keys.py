import os

from google.cloud import kms_v1

from utils.cipher.hash import generar_hash


def generar_clave(secreto, metadatos):
    key = generar_hash(secreto, metadatos)
    client = kms_v1.KeyManagementServiceClient()
    response = client.encrypt(os.environ['PROJECT_KEY_PATH'], key)
    return response.ciphertext


def descifrar_clave(ciphered_key):
    client = kms_v1.KeyManagementServiceClient()
    response = client.decrypt(os.environ['PROJECT_KEY_PATH'], ciphered_key)
    return response.plaintext
