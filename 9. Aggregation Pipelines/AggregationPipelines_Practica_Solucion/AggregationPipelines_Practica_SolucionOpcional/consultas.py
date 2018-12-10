## ASIGNATURA : GESTIÓN DE INFORMACIÓN EN LA WEB
## PRÁCTICA Aggregation Pipelines
## GRUPO 10
## AUTORES: Victor Chamizo Rodriguez, Pablo García Hernandez, Fernando López Carrión, Irene Martín Berlanga y Sergio Martín Gómez

## Victor Chamizo Rodriguez, Pablo García Hernandez, Fernando López Carrión, Irene Martín Berlanga y Sergio Martín Gómez declaramos
## que esta solución es fruto exclusivamente de nuestro trabajo personal. No hemos sido ayudados por ninguna otra persona ni hemos 
## obtenido la solución de fuentes externas, y tampoco hemos compartido nuestra solución con nadie. Declaramos además que no hemos 
## realizado de manera deshonesta ninguna otra actividad que pueda mejorar nuestros resultados ni perjudicar los resultados de los demás.

from bottle import get, run, request, template
from pymongo import MongoClient
import calendar
import locale
import re

client = MongoClient()
db = client.giw
usuarios = db.usuarios
pedidos = db.pedidos

@get('/top_countries')
# http://localhost:8080/top_countries?n=3
def agg1():
	n = int(request.query.get("n"))

	query = []
	query.append({'$group' : {'_id' : '$pais', 'numeroDeUsuarios' : {'$sum' : 1} } } )
	query.append({'$sort' : {'numeroDeUsuarios' : -1, '_id' : 1} } )
	query.append({'$limit' : n})
	resultadoQuery = list(usuarios.aggregate(query))
	
	return template("mostrar_resultados_2_columnas", resultadoQuery=resultadoQuery, numeroDeDocumentos=len(resultadoQuery), nombreSegundoCampo="numeroDeUsuarios", nombreSegundaColumna="Numero de usuarios")

@get('/products')
# http://localhost:8080/products?min=2.34
def agg2():
    precioMinimo = float(request.query.get("min"))

    query = []
    query.append({'$unwind' : '$lineas'})
    query.append({'$match' : { "lineas.precio" : {'$gte' : precioMinimo} } })
    query.append({'$group' : {"_id" : "$lineas.nombre", 'numeroDeUnidadesVendidas' : {'$sum' : 1}, 'precioUnitario' : {'$first' : "$lineas.precio"} } } )

    resultadoQuery = list(pedidos.aggregate(query))

    return template("mostrar_resultados_3_columnas", resultadoQuery=resultadoQuery, numeroDeDocumentos=len(resultadoQuery))
    
@get('/age_range')
# http://localhost:8080/age_range?min=80
def agg3():
	numeroMinimoDeUsuarios = int(request.query.get("min"))

	query = []
	query.append({'$group' : {"_id" : "$pais", 'numeroDeUsuarios' : {'$sum' : 1}, 'edadMaxima' : {'$max' : "$edad"}, 'edadMinima' : {'$min' : "$edad"} } })
	query.append({'$addFields' : {'rangoDeEdad' : {'$subtract' : ["$edadMaxima", "$edadMinima"] } } })
	query.append({'$match' : {'numeroDeUsuarios' : {'$gt' : numeroMinimoDeUsuarios} } } )
	query.append({'$sort' : { 'rangoDeEdad' : -1, '_id' : 1} } )

	resultadoQuery = list(usuarios.aggregate(query))
	
	return template("mostrar_resultados_2_columnas", resultadoQuery=resultadoQuery, numeroDeDocumentos=len(resultadoQuery), nombreSegundoCampo="rangoDeEdad", nombreSegundaColumna="Rango de edades")
     
@get('/avg_lines')
# http://localhost:8080/avg_lines
def agg4():
	query = []
	query.append({'$lookup' : {"from" : "pedidos", 'localField' : '_id', 'foreignField' : 'cliente', 'as' : 'pedidos' } })
	query.append({'$unwind' : '$pedidos' })
	query.append({'$group' : {'_id' : '$pais', 'numeroDeLineasPromedio' : {'$avg' : {'$size' : '$pedidos.lineas'} } } } )

	resultadoQuery = list(usuarios.aggregate(query))
	
	return template("mostrar_resultados_2_columnas", resultadoQuery=resultadoQuery, numeroDeDocumentos=len(resultadoQuery), nombreSegundoCampo="numeroDeLineasPromedio", nombreSegundaColumna="Numero de lineas promedio")

    
    
@get('/total_country')
# http://localhost:8080/total_country?c=Alemania
def agg5():
	pais = request.query.get("c")

	query = []
	query.append({'$match' : {'pais' : pais}})
	query.append({'$lookup' : {"from" : "pedidos", 'localField' : '_id', 'foreignField' : 'cliente', 'as' : 'pedidos' } })
	query.append({'$unwind' : '$pedidos' })
	query.append({'$group' : {'_id' : '$pais', 'totalGastado' : {'$sum' : '$pedidos.total' } } } )

	resultadoQuery = list(usuarios.aggregate(query))
	return template("mostrar_resultados_2_columnas", resultadoQuery=resultadoQuery, numeroDeDocumentos=len(resultadoQuery), nombreSegundoCampo="totalGastado", nombreSegundaColumna="Total gastado")
    
        
if __name__ == "__main__":
    # No cambiar host ni port ni debug
    run(host='localhost',port=8080,debug=True)
