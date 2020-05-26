from django.shortcuts import render
from gestionPeliculas.populate import populateDatabase
from gestionPeliculas.models import UserInformation, Film, Rating

# Create your views here.


def loadDict():
    Prefs={}   # matriz de usuarios y puntuaciones a cada a items
    shelf = shelve.open("dataRS.dat")
    ratings = Rating.objects.all()
    for ra in ratings:
        user = int(ra.user.id)
        itemid = int(ra.film.id)
        rating = float(ra.rating)
        Prefs.setdefault(user, {})
        Prefs[user][itemid] = rating
    shelf['Prefs']=Prefs
    shelf['ItemsPrefs']=transformPrefs(Prefs)
    shelf['SimItems']=calculateSimilarItems(Prefs, n=10)
    shelf.close()


def index(request):
    return render(request, 'index.html')


def populate(request):
    populateDatabase()
    numUsuario = str(UserInformation.objects.all().count())
    numPeliculas = str(Film.objects.all().count())
    numPuntuaciones = str(Rating.objects.all().count())
    mensaje = "Se han cargado " + numUsuario + " usuarios, " + numPeliculas + " películas y " + numPuntuaciones + " puntuaciones"
    return render(request, 'populate.html', {'mensaje': mensaje})











