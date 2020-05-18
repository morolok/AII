from gestionPeliculas.models import Occupation, UserInformation, Film, Rating
from datetime import datetime

path = "ml-100k"

def deleteTables():
    Rating.objects.all().delete()
    Film.objects.all().delete()
    UserInformation.objects.all().delete()
    Occupation.objects.all().delete()  
  
    
def populateOccupations():
    print("Loading occupations...")
        
    lista=[]
    fileobj=open(path+"\\u.occupation", "r")
    for line in fileobj.readlines():
        lista.append(Occupation(occupationName=str(line.strip())))
    fileobj.close()
    Occupation.objects.bulk_create(lista)  # bulk_create hace la carga masiva para acelerar el proceso
    
    print("Occupations inserted: " + str(Occupation.objects.count()))
    print("---------------------------------------------------------")


def populateUsers():
    print("Loading users...")
       
    lista=[]
    dict={}
    fileobj=open(path+"\\u.user", "r")
    for line in fileobj.readlines():
        rip = line.split('|')
        if len(rip) != 5:
            continue
        id_u=int(rip[0].strip())
        u=UserInformation(id=id_u, age=rip[1].strip(), gender=rip[2].strip(), occupation=Occupation.objects.get(occupationName=rip[3].strip()), zipCode=rip[4].strip())
        lista.append(u)
        dict[id_u]=u
    fileobj.close()
    UserInformation.objects.bulk_create(lista)
    
    print("Users inserted: " + str(UserInformation.objects.count()))
    print("---------------------------------------------------------")
    return(dict)


def populateFilms():
    print("Loading movies...")
       
    lista_peliculas =[]  # lista de peliculas
    dict={}
    fileobj=open(path+"\\u.item", "r")
    for line in fileobj.readlines():
        rip = line.split('|')
        try:
            date_rel = datetime.strptime(rip[2].strip(),'%d-%b-%Y')
        except:
            date_rel = datetime.strptime('01-Jan-1990','%d-%b-%Y')
        try:
            date_rel_video = datetime.strptime(rip[3].strip(),'%d-%b-%Y')
        except:
            date_rel_video = date_rel
        id_pe = int(rip[0].strip())
        f = Film(id=id_pe, movieTitle=rip[1].strip(), releaseDate=date_rel, releaseVideoDate=date_rel_video , IMDbURL=rip[4].strip())
        lista_peliculas.append(f)
        dict[id_pe] = f      
    fileobj.close()    
    Film.objects.bulk_create(lista_peliculas)
    
    print("Movies inserted: " + str(Film.objects.count()))
    print("---------------------------------------------------------")
    return(dict)
       
def populateRatings(u,m):
    print("Loading ratings...")
    Rating.objects.all().delete()

    lista=[]
    fileobj=open(path+"\\u.data", "r")
    for line in fileobj.readlines():
        rip = line.split('\t')
        lista.append(Rating(user=u[int(rip[0].strip())], film=m[int(rip[1].strip())], rating=int(rip[2].strip()), rateDate= datetime.fromtimestamp(int(rip[3].strip())) ))
    fileobj.close()
    Rating.objects.bulk_create(lista)
    print("Ratings inserted: " + str(Rating.objects.count()))
    print("---------------------------------------------------------")
    
    
def populateDatabase():
    deleteTables()
    populateOccupations()
    u=populateUsers()
    m=populateFilms()
    populateRatings(u,m)
    print("Finished database population")
    
if __name__ == '__main__':
    populateDatabase()