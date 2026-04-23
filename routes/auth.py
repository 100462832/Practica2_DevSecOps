from db import get_users_connection, verify_password
from flask import request, redirect, render_template, session, flash
from server import app
from urllib.parse import urlparse

# Correccion 1: Comprobar si la url destino es externa
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    dest_url = urlparse(target)
    return dest_url.scheme in ('http', 'https') and ref_url.netloc == dest_url.netloc

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect('/dashboard')
    next_url = request.args.get('next')
    # Validar que next_url sea seguro, si no, ir al dashboard
    if not next_url or not is_safe_url(next_url):
        next_url = '/dashboard'
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_users_connection()
        # Correccion 2: Consulta parametrizada
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()
        # Correccion 3: Verificacion del hash de forma segura
        if user and verify_password(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            session['company_id'] = user['company_id']
            session.permanent = True
            return redirect(next_url)
        else:
            flash("Invalid username or password", "danger")
            return render_template('auth/login.html', next_url=next_url)
    return render_template('auth/login.html', next_url=next_url)


@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect('/login')
