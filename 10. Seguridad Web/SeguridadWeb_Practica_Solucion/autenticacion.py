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

# Initialization of DB
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
    email = request.forms.get("email")
    country = request.forms.get("country")

    if pass1 != pass2: return template('info_msg.html', msg = "ERROR: Las constraseñas no coinciden.")
    
    q = users.find({"nickname" : nickname})
    if q.count() > 0: return template('info_msg.html', msg = "ERROR: El alias de usuario ya existe.")
    
    encryptPassword = encrypt(pass1)

    newUser = {}
    newUser['nickname'] = nickname
    newUser['password'] = encryptPassword
    newUser['name'] = name
    newUser['email'] = email
    newUser['country'] = country

    users.insert(newUser)

    return template('info_msg.html', msg = "Bienvenido usuario " + name + ".")


@post('/change_password')
def change_password():

    old_pass = request.forms.get("old_password")
    new_pass = request.forms.get("new_password")
    nickname = request.forms.get("nickname")

    q = users.find({"nickname" : nickname}, {"password": 1})

    if passValidate(old_pass, q[0]['password']) == False: return template('info_msg.html', msg = "ERROR: Usuario o contraseña incorrectos.")
    
    encryptNewPassword = encrypt(new_pass)

    users.update({"nickname" : nickname}, {"$set": {"password": encryptNewPassword}})

    return template('info_msg.html', msg = "La contraseña del usuario " + nickname + " ha sido modificada.")
    

@post('/login')
def login():
    
    password = request.forms.get("password")
    nickname = request.forms.get("nickname")

    q = users.find({"nickname" : nickname}, {"_id": 0, "password": 1, "name": 1})

    msg = "Bienvenido usuario " + q[0]['name'] + "."

    if passValidate(password, q[0]['password']): return template('info_msg.html', msg = msg)
    else : return template('info_msg.html', msg = "ERROR: Usuario o contraseña incorrectos.")


##############
# APARTADO 2 #
##############

# 
# Explicación detallada de cómo se genera la semilla aleatoria, cómo se construye
# la URL de registro en Google Authenticator y cómo se genera el código QR
#

@post('/signup_totp')
def signup_totp():
    
    pass1 = request.forms.get("password")
    pass2 = request.forms.get("password2")
    nickname = request.forms.get("nickname")
    name = request.forms.get("name")
    email = request.forms.get("email")
    country = request.forms.get("country")

    if pass1 != pass2: return template('info_msg.html', msg = "ERROR: Las constraseñas no coinciden.")
    
    q = users.find({"nickname" : nickname})
    if q.count() > 0: return template('info_msg.html', msg = "ERROR: El alias de usuario ya existe.")
        


        
        
@post('/login_totp')        
def login_totp():
    pass

    
if __name__ == "__main__":
    # NO MODIFICAR LOS PARÁMETROS DE run()
    run(host='localhost',port=8080,debug=True)
