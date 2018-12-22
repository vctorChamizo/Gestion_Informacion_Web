# -*- coding: utf-8 -*-
"""
@author: Enrique Martín Martín
@email: emartinm@ucm.es
"""

from bottle import run, get, request, redirect, app
from beaker.middleware import SessionMiddleware
import sqlite3


# Vulnerabilidad Cross-Site Request Forgery

# Es posible que en navegadores modernos (Chrome, Firefox) no se produzca ninguna
# falsificación porque la peticiòn de la imagen dentro de csrf.html no lleva
# ninguna cookie [medida de seguridad]
# Probado con éxito en el navegador Epiphany 3.28.1 (Ubuntu 18.04 LTS)

# Pasos para reproducirla
# 1.- En pestaña 1: autenticarse
#    http://localhost:8080/login?user=pepe&pass=1234
# 2.- En pestaña 2: comprobar sesión
#    http://localhost:8080/sessinfo
# 3.- En pestaña 3: ver otra página "inocente"
#    csrf.html
# 4.- En pestaña 2: comprobar sesión otra vez -> contraseña cambiada
#    http://localhost:8080/sessinfo

	
@get('/login')
def login():
    passwd = request.query['pass']
    user = request.query['user']

    query = "SELECT * FROM users WHERE username='{0}'".format(user)
    conn = sqlite3.connect('database.db') 
    cur = conn.cursor()
    cur.execute(query)
    
    try:
        row = cur.fetchone()
        conn.close()
        user_password = row[2]
        assert user_password == passwd
        s = request.environ.get('beaker.session')
        s.invalidate() # Regenera la sesión para evitar posible session fixation
        s['username'] = user
        s.save()
        return "Bienvenido {0}!".format(user)
    except:
        s = request.environ.get('beaker.session')
        s.delete()
        return "Usuario o contraseña incorrectos"
        
        
@get('/change_pass')        
def change_pass():
    session = request.environ.get('beaker.session')
    if 'username' in session:
        # Usuario autenticado
        qbody = "UPDATE users SET password='{1}' WHERE username='{0}'"
        new_passwd = request.query['pass']
        query = qbody.format(session['username'], new_passwd)
        conn = sqlite3.connect('database.db') 
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        conn.close()
        return "Contraseña modificada"
        
    else:
        return "Imposible modificar la contraseña"
        
			
@get('/sessinfo')
def sessinfo():
    sessid = request.get_cookie("beaker.session.id")
    s = request.environ.get('beaker.session')
    html = "<h1>Datos de la sessión</h1>\n<ul>\n"
    html += "<li>SESSION ID: " + sessid + "</li>\n"
    for k in s:
        html += "<li>" + str(k) + ": " + str(s[k]) + "</li>\n"
    html += "</ul>\n"
    html += "<h1>Datos del usuario en la base de datos</h1>\n</ul>"

    username = s['username']    
    query = "SELECT * FROM users WHERE username='{0}'".format(username)
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute(query)
    row = cur.fetchone()
    conn.close()
    for v in row:
        html += "<li>" + str(v) + "</li>\n"
    html += "</ul>\n"    
    return html
	
 
@get('/logout')
def logout():
	s = request.environ.get('beaker.session')
	s.delete() # Elimina la session del servidor y expira la cookie en 
     # el navegador del usuario
	redirect('fuera')

	
@get('/fuera')
def fuera():
    html = "<h1>Has cerrado la sesión completamente</h1>\n\n"
    sessid = request.get_cookie("beaker.session.id")
    
    if not (sessid is None):
        html += "<li>SESSION ID: " + sessid + "</li>\n"
        s = request.environ.get('beaker.session')
        html += "<ul>\n"
        for k in s:
            html += "<li>" + str(k) + ": " + str(s[k]) + "</li>\n"
        html += "</ul>"
        
    return html


if __name__ == "__main__":
    # Sesiones usando beaker.session
    session_opts = {
        'session.type' : 'file',
        'session.cookie_expires': 300,
        'session.data_dir': './data',
        'session.auto': True, # se salva automaticamente sin llamar a save()
        'session.httponly': True,
    }
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.executescript("""
      DROP TABLE IF EXISTS users;
      CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT);
      INSERT INTO users VALUES(0,'pepe','1234');
    """)
    app = SessionMiddleware(app(), session_opts)
    run(host='localhost',port=8080,debug=True,app=app)
