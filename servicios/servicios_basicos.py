
import base64

from flask import Blueprint, redirect, url_for, render_template, request
from flask_login import login_required, current_user


servicios_basicos_bp = Blueprint('Seguridad_servicios_basicos', __name__, template_folder='templates')

@servicios_basicos_bp.route("/subirArchivo", methods=['POST'])
@login_required
def recoger_datos_creacion():
    archivo = request.files.getlist("archivoSubir")
    return redirect(url_for('inicio'))