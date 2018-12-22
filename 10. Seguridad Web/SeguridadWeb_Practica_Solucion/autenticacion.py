## ASIGNATURA : GESTIÓN DE INFORMACIÓN EN LA WEB
## PRÁCTICA Autenticacion & TOTP
## GRUPO 10
## AUTORES: Victor Chamizo Rodriguez, Pablo García Hernandez, Fernando López Carrión, Irene Martín Berlanga y Sergio Martín Gómez

## Victor Chamizo Rodriguez, Pablo García Hernandez, Fernando López Carrión, Irene Martín Berlanga y Sergio Martín Gómez declaramos
## que esta solución es fruto exclusivamente de nuestro trabajo personal. No hemos sido ayudados por ninguna otra persona ni hemos 
## obtenido la solución de fuentes externas, y tampoco hemos compartido nuestra solución con nadie. Declaramos además que no hemos 
## realizado de manera deshonesta ninguna otra actividad que pueda mejorar nuestros resultados ni perjudicar los resultados de los demás.


from bottle import run, post, request, template
from pymongo import MongoClient
from passlib.hash import pbkdf2_sha256
import hashlib
import random
import onetimepass as otp
import base64

client = MongoClient()
db = client.giw
users = db.users

pepper = "1djkn71iu872njd"

##############
# APARTADO 1 #
##############

# El mecanismo utilizado para almacenar las contraseñas es generar un hash mediante
# un algoritmo de hash criptográfico utilizando además el algoritmo de ralentización pbkdf2. 
# El algoritmo utilizado genera una sal de 16 bytes por defecto, como se puede ver en la 
# documentación https://passlib.readthedocs.io/en/stable/lib/passlib.hash.pbkdf2_digest.html#passlib.hash.pbkdf2_sha256
# Además de la sal se utiliza una cadena constante que está en el código, llamada pimienta.
# El hash generado por este método contiene el algoritmo de ralentización utilizado (pbkdf2), la
# función criptográfica utilizada (SHA-256), la sal y el hash resultante. 

# Almacenar las contraseñas de esta manera es seguro ya que dos contraseñas iguales no darán
# como resultado el mismo hash debido a la aleatoriedad de la sal. Además un ataque de fuerza
# es inviable ya que al ralentizar la función hash el tiempo necesario para encontrar la contraseña
# asociada a un hash es demasiado elevado. 


def encrypt(password):
	return pbkdf2_sha256.using(rounds=100000).hash(password + pepper)

def passwordIsCorrect(password, hash):
	return pbkdf2_sha256.verify(password + pepper, hash)


@post('/signup')
def signup():
	nickname = request.forms.get("nickname")
	name = request.forms.get("name")
	country = request.forms.get("country")
	email = request.forms.get("email")
	password = request.forms.get("password")
	password2 = request.forms.get("password2")

	if password != password2:
		return template("mensaje_de_error", mensajeDeError="Las contraseñas no coinciden.")

	userExists = users.find({'_id' : nickname}).count();

	if userExists:
		return template("mensaje_de_error", mensajeDeError="El alias de usuario ya existe.")

	encryptedPassword = encrypt(password)

	users.insert_one({'_id' : nickname, 'name' : name, 'country' : country, 'email' : email, 'password' : encryptedPassword})	
	
	return template("correcto", message="Bienvenido usuario " + name)
    
@post('/change_password')
def change_password():
    nickname = request.forms.get("nickname")
    old_password = request.forms.get("old_password")
    new_password = request.forms.get("new_password")

    user = users.find({'_id' : nickname})
    
    try:
    	if passwordIsCorrect(old_password, user[0]['password']):
    		newPasswordEncrypted = encrypt(new_password)
    		users.update_one({'_id' : nickname}, {'$set' : {'password' : newPasswordEncrypted}})
    		return template("correcto", message="La contraseña del usuario " + nickname + " ha sido modificada.")
    	else:
    		return template("mensaje_de_error", mensajeDeError="Usuario o contraseña incorrectos.")
    except Exception as e:
    	return template("mensaje_de_error", mensajeDeError="Usuario o contraseña incorrectos.")

@post('/login')
def login():
	nickname = request.forms.get("nickname")
	password = request.forms.get("password")

	user = users.find({'_id' : nickname})

	try:
		if passwordIsCorrect(password, user[0]['password']):
			return template("correcto", message="Bienvenido " + user[0]['name'])
		else:
			return template("mensaje_de_error", mensajeDeError="Usuario o contraseña incorrectos.")
	except Exception as e:
		return template("mensaje_de_error", mensajeDeError="Usuario o contraseña incorrectos.")

##############
# APARTADO 2 #
##############

# 
# La semilla aleatoria se genera haciendo una cadena aleatoria de 16 caracteres y se codifica
# en base32. Esta semilla se muestra al usuario y es la cadena de texto que se utiliza para
# generar el código QR. El código QR se genera con la API especificada en el enunciado, 
# insertando una etiqueta <img> en la plantilla para que haga una petición GET a una URL.
#



def generateRandomSeed():
	randomSeed = ''
	ALPHABET = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
	chars=[]
	for i in range(16):
		chars.append(random.choice(ALPHABET))

	randomSeed = randomSeed.join(chars)

	return randomSeed

def encodeBase32(randomSeed):
	return base64.b32encode(randomSeed.encode("UTF-8"))

def decode(seed):
	return base64.b32decode(seed.encode("UTF-8"))

def getTOTP(secret):
	return otp.get_totp(secret)

def isValidTOTP(token, secret):
	return otp.valid_totp(token, secret)


@post('/signup_totp')
def signup_totp():
	randomSeed = generateRandomSeed()
	randomSeed = encodeBase32(randomSeed)

	nickname = request.forms.get("nickname")
	name = request.forms.get("name")
	country = request.forms.get("country")
	email = request.forms.get("email")
	password = request.forms.get("password")
	password2 = request.forms.get("password2")

	if password != password2:
		return template("mensaje_de_error", mensajeDeError="Las contraseñas no coinciden.")

	userExists = users.find({'_id' : nickname}).count();

	if userExists:
		return template("mensaje_de_error", mensajeDeError="El alias de usuario ya existe.")

	encryptedPassword = encrypt(password)

	users.insert_one({'_id' : nickname, 'name' : name, 'country' : country, 'email' : email, 'password' : encryptedPassword, 'seed' : randomSeed})	

	return template("correctoTOTP", message="Bienvenido usuario " + name, seed=randomSeed[:-6])
    

@post('/login_totp')        
def login_totp():
	nickname = request.forms.get("nickname")
	password = request.forms.get("password")
	totp = request.forms.get("totp")

	encryptedPassword = encrypt(password)

	user = users.find({'_id' : nickname})

	try:
		if passwordIsCorrect(password, user[0]['password']) and isValidTOTP(totp, user[0]['seed']):
			return template("correcto", message="Bienvenido " + user[0]['name'])
		else:
			return template("mensaje_de_error", mensajeDeError="Usuario o contraseña incorrectos.")
	except Exception as e:
		print (e)
		return template("mensaje_de_error", mensajeDeError="Usuario o contraseña incorrectos.")


    
if __name__ == "__main__":
    # NO MODIFICAR LOS PARÁMETROS DE run()
    run(host='localhost',port=8080,debug=True)
