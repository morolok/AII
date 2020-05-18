import shelve
from gestionPeliculas.models import UserInformation, Film, Rating
from gestionPeliculas.forms import UserForm, FilmForm
from django.shortcuts import render, get_object_or_404
from gestionPeliculas.recommendations import  transformPrefs, getRecommendations, topMatches
from gestionPeliculas.populate import populateDatabase


# Create your views here.


# Funcion que carga en el diccionario Prefs todas las puntuaciones de usuarios a peliculas. Tambien carga el diccionario inverso
# Serializa los resultados en dataRS.dat
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
    shelf.close()

    
#  CONJUNTO DE VISTAS

def index(request): 
    return render(request,'index.html')

def populateDB(request):
    populateDatabase() 
    return render(request,'populate.html')

def loadRS(request):
    loadDict()
    return render(request,'loadRS.html')
 
# APARTADO A
def recommendedFilmsUser(request):
    if request.method=='GET':
        form = UserForm(request.GET, request.FILES)
        if form.is_valid():
            idUser = form.cleaned_data['id']
            user = get_object_or_404(UserInformation, pk=idUser)
            shelf = shelve.open("dataRS.dat")
            Prefs = shelf['Prefs']
            shelf.close()
            rankings = getRecommendations(Prefs,int(idUser))
            recommended = rankings[:2]
            films = []
            scores = []
            for re in recommended:
                films.append(Film.objects.get(pk=re[1]))
                scores.append(re[0])
            items= zip(films,scores)
            return render(request,'recommendationItems.html', {'user': user, 'items': items})
    form = UserForm()
    return render(request,'search_user.html', {'form': form})


# APARTADO B
def similarFilms(request):
    film = None
    if request.method=='GET':
        form = FilmForm(request.GET, request.FILES)
        if form.is_valid():
            idFilm = form.cleaned_data['id']
            film = get_object_or_404(Film, pk=idFilm)
            shelf = shelve.open("dataRS.dat")
            ItemsPrefs = shelf['ItemsPrefs']
            shelf.close()
            recommended = topMatches(ItemsPrefs, int(idFilm),n=3)
            films = []
            similar = []
            for re in recommended:
                films.append(Film.objects.get(pk=re[1]))
                similar.append(re[0])
            items= zip(films,similar)
            return render(request,'similarFilms.html', {'film': film,'films': items})
    form = FilmForm()
    return render(request,'search_film.html', {'form': form})

#APARTADO C
def search(request):
    if request.method=='GET':
        form = UserForm(request.GET, request.FILES)
        if form.is_valid():
            idUser = form.cleaned_data['id']
            user = get_object_or_404(UserInformation, pk=idUser)
            return render(request,'ratedFilms.html', {'usuario':user})
    form=UserForm()
    return render(request,'search_user.html', {'form':form })
