from flask import Blueprint, redirect, url_for, request, render_template, jsonify
from flask_login import login_required, current_user, login_user
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


@servicios_basicos_bp.route("/subirArchivo", methods=['POST'])
@login_required
def recoger_datos_creacion():
    user = current_user
    archivo = request.files.getlist("archivoSubir")
    return redirect(url_for('inicio'))
