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
from pprint import pprint 

# Templates path
TEMPLATE_PATH.insert(0, "views")

# Inicializacion de BD
client = MongoClient('localhost', 27017)
db = client.giw_prac10
users = db.users

##############
# APARTADO 1 #
##############

# 
# Explicación detallada del mecanismo escogido para el almacenamiento de
# contraseñas, explicando razonadamente por qué es seguro
#


@post('/signup')
def signup():
    form = request.forms.get("password")
    print(form)

@post('/change_password')
def change_password():
    pass
            

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
