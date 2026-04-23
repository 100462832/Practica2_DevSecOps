from flask import Flask, render_template
import secrets
from flask_wtf.csrf import CSRFProtect
from datetime import timedelta

app = Flask(__name__)
# Correccion 1: Implementacion de token CSRF
app.secret_key = secrets.token_hex(32)
# Correccion 2: Tiempo de sesion reducido
app.permanent_session_lifetime = timedelta(minutes=20)
# Correccion 3: Implementacion de token CSRF
csrf = CSRFProtect(app)

# Correccion 4: Configuracion de las flags de seguridad de las cookies
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_SAMESITE='Lax',
)

@app.errorhandler(404)
def not_found(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(403)
def forbidden(e):
    return render_template('errors/403.html'), 403

