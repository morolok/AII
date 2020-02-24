class Cadena:

    def __init__(self):
        print (self.e1_a('1234567',','))
        print (self.e1_b('mi archivo de texto.txt'))
        print (self.e1_c('Su clave es: 1540'))
        print (self.e1_d('2552552550'))
        print (self.e2_a('subcadena','cadena'))
        print (self.e2_b('kde','Gnome'))
    
    def e1_a(self,s,c):
    	return ",".join(list(s))

    def e1_b(self,s):
    	return s.replace(' ','_')

    def e1_c(self,s):
    	translation_table = str.maketrans('0123456789', 'XXXXXXXXXX')
    	return s.translate(translation_table)

    def e1_d(self,s):
    	l=[]
    	i=0
    	for x in s:
    		l.append(x)
    		i += 1
    		if i == 3:
    			l.append('.')
    			i=0
    	return "".join(l)

    def e2_a(self,s1,s2):
    	return s2 in s1

    def e2_b(self,s1,s2):
    	return s1 if s1.lower() < s2.lower() else s2

class Lista:
	
	def __init__(self):
		self.e1_a(('Luis','Marta','Paula'))
		self.e1_b(('Luis','Marta','Paula','Luis'),1,2)
		self.e1_c((('Luis','h'),('Marta','m'),('Paula','m')))
		self.e2_a((('García','Luis','M'),('Carrillo','Marta','J'),('Fernández','Paula','M')))

	def e1_a(self,t):
		for e in t:
			print ("Estimado/a",e,"vote por mi")

	def e1_b(self,t,p,n):
		t1 = t[p:p+n]
		self.e1_a(t1)

	def e1_c(self,t):
		for e in t:
			print ("Estimado" if e[1]=='h' else "Estimada", e[0] ,"vote por mi")
	
	def e2_a(self,t):
		for e in t:
			print (e[1],e[2],'.',e[0])

class Busqueda:

	def __init__(self):
		self.e1_a((('Jorge García','12345'),('Luisa Montero','54321'),('Inés Roca Díaz','67890')),'García')

	def e1_a(self,t,s):
		for e in t:
			if s in e[0]:
				print ('Nombre:',e[0])
				print ('Teléfono:',e[1])

class Diccionario:

	def __init__(self):
		self.e1_a({'Jorge':'12345','Luisa':'54321','Marta':'67890'})

	def e1_a(self,d):
		while True:
			nombre = input('Introduzca nombre: ')
			if nombre == '*':
				break
			if nombre in d:
				print ('Teléfono', d[nombre])
				respuesta = input('Es correcto(s/n)? ')
				if respuesta == 'n':
					numero = input('Introduzca el nuevo número ')
					d[nombre] = numero
				else:
					numero = input('Introduzca un teléfono para el nuevo nombre')
					d[nombre] = numero
		print (d)

class Corcho:

	def __init__(self,nombre):
		self.bodega = nombre

class Botella:
	
	def __init__(self,corcho):
		self.corcho=corcho
		print ('Botella de la bodega',corcho.bodega)

class Sacacorcho:
	
	def __init__(self):
		self.corcho=None
	
	def destapar(self,botella):
		print ('descorchar')
		self.corcho=botella.corcho
		botella.corcho=None

	def limpiar(self):
		self.corcho=None
		print ('limpiar')

class Objeto:

	def __init__(self):
		corcho=Corcho('Yllera')
		botella=Botella(corcho)
		sacacorcho=Sacacorcho()
		sacacorcho.destapar(botella)
		sacacorcho.limpiar()

class Personaje:

	def __init__(self):
		self.vida=100
		self.posicion={"Norte":0,"Sur":0,"Este":0,"Oeste":0} # Diccionario con la coordenadas [Norte, Sur, Este, Oeste]
		self.velocidad=10

	def recibir_ataque(self,fuerza):
		self.vida = self.vida - fuerza
		if self.vida <= 0:
			print ("Te has quedado sin vida")
		else:
			print ("Te queda", self.vida, "vida")

	def mover(self, direccion):
		self.posicion[direccion] = self.posicion[direccion]+self.velocidad

class Soldado(Personaje):
	
	def __init__(self):
		Personaje.__init__(self)
		self.ataque = 10
	
	def atacar(self, personaje):
		personaje.recibir_ataque(self.ataque)

class Campesino(Personaje):
	
	def __init__(self):
		Personaje.__init__(self)
		self.cosecha = 10
	
	def cosechar(self):
		return self.cosecha

class Herencia:
	
	def __init__(self):
		soldado=Soldado()
		campesino=Campesino()
		soldado.atacar(campesino)
		soldado.atacar(campesino)
		print (campesino.cosechar())

if __name__ == "__main__":
	cadena = Cadena()
	lista = Lista()
	busqueda = Busqueda()
	diccionario=Diccionario()
	objeto=Objeto()
	herencia=Herencia()