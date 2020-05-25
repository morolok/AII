from gestionLibros.models import Usuario, Libro, Puntuacion

path = "BX-Book-dataset"


def deleteTables():
    Libro.objects.all().delete()
    Puntuacion.objects.all().delete()


def populateLibros():
    print("Cargando libros...")

    lista=[]
    fileobj=open(path+"\\books.csv", "r")
    fileobj.readline()
    for line in fileobj.readlines():
        campos = line.split(';')
        isbn_libro = int(campos[0].strip())
        l = Libro(isbn=isbn_libro, titulo=campos[1].strip(), autor=campos[2].strip(), añoPublicacion=campos[3].strip(), editor=campos[4].strip())
        lista.append(l)
    fileobj.close()
    Libro.objects.bulk_create(lista)
    
    print("Libros insertados: " + str(Libro.objects.count()))
    print("---------------------------------------------------------")


def populatePuntuacion():
    print("Cargando puntuaciones...")
    Puntuacion.objects.all().delete()

    lista=[]
    fileobj=open(path+"\\ratings.csv", "r")
    fileobj.readline()
    for line in fileobj.readlines():
        campos = line.split(';')
        usuario, creado = Usuario.objects.get_or_create(id=int(campos[0].strip()))
        libro, creado = Libro.objects.get_or_create(isbn=int(campos[1].strip()))
        p = Puntuacion(idUsuario=usuario, isbn=libro, puntuacion=int(campos[2].strip()))
        lista.append(p)
    fileobj.close()
    Puntuacion.objects.bulk_create(lista)

    print("Puntuaciones insertadas: " + str(Puntuacion.objects.count()))
    print("---------------------------------------------------------")


def populateDatabase():
    deleteTables()
    populateLibros()
    populatePuntuacion()
    print("Finalizada la carga de la base de datos")


