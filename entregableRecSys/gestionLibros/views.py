import shelve
from gestionLibros.models import Libro, Puntuacion
from gestionLibros.forms import FormularioUsuario, FormularioLibro
from django.shortcuts import render, get_object_or_404, redirect
from gestionLibros.recommendations import  transformPrefs, getRecommendations, topMatches, calculateSimilarItems
from gestionLibros.populate import populateDatabase


# Create your views here.


def loadDict():
    Prefs={}
    shelf = shelve.open("dataRS.dat")
    puntuaciones = Puntuacion.objects.all()
    for punt in puntuaciones:
        id_usuario = int(punt.idUsuario.id)
        isbn_libro = int(punt.isbn.isbn)
        #libro = Libro.objects.filter(isbn=isbn_libro)
        puntuacion = int(punt.puntuacion)
        Prefs.setdefault(id_usuario, {})
        Prefs[id_usuario][isbn_libro] = puntuacion
    shelf['Prefs']=Prefs
    shelf['ItemsPrefs']=transformPrefs(Prefs)
    shelf['SimItems']=calculateSimilarItems(Prefs, n=10)
    shelf.close()


def index(request): 
    return render(request,'index.html')


def populateDB(request):
    if(request.method == 'POST'):
        if 'Aceptar' in request.POST:
            populateDatabase()
            return redirect('exitoCargaDB')
        else:
            return redirect("/")
    return render(request,'populate.html')


def exitoCargaBD(request):
    numLibros = Libro.objects.all().count()
    numPuntuaciones = Puntuacion.objects.all().count()
    mensaje = "Se han cargado " + str(numLibros) + " libros y " + str(numPuntuaciones) + " puntuaciones."
    contexto = {'mensaje': mensaje}
    return render(request, "exitoCargaBD.html", contexto)


def cargaRS(request):
    loadDict()
    return render(request,'cargarRS.html')


def puntuacionesDeUnUsuario(request):
    if request.method=='GET':
        form = FormularioUsuario(request.GET, request.FILES)
        if form.is_valid():
            idUsuario = form.cleaned_data['id']
            puntuaciones = Puntuacion.objects.filter(idUsuario=idUsuario)
            informacion = []
            for punt in puntuaciones:
                l, creado = Libro.objects.get_or_create(isbn=punt.isbn.isbn)
                informacion.append((punt.isbn, l.titulo, punt.puntuacion))
            return render(request, 'librosPuntuados.html', {'idUsuario':idUsuario, 'informacion': informacion})
    form=FormularioUsuario()
    return render(request,'puntuacionesDeUnUsuario.html', {'form':form })


def mejoresLibros(request):
    puntuaciones = Puntuacion.objects.filter()
    isbnPuntuaciones = {}
    for punt in puntuaciones:
        isbnLibro = punt.isbn
        if(isbnLibro not in isbnPuntuaciones.keys()):
            ls = []
            ls.append(punt.puntuacion)
            isbnPuntuaciones[isbnLibro] = ls
        else:
            ls = isbnPuntuaciones[isbnLibro]
            ls.append(punt.puntuacion)
            isbnPuntuaciones[isbnLibro] = ls
    informacion = []
    for isbn, lsPuntuaciones in isbnPuntuaciones.items():
        l, creado = Libro.objects.get_or_create(isbn=isbn.isbn)
        puntuacionMedia = (sum(lsPuntuaciones))/(len(lsPuntuaciones))
        informacion.append((isbn, l.titulo, l.autor, puntuacionMedia))
    res = []
    for _ in range(0,3):
        puntuacionMediaPivote = 0.0
        tupla = ()
        for info in informacion:
            if(info[3] > puntuacionMediaPivote):
                tupla = info
                puntuacionMediaPivote = info[3]
        informacion.remove(tupla)
        res.append(tupla)
    
    return render(request, 'mejoresLibros.html', {'res': res})


def buscarLibros(request):
    libro = None
    if request.method=='GET':
        form = FormularioLibro(request.GET, request.FILES)
        if form.is_valid():
            isbnLibro = form.cleaned_data['isbn']
            libro, creado = Libro.objects.get_or_create(isbn=isbnLibro)
            shelf = shelve.open("dataRS.dat")
            ItemsPrefs = shelf['ItemsPrefs']
            shelf.close()
            recommended = topMatches(ItemsPrefs, int(isbnLibro),n=5)
            libros = []
            similar = []
            for re in recommended:
                lib, creado = Libro.objects.get_or_create(isbn=re[1])
                libros.append(lib)
                similar.append(re[0])
            items= zip(libros,similar)
            return render(request,'librosSimilares.html', {'libro': libro, 'libros': items})
    form = FormularioLibro()
    return render(request, 'buscarLibros.html', {'form': form})


def recomendarLibroUsuario(request):
    if request.method=='GET':
        form = FormularioUsuario(request.GET, request.FILES)
        if form.is_valid():
            idUsuario = form.cleaned_data['id']
            shelf = shelve.open("dataRS.dat")
            Prefs = shelf['Prefs']
            shelf.close()
            rankings = getRecommendations(Prefs,int(idUsuario))
            recommended = rankings[:10]
            libros = []
            scores = []
            for re in recommended:
                lib, creado = Libro.objects.get_or_create(isbn=re[1])
                libros.append(lib)
                scores.append(re[0])
            items= zip(libros,scores)
            return render(request,'librosRecomendados.html', {'idUsuario': idUsuario, 'items': items})
    form = FormularioUsuario()
    return render(request, 'recomendarLibroUsuario.html', {'form': form})