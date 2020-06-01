from gestionArtistas.models import Usuario, Artista, Etiqueta, UsuarioArtista, UsuarioEtiquetaArtista

path = "hetrec2011-lastfm-2k"

def deleteTables():
    Usuario.objects.all().delete()
    Artista.objects.all().delete()
    Etiqueta.objects.all().delete()
    UsuarioArtista.objects.all().delete()
    UsuarioEtiquetaArtista.objects.all().delete()


def populateArtista():
    print("Cargando artistas...")
    lista=[]
    fileobj=open(path+"\\artists.dat", "r", encoding="utf-8")
    fileobj.readline()
    for linea in fileobj.readlines():
        campos = linea.split("\t")
        idArtista = int(campos[0].strip())
        nombre = campos[1].strip()
        url = campos[2].strip()
        pictureUrl = campos[3].strip()
        artista = Artista(id=idArtista, nombre=nombre, url=url, pictureUrl=pictureUrl)
        lista.append(artista)
    fileobj.close()
    Artista.objects.bulk_create(lista)
    print("Artistas creados: " + str(Artista.objects.count()))
    print("---------------------------------------------------------")


def populateEtiqueta():
    print("Cargando etiquetas...")
    lista=[]
    fileobj=open(path+"\\tags.dat", "r", encoding="utf-8")
    fileobj.readline()
    for linea in fileobj.readlines():
        campos = linea.split("\t")
        idEtiqueta = int(campos[0].strip())
        tagValue = campos[1].strip()
        etiqueta = Etiqueta(id=idEtiqueta, tagValue=tagValue)
        lista.append(etiqueta)
    fileobj.close()
    Etiqueta.objects.bulk_create(lista)
    print("Etiquetas creadas: " + str(Etiqueta.objects.count()))
    print("---------------------------------------------------------")


def populateUsuarioArtista():
    print("Cargando usuario artista...")
    lista=[]
    fileobj=open(path+"\\user_artists.dat", "r", encoding="utf-8")
    fileobj.readline()
    for linea in fileobj.readlines():
        campos = linea.split("\t")
        idUsuario = int(campos[0].strip())
        idArtista = int(campos[1].strip())
        tiempoEscucha = int(campos[2].strip())
        usuario, creado = Usuario.objects.get_or_create(id=idUsuario)
        artista, creado = Artista.objects.get_or_create(id=idArtista)
        usuarioArtista = UsuarioArtista(idUsuario=idUsuario, idArtista=idArtista, tiempoEscucha=tiempoEscucha)
        lista.append(usuarioArtista)
    fileobj.close()
    UsuarioArtista.objects.bulk_create(lista)
    print("Usuario artistas creados: " + str(UsuarioArtista.objects.count()))
    print("---------------------------------------------------------")
