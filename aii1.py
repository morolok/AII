def CadenasCaracteres():

	def insertar(cadena, caracter):
		res = ""
		tam = len(cadena)
		for i in cadena:
			if (tam == 1):
				res +=i
			else:
				res += i + caracter
			tam -= 1
		return res

	def reemplazar(cadena, caracter):
		res = cadena.replace(" ", caracter)
		return res

	def reemplazarNumero(cadena, caracter):
		res = ""
		for i in cadena:
			if (i.isnumeric()):
				res += caracter
			else:
				res += i
		return res

	def insertar2(cadena, caracter):
		res = ""
		cont = 1
		for i in cadena:
			if (cont == 3):
				res += i + caracter
				cont = 1
			else:
				res += i
				cont += 1
		return res

	ej1a = insertar("separar",",")
	ej1b = reemplazar("mi archivo de texto.txt", "_")
	ej1c = reemplazarNumero("su clave es: 1540", "X")
	ej1d = insertar2("2552552550", ".")

	print(ej1a)
	print(ej1b)
	print(ej1c)
	print(ej1d)

def TuplasYListas():

	def imprimirMensajes(ls):
		for i in ls:
			if (i[1] == "Hombre"):
				print("Estimado " + i[0] + ", vote por mi.")
			else:
				print("Estimada " + i[0] + ", vote por mi.")

	def imprimirMensajes2(ls, py, n):
		for i in range(py, len(ls)):
			if (n == 0):
				break
			else:
				if (ls[i][1] == "Hombre"):
					print("Estimado " + ls[i][0] + ", vote por mi.")
				else:
					print("Estimada " + ls[i][0] + ", vote por mi.")
			n -= 1
	
	def imprimirNombre(ls):
		res = []
		for i in ls:
			aux = i[1] + " " + i[2] + ". " + i[0]
			res.append(aux)
		return res


	ls = [("Marta","Mujer"),("Carlos","Hombre"),("Eugenia","Mujer"),("Guillén","Hombre"),("Nefasto","Hombre"),("Ale","Hombre"),("Acuña","Hombre")]
	ls2 = [("Mata", "José", "F"), ("Contreras", "Miguel", "Á"), ("Salas", "María", "I"), ("Moreno", "María", "R")]
	imprimirMensajes(ls)
	imprimirMensajes2(ls,1,3)
	ej2 = imprimirNombre(ls2)
	print(ej2)

def Busqueda():

	def buscar(cadena, ls):
		res = []
		for i in ls:
			if (cadena in i[0]):
				res.append(i)
		return res

	ls = [("Carlos Mata Blasco","648840277"), ("Miguel Pérez Hernández","678036511"), ("Ángel Martínez Pérez","634900923"), 
		("Luis Guerrero Herrero","654876012"), ("Antonio Salas Martín","654390255")]
	ej1 = buscar("Pérez", ls)
	print(ej1)

def Diccionarios():

	def buscar(agenda):
		nombre = input("Nombre que desea buscar: ")
		if (nombre in agenda):
			tel = agenda[nombre]
			print("Teléfono de " + nombre + ": " + tel)
			cad = input("Si el telefono no es el correcto introduzca el nuevo telefono, en caso contraio escriba *\n")
			if (cad != "*"):
				agenda[nombre] = cad
				print("Telefono cambiado a: " + agenda[nombre])
		else:
			tel = input("El nombre no ha sido encontrado, inserte el telefono para buscar al contacto por el telefono: ")
			nom = None
			for c,v in agenda.items():
				if(tel == v):
					nom = c
					break
			print("El telefono " + tel + " corresponde a " + nom)
			cad = input("Si el telefono no es el correcto introduzca el nuevo telefono, en caso contraio escriba *\n")
			if(cad != "*"):
				agenda[nom] = cad
				print("Telefono cambiado a: " + agenda[nom])

		#print("Nombre a buscar: " + nombre)

	agenda = {"Carlos": "648840277", "Miguel": "678036511", "Ángel": "634900923", "Luis": "654876012", "Antonio": "654390255"}
	buscar(agenda)


class Corcho():

	def __init__(self, bodega):
		self.bodega = bodega

class Botella():

	def __init__(self, corcho):
		self.corcho = corcho

class Sacacorchos():

	def destapar(self, Botella):
		self.corcho = Botella.corcho
		Botella.corcho = None

	def limpiar(self):
		self.corcho = None

class Personaje():

	def __init__(self, vida, posicion, velocidad):
		self.vida = vida
		self.posicion = posicion
		self.velocidad = velocidad

	def recibir_ataque(self, daño):
		self.vida = self.vida - daño
		if (self.vida <= 0):
			print("Vida restante tras el ataque menor o igual que 0.")

	def mover(self):
		self.posicion = self.posicion + self.velocidad

class Soldado(Personaje):

	def __init__(self, ataque):
		self.ataque = ataque

	def atacar(self, personaje):
		personaje.recibir_ataque(self.ataque)

class Campesino(Personaje):

	def __init__(self, cosecha):
		self.cosecha = cosecha

	def cosechar(self):
		return self.cosecha

#CadenasCaracteres()
#TuplasYListas()
#Busqueda()
#Diccionarios()