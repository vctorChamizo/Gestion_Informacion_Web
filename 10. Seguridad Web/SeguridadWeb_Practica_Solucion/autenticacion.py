# -*- coding: utf-8 -*-


# Asignatura: Gestión de la Información Web
# Práctica: Consultas MongoDB
# Grupo: 10
# Autores: Sergio Martín, Víctor Chamizo, Fernando Lopez, Pablo Garcia e Irene Martín declaramos
# que esta solución es fruto exclusivamente de nuestro trabajo personal. No hemos sido ayudados
# por ninguna otra persona ni hemos obtenido la solución de fuentes externas, y tampoco hemos compartido
# nuestra solución con nadie. Declaramos ademáss que no hemos realizado de manera deshonesta ninguna otra
# actividad que pueda mejorar nuestros resultados ni perjudicar los resultados de los demás.


# Imports
from bottle import get, post, run, template, request, TEMPLATE_PATH
from pymongo import MongoClient
from passlib.hash import pbkdf2_sha256
import hashlib
import random

#Constants
PEPPER = "a21g01m96v1c9"

# Templates path
TEMPLATE_PATH.insert(0, "views")

# Inicializacion de BD
client = MongoClient()
db = client.giw_prac10
users = db.users

##############
# APARTADO 1 #
##############

# 
# Explicación detallada del mecanismo escogido para el almacenamiento de
# contraseñas, explicando razonadamente por qué es seguro
#

def encrypt (password):
    return pbkdf2_sha256.using(rounds = 100000).hash(password + PEPPER)

def passValidate (password, hash):
    return pbkdf2_sha256.verify(password + PEPPER, hash)


@post('/signup')
def signup():

    pass1 = request.forms.get("password")
    pass2 = request.forms.get("password2")
    nickname = request.forms.get("nickname")
    name = request.forms.get("name")

    if pass1 != pass2: return template('err_msg.html', err = "Las constraseñas no coinciden.")
    
    q = users.find({"nickname" : nickname})
    if q.count() > 0: return template('err_msg.html', err = "El alias de usuario ya existe.")
    
    encryptPassword = encrypt(pass1)

    newUser = {}
    newUser['nickname'] = nickname
    newUser['password'] = encryptPassword
    newUser['name'] = name
    newUser['email'] = request.forms.get("email")
    newUser['country'] = request.forms.get("country")

    users.insert(newUser)

    msg = "Bienvenido usuario " + name + "."

    return template('info_msg.html', msg = msg)


@post('/change_password')
def change_password():

    old_pass = request.forms.get("old_password")
    new_pass = request.forms.get("new_password")
    nickname = request.forms.get("nickname")
            
    q = users.find({"nickname" : nickname, "password": old_pass})
    if q.count() > 0: return template('err_msg.html', err = "Usuario o contraseña incorrectos.")

    encryptPassword = encrypt(new_pass)

    msg = "La contraselña del usuario " + nickname + " ha sido modificada."

    return template('info_msg.html', msg = msg)
    

@post('/login')
def login():
    pass


##############
# APARTADO 2 #
##############

# 
# Explicación detallada de cómo se genera la semilla aleatoria, cómo se construye
# la URL de registro en Google Authenticator y cómo se genera el código QR
#

@post('/signup_totp')
def signup_totp():
    pass
        
        
@post('/login_totp')        
def login_totp():
    pass

    
if __name__ == "__main__":
    # NO MODIFICAR LOS PARÁMETROS DE run()
    run(host='localhost',port=8080,debug=True)
