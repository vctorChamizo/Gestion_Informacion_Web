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
from bottle import get, run, template, request, TEMPLATE_PATH
from pymongo import MongoClient
import calendar
import locale
import re

# Templates path
TEMPLATE_PATH.insert(0, "views")

# Inicializacion de BD
client = MongoClient('localhost', 27017)
db = client.giw
collection = db.usuarios

# Funciones auxiliares
def findInvalidFields(fields):
	invalidFields = []
	validFields = {"name", "surname", "birthdate"}

	for field in fields:
		if field not in validFields:
			invalidFields.append(field)

	return invalidFields

def makeFindUsersQuery(name, surname, birthdate):
    query = {}

    if name is not None: query['name'] = name
    if surname is not None: query['surname'] = surname
    if birthdate is not None: query['birthdate'] = birthdate

    return query

# Find users
@get('/find_users')
def find_users():

    fields = request.query
    invalidFields = findInvalidFields(fields)

    if len(invalidFields) > 0:
        return template('listError.html', list_other = invalidFields)

    name = request.query.name
    surname = request.query.surname
    birthdate = request.query.birthdate

    query = makeFindUsersQuery(name, surname, birthdate)
    resultQuery = collection.find(query)

    return template('table.html', nUsers = resultQuery.count(), resultQuery = resultQuery)

    # http://localhost:8080/find_users?name=Luz
    # http://localhost:8080/find_users?name=Luz&surname=Romero
    # http://localhost:8080/find_users?name=Luz&surname=Romero&birthdate=2006-08-14
    # http://localhost:8080/find_users?name=Luz&food=paella&car=Audi

# Users born between two dates
@get('/find_email_birthdate')
def email_birthdate():

    fechaInicio = request.query.get('from')
    fechaFin = request.query.get['to']

    query = {'birthdate' : {"$gte" : fechaInicio, "$lte" : fechaFin}}, {'webpage' : 0, 'credit_card' : 0, 'password' : 0, 'name' : 0, 'surname' : 0, 'address' : 0, 'likes' : 0}

    resultQuery = collection.fin(query)

    return template('tableBirthdate.html', nUsers = resultQuery.count(), resultQuery = resultQuery)

    # http://localhost:8080/find_email_birthdate?from=1973-01-01&to=1990-12-31

# Users with matching likes
@get('/find_country_likes_limit_sorted')
def find_country_likes_limit_sorted():

    country = request.query.get("country")
    likes = request.query.get("likes").split(',')
    maxNumberOfUsers = request.query.get("limit")
    order = 1 if request.query.get("ord") == 'asc' else -1

    query = {'address.country' : country, 'likes' : {'$all' : likes}}
    resultQuery = collection.find(query).limit(int(maxNumberOfUsers)).sort([('birthdate', order)])

    return template('tableBirthdate.html', nUsers = resultQuery.count(), resultQuery = resultQuery)

    # http://localhost:8080/find_country_likes_limit_sorted?country=Irlanda&likes=movies,animals&limit=4&ord=asc

# Users born on a specific date
@get('/find_birth_month')
def find_birth_month():

    locale.setlocale(locale.LC_ALL, 'es_ES') # Para que calendar.month_name devuelva los meses en español
    month = request.query.get("month")
    numbersOfTheMonths = {value: key for key,value in enumerate(calendar.month_name)}

    regex = '[0-9]{4}-0?' + str(numbersOfTheMonths[month]) +  '-[0-9]{2}'

    query = {'birthdate' : {'$regex' : regex}}
    resultQuery = collection.find(query).sort([('birthdate', 1)])

    return template('tableBirthdate.html', nUsers = resultQuery.count(), resultQuery = resultQuery)

    # http://localhost:8080/find_birth_month?month=abril


# Users who dont have hobbies completed in the suffix
@get('/find_likes_not_ending')
def find_likes_not_ending():

    ending = request.query.get("ending").lower()
    regex = re.compile('.*' + ending + '$')

    query = {'likes' : {'$not' : regex}}
    resultQuery = collection.find(query).sort([('birthdate', 1)])

    return template('tableBirthdate.html', nUsers = resultQuery.count(), resultQuery = resultQuery)

    # http://localhost:8080/find_likes_not_ending?ending=s

# Users born in leap years
@get('/find_leap_year')
def find_leap_year():

	exp = request.query.get("exp")

    query = {'credit_card.expire.year' : {'$eq' : exp}, '$where' :
                """function() {
    	            let yearOfBirth = this.birthdate.substr(0,4);
    	            let yearOfBirthMod400 = yearOfBirth % 400;
    	            let yearOfBirthMod4 = yearOfBirth % 4;
    	            let yearOfBirthMod100 = yearOfBirth % 100;
    	            let isLeapYear = yearOfBirthMod400 == 0 || (yearOfBirthMod4 == 0 && yearOfBirthMod100 != 0);

    	            return isLeapYear;
                }"""
    }

	resultQuery = usuarios.find(query)

    return template('tableBirthdate.html', nUsers = resultQuery.count(), resultQuery = resultQuery)

    # http://localhost:8080/find_leap_year?exp=20

###################################
# NO MODIFICAR LA LLAMADA INICIAL #
###################################
if __name__ == "__main__":
  run(host='localhost',port=8080,debug=True)
