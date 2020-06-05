from django.shortcuts import render, get_object_or_404, redirect
from gestionAnimes.populate import populateDatabase
from gestionAnimes.models import Genero, Usuario, Anime, Puntuacion
import shelve
from gestionAnimes.forms import UserForm, GenreForm
from gestionAnimes.recommendations import  transformPrefs, calculateSimilarItems, getRecommendations, getRecommendedItems, topMatches


def loadDict():
    Prefs={}
    shelf = shelve.open("dataRS.dat")
    puntuaciones = Puntuacion.objects.all()
    for punt in puntuaciones:
        id_usuario = int(punt.idUsuario.id)
        id_anime = int(punt.idAnime.id)
        puntuacion = int(punt.puntuacion)
        Prefs.setdefault(id_usuario, {})
        Prefs[id_usuario][id_anime] = puntuacion
    shelf['Prefs']=Prefs
    shelf['ItemsPrefs']=transformPrefs(Prefs)
    shelf['SimItems']=calculateSimilarItems(Prefs, n=10)
    shelf.close()


# Create your views here.


def index(request):
    return render(request, 'index.html')


def populateDB(request):
    if(request.method == 'POST'):
        if 'Aceptar' in request.POST:
            populateDatabase()
            return redirect('exitoCargaDB')
        else:
            return redirect("/")
    return render(request,'populate.html')


def exitoCargaBD(request):
    numAnimes = Anime.objects.all().count()
    numPuntuaciones = Puntuacion.objects.all().count()
    mensaje = "Se han cargado " + str(numAnimes) + " animes y " + str(numPuntuaciones) + " puntuaciones."
    contexto = {'mensaje': mensaje}
    return render(request, "exitoCargaBD.html", contexto)


def cargaRS(request):
    loadDict()
    return render(request,'cargarRS.html')


def puntuacionesDeUnUsuario(request):
    if request.method=='GET':
        form = UserForm(request.GET, request.FILES)
        if form.is_valid():
            idUsuario = form.cleaned_data['id']
            puntuaciones = Puntuacion.objects.filter(idUsuario=idUsuario)
            informacion = []
            for punt in puntuaciones:
                anime, creado = Anime.objects.get_or_create(id=punt.idAnime.id)
                informacion.append((punt.idAnime, anime.titulo, punt.puntuacion))
            return render(request, 'animesPuntuados.html', {'idUsuario':idUsuario, 'informacion': informacion})
    form=UserForm()
    return render(request,'puntuacionesDeUnUsuario.html', {'form':form })


def animesPorGenero(request):
    if request.method=='GET':
        form = GenreForm(request.GET, request.FILES)
        if (form.is_valid()):
            nombre = form.cleaned_data['nombre'][0]
            todosAnimes = Anime.objects.all()
            animes = []
            for anime in todosAnimes:
                lsGeneros = []
                for gen in anime.generos.all():
                    lsGeneros.append(gen.nombre)
                if(nombre in lsGeneros):
                    animes.append(anime)
            informacion = []
            for anime in animes:
                lsGeneros = []
                for gen in anime.generos.all():
                    lsGeneros.append(gen.nombre)
                informacion.append((anime.titulo, lsGeneros, anime.formatoEmision, anime.numeroEpisodios))
            return render(request, 'animesGenero.html', {'informacion': informacion, 'genero': nombre})
    form=GenreForm()
    return render(request,'animesPorGenero.html', {'form':form })


def usuariosParecidos(request):
    if request.method=='GET':
        form = UserForm(request.GET, request.FILES)
        if form.is_valid():
            idUsuario = form.cleaned_data['id']
            usuario, creado = Usuario.objects.get_or_create(id=idUsuario)
            shelf = shelve.open("dataRS.dat")
            ItemsPrefs = shelf['ItemsPrefs']
            shelf.close()
            recommended = topMatches(ItemsPrefs, int(idUsuario),n=3)
            usuarios = []
            similar = []
            for re in recommended:
                usu, creado = Usuario.objects.get_or_create(id=re[1])
                usuarios.append(usu)
                similar.append(re[0])
            items= zip(usuarios,similar)
            return render(request, 'usuariosSimilares.html', {'usuario': usuario, 'usuarios': items})
    form=UserForm()
    return render(request, 'usuariosParecidos.html', {'form':form })


def recomendarAnimes(request):
    if request.method=='GET':
        form = UserForm(request.GET, request.FILES)
        if form.is_valid():
            idUsuario = form.cleaned_data['id']
            usuario, creado = Usuario.objects.get_or_create(id=idUsuario)
            shelf = shelve.open("dataRS.dat")
            Prefs = shelf['Prefs']
            SimItems = shelf['SimItems']
            shelf.close()
            rankings = getRecommendedItems(Prefs, SimItems, int(idUsuario))
            recommended = rankings[:5]
            animes = []
            scores = []
            for re in recommended:
                animes.append(Anime.objects.get(id=re[1]))
                scores.append(re[0])
            items= zip(animes,scores)
            return render(request,'animesRecomendados.html', {'usuario': usuario, 'items': items})
    form=UserForm()
    return render(request, 'recomendarAnimes.html', {'form': form})



