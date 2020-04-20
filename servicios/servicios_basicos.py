import os
import io

from flask import Blueprint, redirect, url_for, request, render_template, jsonify, send_from_directory, send_file
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from mongo.repository.usuario_repository import update_user_by_id, replace_user_by_id
from utils.cipher.file_encoding import cifrar_archivo, descifrar_archivo
from utils.key_management.keys import generar_clave, cifrar_clave

servicios_basicos_bp = Blueprint('Seguridad_servicios_basicos', __name__, template_folder='templates')


@servicios_basicos_bp.route("/establecerPasswordHTML", methods=['GET'])
@login_required
def establecer_password_html():
    user = current_user
    return render_template("establecerPassword.html", user=user)


@servicios_basicos_bp.route("/establecerPassword", methods=['POST'])
@login_required
def establecer_password():
    user = current_user
    password = request.values.get("password")
    user.set_password(password)
    value = update_user_by_id(user.id_mongo, {'password': user.password})
    return jsonify(isError=False, message="Success", statusCode=200), 200


@servicios_basicos_bp.route("/descargarArchivo", methods=['GET', 'POST'])
@login_required
def descargar_archivo():
    user = current_user
    nombre_archivo = request.values.get("nombre")
    secreto = request.values.get("secreto")
    from main import uploads_dir
    uploads_dir_user = os.path.join(uploads_dir, user.id_mongo)
    path_guardado = os.path.join(uploads_dir_user, nombre_archivo)
    cifrado = open(path_guardado, "rb").read()
    metadatos = open(path_guardado + ".metadata", "rb").read()
    metadatos = metadatos.decode()
    metadatos = float(metadatos)
    key = generar_clave(user.password, metadatos)
    valor_claro = descifrar_archivo(cifrado, metadatos, key)
    return send_file(io.BytesIO(valor_claro),
                     attachment_filename=nombre_archivo,
                     mimetype='text/plain')


@servicios_basicos_bp.route("/subirArchivo", methods=['POST'])
@login_required
def recoger_datos_creacion():
    user = current_user
    archivo = request.files.getlist("archivoSubir")[0]
    # Guardar archivo
    from main import uploads_dir
    uploads_dir_user = os.path.join(uploads_dir, user.id_mongo)
    if not os.path.exists(uploads_dir_user):
        os.makedirs(uploads_dir_user)
    filename = secure_filename(archivo.filename)
    path_guardado = os.path.join(uploads_dir_user, filename)
    archivo.save(path_guardado)
    archivo = open(path_guardado, 'rb').read()
    # Obtenemos metadatos
    metadatos = os.path.getctime(path_guardado)
    # Eliminamos el archivo original
    os.remove(path_guardado)
    # Generamos key (esta clave ya está cifrada)
    key = generar_clave(user.password, metadatos)
    # Ciframos archivo
    cifrado = cifrar_archivo(archivo, metadatos, key)
    # Guardamos archivo cifrado
    with open(path_guardado, 'wb') as f:
        f.write(cifrado)
    metadatos = str(metadatos)
    metadatos = metadatos.encode('utf-8')
    with open(path_guardado + ".metadata", 'wb') as f:
        f.write(bytes(metadatos))
    # Ciframos la clave
    ciphered_key = cifrar_clave(key)
    # Asociamos el archivo al usuario
    user.guardar_archivo(filename, ciphered_key)
    replace_user_by_id(user.id_mongo, user)
    return redirect(url_for('inicio'))
