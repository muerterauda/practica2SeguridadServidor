import os
import random
import string

from google.cloud import kms_v1

from utils.cipher.hash import generar_hash


def generar_clave_archivo(metadatos):
    metadatos = str(metadatos).join(random.choice(string.ascii_lowercase) for x in range(32))
    return generar_hash(valor=metadatos)


def generar_clave(clave_archivo, secreto, add_data):
    clave = str(clave_archivo) + str(secreto)
    return generar_hash(valor=clave, datos_adicionales=add_data)


def cifrar_clave(key):
    client = kms_v1.KeyManagementServiceClient()
    response = client.encrypt(os.environ['PROJECT_KEY_PATH'], key)
    return response.ciphertext


def descifrar_clave(ciphered_key):
    client = kms_v1.KeyManagementServiceClient()
    response = client.decrypt(os.environ['PROJECT_KEY_PATH'], ciphered_key)
    return response.plaintext
