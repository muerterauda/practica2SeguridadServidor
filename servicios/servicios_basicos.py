import os

from flask import Blueprint, redirect, url_for, request, render_template, jsonify, Response, send_from_directory
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from mongo.repository.usuario_repository import update_user_by_id

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

@servicios_basicos_bp.route("/descargarArchivo", methods=['GET'])
@login_required
def descargar_archivo():
    user = current_user
    nombre_archivo = request.values.get("nombre")
    nombre_archivo = 'Buy_3.jpg'
    from main import uploads_dir
    uploads_dir_user = os.path.join(uploads_dir, user.id_mongo)
    archivo = send_from_directory(directory=uploads_dir_user, filename='Buy_3.jpg')
    return archivo


@servicios_basicos_bp.route("/subirArchivo", methods=['POST'])
@login_required
def recoger_datos_creacion():
    user = current_user
    archivo = request.files.getlist("archivoSubir")
    from main import uploads_dir
    uploads_dir_user = os.path.join(uploads_dir, user.id_mongo)
    if not os.path.exists(uploads_dir_user):
        os.makedirs(uploads_dir_user)
    filename = secure_filename(archivo[0].filename)
    archivo[0].save(os.path.join(uploads_dir_user, filename))
    from google.cloud import kms_v1
    client = kms_v1.KeyManagementServiceClient()
    ruta = "projects/practicasegurdadatrest/locations/global/keyRings/my_keyring/cryptoKeys/seguridadAtRest"
    response = client.encrypt(ruta, archivo[0].read())
    with open(os.path.join(uploads_dir_user, filename+".enc"), 'wb') as f:
        f.write(response.ciphertext)
    return redirect(url_for('inicio'))
