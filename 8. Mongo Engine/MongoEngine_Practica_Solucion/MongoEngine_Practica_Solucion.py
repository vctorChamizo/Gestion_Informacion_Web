 
## ASIGNATURA : GESTIÓN DE INFORMACIÓN EN LA WEB
## PRÁCTICA MongoEngine
## GRUPO 10
## AUTORES: Victor Chamizo Rodriguez, Pablo García Hernandez, Fernando López Carrión, Irene Martín Berlanga y Sergio Martín Gómez

## Victor Chamizo Rodriguez, Pablo García Hernandez, Fernando López Carrión, Irene Martín Berlanga y Sergio Martín Gómez declaramos
## que esta solución es fruto exclusivamente de nuestro trabajo personal. No hemos sido ayudados por ninguna otra persona ni hemos 
## obtenido la solución de fuentes externas, y tampoco hemos compartido nuestra solución con nadie. Declaramos además que no hemos 
## realizado de manera deshonesta ninguna otra actividad que pueda mejorar nuestros resultados ni perjudicar los resultados de los demás.

from mongoengine import *
import datetime
import re


connect('giw_mongoengine')

class Producto(Document):
	codigoDeBarras = StringField(primary_key=True, regex="[0-9]{13}")
	nombre = StringField(required=True)
	categoriaPrincipal = IntField(required=True)
	categoriasSecundarias = ListField(IntField())

	def cumpleCondicionCategorias(self):
		tieneCategoriasSecundarias = len(self.categoriasSecundarias) > 0
		principalEstaEnPrimerLugar = True

		if tieneCategoriasSecundarias:
			principalEstaEnPrimerLugar = self.categoriaPrincipal == self.categoriasSecundarias[0]

		return not tieneCategoriasSecundarias or principalEstaEnPrimerLugar

	def sumarDigitosEnPosicionesPares(self):
		sumaDigitosEnPosicionesPares = 0

		for digito in self.codigoDeBarras[1::2]:
			sumaDigitosEnPosicionesPares += int(digito)

		return sumaDigitosEnPosicionesPares

	def sumarDigitosEnPosicionesImpares(self):
		sumaDigitosEnPosicionesImpares = 0

		for digito in self.codigoDeBarras[0:-1:2]:
			sumaDigitosEnPosicionesImpares += int(digito)

		return sumaDigitosEnPosicionesImpares


	def comprobarCodigoDeBarras(self):
		checksum = 3 * self.sumarDigitosEnPosicionesPares()
		checksum += self.sumarDigitosEnPosicionesImpares()

		checksum = 10 - (checksum % 10)

		if checksum == 10:
			checksum = 0

		return checksum == int(self.codigoDeBarras[-1:])  

	def clean(self):
		cumpleCondicionDeCategorias = self.cumpleCondicionCategorias()
		estaBienFormadoElCodigoDeBarras = self.comprobarCodigoDeBarras()

		if not cumpleCondicionDeCategorias:
			raise ValidationError("El producto " + self.nombre + " no cumple la condición de categorias.")
		elif not estaBienFormadoElCodigoDeBarras:
			raise ValidationError("El codigo de barras del producto " + self.nombre + " no está bien formado.")

class LineaDePedido(EmbeddedDocument):
	cantidadDelProducto = IntField(required=True, min_value=1)
	precioDelProducto = FloatField(required=True, min_value=0)
	nombreDelProducto = StringField(required=True)
	precioTotalDeLaLinea = FloatField(required=True, min_value=0)
	producto = ReferenceField(Producto, required=True)

	def clean(self):
		nombresCoinciden = self.nombreDelProducto == self.producto.nombre
		precioCorrectamenteCalculado = self.precioTotalDeLaLinea == self.cantidadDelProducto * self.precioDelProducto
		
		if not nombresCoinciden:
			raise ValidationError("El nombre del producto no coincide en la línea" + self.producto.nombre + ".")
		elif not precioCorrectamenteCalculado:
			raise ValidationError("El precio de la linea " + self.nombreDelProducto + " no es correcto.")


