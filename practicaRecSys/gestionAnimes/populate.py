from gestionAnimes.models import Genero, Usuario, Anime, Puntuacion

path = "animeRS_Dataset"

def deleteTables():
    Genero.objects.all().delete()
    Puntuacion.objects.all().delete()
    Anime.objects.all().delete()
    Usuario.objects.all().delete()


def populateAnime():
    print("Cargando animes...")
    dicc = {}
    fileobj=open(path+"\\anime.csv", "r", encoding="utf-8")
    fileobj.readline()
    for line in fileobj.readlines():
        campos = line.split(";")
        idAnime = int(campos[0].strip())
        titulo = campos[1].strip()
        lsGeneros = campos[2].strip().split(",")
        formatoEmision = campos[3].strip()
        if(campos[4].strip() == 'Unknown'):
            numeroEpisodios = 0
        else:
            numeroEpisodios = int(campos[4].strip())
        anime = Anime.objects.create(id=idAnime, titulo=titulo, formatoEmision=formatoEmision, numeroEpisodios=numeroEpisodios)
        lsAux = []
        for genero in lsGeneros:
            gen, creado = Genero.objects.get_or_create(nombre=genero.strip())
            lsAux.append(gen)
        for genero in lsAux:
            anime.generos.add(genero)
        dicc[idAnime]=anime
    fileobj.close()
    print("Animes insertados: " + str(Anime.objects.count()))
    print("---------------------------------------------------------")
    return(dicc)


def populatePuntuacion(dAnimes):
    print("Cargando puntuaciones...")
    lista = []
    fileobj=open(path+"\\ratings.csv", "r", encoding="utf-8")
    fileobj.readline()
    for line in fileobj.readlines():
        campos = line.split(";")
        idUsuario = int(campos[0].strip())
        idAnime = int(campos[1].strip())
        punt = int(campos[2].strip())
        usuario, creado = Usuario.objects.get_or_create(id=idUsuario)
        anime = dAnimes[idAnime]
        p = Puntuacion(idUsuario=usuario, idAnime=anime, puntuacion=punt)
        lista.append(p)
    fileobj.close()
    Puntuacion.objects.bulk_create(lista)
    print("Puntuaciones insertadas: " + str(Puntuacion.objects.count()))
    print("---------------------------------------------------------")


def populateDatabase():
    deleteTables()
    dAnimes = populateAnime()
    populatePuntuacion(dAnimes)
    print("Población de la base de datos finalizada")