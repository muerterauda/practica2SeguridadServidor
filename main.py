import json
import os

import flask
from flask import Flask, url_for, redirect, \
    render_template, session, request, send_from_directory
from flask_login import LoginManager, login_required, current_user, logout_user, login_user
from mysqlx import Auth
from requests.exceptions import HTTPError
from requests_oauthlib import OAuth2Session

from mongo.entity.usuario import User
from mongo.repository.usuario_repository import find_user_by_id, replace_user_by_id, update_user_by_id, save_user
from servicios.servicios_basicos import servicios_basicos_bp

basedir = os.path.abspath(os.path.dirname(__file__))

ruta = "C:\\Users\\Thoriones\\Downloads\\practicasegurdadatrest-481ffbd20405.json"
# ruta = "C:\\Users\\Muerterauda\\Desktop\\practicasegurdadatrest-481ffbd20405.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = ruta
os.environ[
    'PROJECT_KEY_PATH'] = "projects/practicasegurdadatrest/locations/global/keyRings/my_keyring/cryptoKeys/seguridadAtRest"
os.environ['PROJECT_ID'] = "practicasegurdadatrest"

"""App Configuration"""


class Auth:
    """Google Project Credentials"""
    CLIENT_ID = '393209363579-cs7u7kk4dpflnhpsdckv1f5pvau4443o.apps.googleusercontent.com'
    CLIENT_SECRET = 'v1gtkZqsczHmqlPGZ8e4DAsP'
    REDIRECT_URI = 'https://localhost:5000/gCallback'
    AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
    TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'
    USER_INFO = 'https://www.googleapis.com/userinfo/v2/me'
    SCOPE = ['profile', 'email']


class Config:
    """Base config"""
    APP_NAME = "Practica de seguridad"
    SECRET_KEY = "somethingsecret"


config = {
    "dev": Config,
    "default": Config
}

"""APP creation and configuration"""
app = Flask(__name__, static_folder="static")
app.config.from_object(config['dev'])
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.session_protection = "strong"


@login_manager.user_loader
def load_user(user_id):
    if user_id:
        return find_user_by_id(user_id)
    else:
        return None


""" OAuth Session creation """


def get_google_auth(state=None, token=None):
    if token:
        return OAuth2Session(Auth.CLIENT_ID, token=token)
    if state:
        return OAuth2Session(
            Auth.CLIENT_ID,
            state=state,
            redirect_uri=Auth.REDIRECT_URI)
    oauth = OAuth2Session(
        Auth.CLIENT_ID,
        redirect_uri=Auth.REDIRECT_URI,
        scope=Auth.SCOPE)
    return oauth


@app.route('/login')
def login():
    if current_user.is_authenticated:
        next_f = flask.request.args.get('next')
        if not next_f:
            next_f = session.get('next_f')
        return flask.redirect(next_f or flask.url_for('inicio'))
    google = get_google_auth()
    next_f = flask.request.args.get('next')
    if next_f:
        auth_url, state = google.authorization_url(
            Auth.AUTH_URI, access_type='offline')
        session['next_f'] = next_f
    else:
        auth_url, state = google.authorization_url(
            Auth.AUTH_URI, access_type='offline')
    session['oauth_state'] = state
    return render_template('login.html', auth_url=auth_url)


@app.route('/gCallback')
def callback():
    next_f = session.get('next_f')
    if current_user is not None and current_user.is_authenticated:
        return redirect(url_for(next_f))
    if 'error' in request.args:
        if request.args.get('error') == 'access_denied':
            return 'You denied access.'
        return 'Error encountered.'
    if 'code' not in request.args and 'state' not in request.args:
        return redirect(url_for('login'))
    else:
        google = get_google_auth(state=session['oauth_state'])
        try:
            token = google.fetch_token(
                Auth.TOKEN_URI,
                client_secret=Auth.CLIENT_SECRET,
                authorization_response=request.url)
        except HTTPError:
            return 'HTTPError occurred.'
        google = get_google_auth(token=token)
        resp = google.get(Auth.USER_INFO)
        if resp.status_code == 200:
            user_data = resp.json()
            email = user_data['email']
            user = find_user_by_id(email)
            if user is None:
                dicccionario_usuario = {'id': email, 'name': user_data['name'], 'avatar': user_data['picture'],
                                        'password': ''}
                user = User(dicccionario_usuario)
                save_user(user)
                user = find_user_by_id(email)
            else:
                cambiado = False
                if user_data['name'] != user.name:
                    user.name = user_data['name']
                    cambiado = True
                if user.avatar != user_data['picture']:
                    user.avatar = user_data['picture']
                    cambiado = True
                user.access_tokens = json.dumps(token)
                if cambiado:
                    replace_user_by_id(user.id_mongo, user)
                else:
                    update_user_by_id(user.id_mongo, {"tokens": user.access_tokens})
            login_user(user)
            if next_f:
                return redirect(next_f)
            else:
                return redirect(url_for('inicio'))
        return 'No se pudo conseguir su informacion'


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/')
@login_required
def inicio():
    user = current_user
    return render_template("inicio.html", user=user)


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('resources/static/js', path)


@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('resources/static/css', path)


@app.route('/img/<path:path>')
def send_img(path):
    return send_from_directory('resources/static/img', path)


app.register_blueprint(servicios_basicos_bp, url_prefix="/serviciosBasicos/")
uploads_dir = os.path.join(app.instance_path, 'archivos')
uploads_dir = uploads_dir.replace('instance', '')
uploads_dir = uploads_dir.replace('\\\\', '\\')
if not os.path.exists(uploads_dir):
    os.makedirs(uploads_dir)

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(ssl_context='adhoc', host='localhost', debug=True)
