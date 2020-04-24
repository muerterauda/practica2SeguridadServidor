import hashlib
import json

from cryptography.hazmat.primitives import hashes, hmac

from utils.backend import backend


def generar_hash(valor, tipo=None, datos_adicionales=None):
    if tipo == "128":
        h = hashlib.shake_128()
    else:
        h = hashlib.sha256()
    if type(valor) is not bytes:
        valor = valor.encode('utf-8')
    h.update(bytes(valor))
    if datos_adicionales:
        datos_adicionales = str(datos_adicionales).encode('utf-8')
        h.update(bytes(datos_adicionales))
    if tipo:
        hash = h.digest(16)
    else:
        hash = h.hexdigest()
    return hash


def generate_mac(key, message):
    h = hmac.HMAC(key, hashes.SHA256(), backend=backend)
    h.update(message.encode())
    return h.finalize()


def generate_mac_hex(key, message):
    return generate_mac(key, message).hex()


def comparar_mac(key, content_de, secreto=None):
    mac = content_de.pop('mac')
    mensaje_mac = json.dumps(content_de)
    if secreto:
        mensaje_mac = mensaje_mac + secreto
    hmac_generado = generate_mac_hex(key, mensaje_mac)
    assert mac == hmac_generado