class Pedido(Document):
	precio = FloatField(required=True, min_value=0)
	fecha = ComplexDateTimeField(required=True)
	lineasDelPedido = ListField(EmbeddedDocumentField(LineaDePedido), required=True)

	def clean(self):
		precioTotalLineas = 0

		for linea in self.lineasDelPedido:
			precioTotalLineas += linea.precioTotalDeLaLinea

		if self.precio != precioTotalLineas:
			raise ValidationError("El precio del pedido con precio " + str(self.precio) + " no coincide con el de sus líneas: " + str(precioTotalLineas))


class Usuario(Document):
	dni = StringField(primary_key=True, regex="[0-9]{7,8}-?[A-Z]{1}")
	nombre = StringField(required=True)
	primerApellido = StringField(required=True)
	segundoApellido = StringField()

	fechaDeNacimiento = StringField(required=True, regex="([12]\\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\\d|3[01]))") 
	ultimosDiezAccesosAlSistema = ListField(ComplexDateTimeField)
	tarjetasDeCredito = ListField(StringField())
	pedidos = ListField(ReferenceField(Pedido, reverse_delete_rule=4))

	def clean(self):
		mapaRestosLetrasDni = {0 : "T", 1 : "R", 2 : "W", 3 : "A", 4 : "G", 5 : "M", 6 : "Y", 7 : "F", 8 : "P",
						   9 : "D", 10 : "X", 11 : "B", 12 : "N", 13 : "J", 14 : "Z", 15 : "S", 16 : "Q", 
						   17 : "V", 18 : "H", 19 : "L", 20 : "C", 21 : "K", 22 : "E"}

		m = re.search('([0-9]{7,8})', self.dni)
		numerosDni = int(m.group(0))
		numerosDniMod23 = numerosDni % 23
		digitoDeControl = self.dni[-1]

		if digitoDeControl != mapaRestosLetrasDni[numerosDniMod23]:
			raise ValidationError("El dígito de control del dni " + self.dni + " no es correcto.")


class TarjetaDeCredito(Document):
	propietario = StringField(required=True)
	numero = StringField(primary_key=True, regex="[0-9]{16}")
	mesDeCaducidad = StringField(required=True, regex="^(0?[1-9]|1[012])$")
	añoDeCaducidad = StringField(required=True, regex="[1-9]{2}")
	codigoDeVerificacion = IntField(required=True, min_value=100, max_value=999)


