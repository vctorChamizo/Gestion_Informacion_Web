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
from pprint import pprint 

# Templates path
TEMPLATE_PATH.insert(0, "views")

# Inicializacion de BD
client = MongoClient()
db = client.giw_prac9
usuarios = db.usuarios
pedidos = db.pedidos



@get('/top_countries')
# http://localhost:8080/top_countries?n=3
def agg1():

    n_max = int(request.query.n)

    agg = [ {"$group": {"_id": "$pais", "count": {"$sum": 1}}},
            {"$project": {"_id": 0, "pais": "$_id", "total_usuarios": "$count"}},
            {"$sort": {"total_usuarios": -1}},
            {"$limit":  n_max} ]

    result = list(usuarios.aggregate(agg))
    return template('agg1.html', n = len(result), result = result)



@get('/products')
# http://localhost:8080/products?min=2.34
def agg2():
    
    min = float(request.query.min)

    agg = [ {"$unwind": "$lineas"},
            {"$match": {"lineas.precio": {"$gte": min}}},
            {'$group' : {"_id" : "$lineas.nombre", 'num_uni' : {'$sum' : 1}, 'precioUnitario' : {'$first' : "$lineas.precio"}}},
            {"$project": { "_id": 0, "nombre_producto": "$_id", "numero_unidades": "$num_uni", "precio_unitario": "$lineas.precio"}}]

    result = list(pedidos.aggregate(agg))
    return template('agg2.html', n = len(result), result = result)



@get('/age_range')
# http://localhost:8080/age_range?min=80
def agg3():

    min = int(request.query.min)

    agg = [ {"$group": {"_id": "$pais", "count": {"$sum": 1}, "max_age": {"$max": "$edad"}, "min_age": {"$min": "$edad"}}},
            {"$match": {count: {"$gt": min}}},
            {"$project": { "_id": 0, "pais": "$_id", "rango_edades": {"$subtract": ["$max_age", "$min_age"]}}}]

    result = list(usuarios.aggregate(agg))
    return template('agg3.html', n = len(result), result = result)



@get('/avg_lines')
# http://localhost:8080/avg_lines
def agg4():

    agg = [ {"$lookup": {"from": "usuarios", "localField": "cliente", "foreignField": "_id", "as": "usuarios"}},
            {"$group": {"_id": "$usuarios.pais", "lp": {"$avg": {"$size": "$lineas"}}}},
            {"$project": {"_id": 0, "pais": "$_id", "promedio_lineas_pedidos": "$lp"}}]

    result = list(usuarios.aggregate(agg))
    return template('agg4.html', n = len(result), result = result)



@get('/total_country')
# http://localhost:8080/total_country?c=Alemania
def agg5():
    
    country = request.query.c

    agg = [ {"$lookup": {"from": "usuarios", "localField": "cliente", "foreignField": "_id", "as": "usuarios"}},
            {"$group": {"_id": "$usuarios.pais", "gasto": {"$sum": "$total"}}},
            {"$match": {"_id": country}},
            {"$project": {"_id": 0, "pais": "$_id", "gasto_total": "$gasto"}}]

    result = list(usuarios.aggregate(agg))
    return template('agg5.html', n = rlen(result), result = result)



if __name__ == "__main__":
    # No cambiar host ni port ni debug
    run(host='localhost',port=8080,debug=True)