def insertar():

	# ¿Hay que meter alguno mal para que salte ValidationError?
	producto1 = Producto(codigoDeBarras="0012345678905", nombre="PS4", categoriaPrincipal=1, categoriasSecundarias=[1, 2])
	producto2 = Producto(codigoDeBarras="9780201379624", nombre="Xbox", categoriaPrincipal=2)
	producto3 = Producto(codigoDeBarras="1234567890197", nombre="Nintendo Switch", categoriaPrincipal=5, categoriasSecundarias=[5, 4])
	producto4 = Producto(codigoDeBarras="1254567890195", nombre="Super Mario Odissey", categoriaPrincipal=8)

	linea1Pedido1Usuario1 = LineaDePedido(cantidadDelProducto=6, precioDelProducto=5.0, nombreDelProducto="PS4", precioTotalDeLaLinea=30.0, producto=producto1)
	linea2Pedido1Usuario1 = LineaDePedido(cantidadDelProducto=1, precioDelProducto=5.0, nombreDelProducto="Xbox", precioTotalDeLaLinea=5.0, producto=producto2)
	
	linea1Pedido2Usuario1 = LineaDePedido(cantidadDelProducto=7, precioDelProducto=5.0, nombreDelProducto="Nintendo Switch", precioTotalDeLaLinea=35.0, producto=producto3)
	linea2Pedido2Usuario1 = LineaDePedido(cantidadDelProducto=2, precioDelProducto=5.0, nombreDelProducto="Super Mario Odissey", precioTotalDeLaLinea=10.0, producto=producto4)

	linea1Pedido1Usuario2 = LineaDePedido(cantidadDelProducto=8, precioDelProducto=5.0, nombreDelProducto="PS4", precioTotalDeLaLinea=40.0, producto=producto1)
	linea2Pedido1Usuario2 = LineaDePedido(cantidadDelProducto=3, precioDelProducto=5.0, nombreDelProducto="Xbox", precioTotalDeLaLinea=15.0, producto=producto2)
	
	linea1Pedido2Usuario2 = LineaDePedido(cantidadDelProducto=5, precioDelProducto=5.0, nombreDelProducto="Nintendo Switch", precioTotalDeLaLinea=25.0, producto=producto3)
	linea2Pedido2Usuario2 = LineaDePedido(cantidadDelProducto=8, precioDelProducto=5.0, nombreDelProducto="Super Mario Odissey", precioTotalDeLaLinea=40.0, producto=producto4)
	
	lineasPedido1Usuario1 = [linea1Pedido1Usuario1, linea2Pedido1Usuario1]
	lineasPedido2Usuario1 = [linea1Pedido2Usuario1, linea2Pedido2Usuario1]

	lineasPedido1Usuario2 = [linea1Pedido1Usuario2, linea2Pedido1Usuario2]
	lineasPedido2Usuario2 = [linea1Pedido2Usuario2, linea2Pedido2Usuario2]

	pedido1Usuario1 = Pedido(precio=35.0, fecha=datetime.datetime.now(), lineasDelPedido=lineasPedido1Usuario1)
	pedido2Usuario1 = Pedido(precio=45.0, fecha=datetime.datetime.now(), lineasDelPedido=lineasPedido2Usuario1)
	
	pedido1Usuario2 = Pedido(precio=55.0, fecha=datetime.datetime.now(), lineasDelPedido=lineasPedido1Usuario2)
	pedido2Usuario2 = Pedido(precio=65.0, fecha=datetime.datetime.now(), lineasDelPedido=lineasPedido2Usuario2)

	tarjeta1Usuario1 = TarjetaDeCredito(propietario="Sergio", numero="1234567890123456", mesDeCaducidad="12", añoDeCaducidad="23", codigoDeVerificacion=123)
	tarjeta2Usuario1 = TarjetaDeCredito(propietario="Sergio", numero="2167013026479256", mesDeCaducidad="09", añoDeCaducidad="24", codigoDeVerificacion=456)

	tarjeta1Usuario2 = TarjetaDeCredito(propietario="Irene", numero="8901234561234567", mesDeCaducidad="01", añoDeCaducidad="25", codigoDeVerificacion=789)
	tarjeta2Usuario2 = TarjetaDeCredito(propietario="Irene", numero="6789012312345456", mesDeCaducidad="05", añoDeCaducidad="26", codigoDeVerificacion=327)

	usuario1 = Usuario(dni="12345678Z", nombre="Sergio", primerApellido="Martin", segundoApellido="Gomez", fechaDeNacimiento="1990-05-29", tarjetasDeCredito=[tarjeta1Usuario1.numero, tarjeta2Usuario1.numero], pedidos=[pedido1Usuario1, pedido2Usuario1])
	usuario2 = Usuario(dni="23456123X", nombre="Irene", primerApellido="Martin", fechaDeNacimiento="1992-01-28", tarjetasDeCredito=[tarjeta1Usuario2.numero, tarjeta2Usuario2.numero], pedidos=[pedido1Usuario2, pedido2Usuario2])
	
	producto1.save()
	producto2.save()
	producto3.save()
	producto4.save()

	pedido1Usuario1.save()
	pedido2Usuario1.save()

	pedido1Usuario2.save()
	pedido2Usuario2.save()

	tarjeta1Usuario1.save()
	tarjeta2Usuario1.save()

	tarjeta1Usuario2.save()
	tarjeta2Usuario2.save()

	usuario1.save()
	usuario2.save()

if __name__ == '__main__':
	insertar()
