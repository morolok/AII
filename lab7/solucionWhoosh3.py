#encoding:latin-1
import os
from datetime import datetime
from whoosh.index import create_in,open_dir
from whoosh.fields import Schema, TEXT, DATETIME, ID
from whoosh.qparser import QueryParser, MultifieldParser
from whoosh import qparser

#Crea un indice desde los documentos contenidos en dirdocs
#El indice lo crea en un directorio (dirindex) 
def crea_index(dirdocs,dirindex):
    if not os.path.exists(dirdocs):
        print ("Error: no existe el directorio de documentos " + dirdocs)
    else:
        if not os.path.exists(dirindex):
            os.mkdir(dirindex)
    if not len(os.listdir(dirindex))==0:
        sn=input("Indice no vacío. Desea reindexar?(s/n)")
    else:
        sn='s' 
    if sn == 's':
            ix = create_in(dirindex, schema=get_schema())
            writer = ix.writer()
            for docname in os.listdir(dirdocs):
                if not os.path.isdir(dirdocs+docname):
                    add_doc(writer, dirdocs, docname)                  
            writer.commit()
        
def apartado_a(dirindex,agenda):
    query = input("Introduzca consulta sobre asunto o contenido del correo: ")
    ix=open_dir(dirindex)   

    with ix.searcher() as searcher:
        myquery = MultifieldParser(["asunto","contenido"], ix.schema).parse(query)
        results = searcher.search(myquery)
        for r in results:
            print ("RTTE: "+agenda[r['remitente']], "   ASUNTO: "+r['asunto'])
        
def apartado_b(dirindex):
    query = input("Introduzca la fecha (AAAAMMDD): ")
    myquery='{'+ query + 'TO]'
    ix=open_dir(dirindex)   
    try:
        with ix.searcher() as searcher:
            query = QueryParser("fecha", ix.schema).parse(myquery)
            results = searcher.search(query)
            for r in results:
                print ("Fecha: "+r['fecha'].strftime('%d-%m-%Y'), "   RTTE: "+r['remitente'], "   DESTINARIOS: "+r['destinatarios'], "   ASUNTO: "+r['asunto'])
    except:
        print ("Error: Formato de fecha incorrecto")            

def apartado_c(dirindex):
    query = input("Introduzca palabras spam: ")
    ix=open_dir(dirindex)   

    with ix.searcher() as searcher:
        query = QueryParser("asunto", ix.schema,group=qparser.OrGroup).parse(query)
        results = searcher.search(query)
        for r in results:
            print ("FICHERO: "+r['nombrefichero'])
        

def get_schema():
    return Schema(remitente=TEXT(stored=True), destinatarios=TEXT(stored=True), fecha=DATETIME(stored=True), asunto=TEXT(stored=True), contenido=TEXT(stored=True), nombrefichero=ID(stored=True))


def add_doc(writer, path, docname):
    try:
        fileobj=open(path+'\\'+docname, "r")
        rte=fileobj.readline().strip()
        dtos=fileobj.readline().strip()
        f=fileobj.readline().strip()
        dat=datetime.strptime(f,'%Y%m%d')
        ast=fileobj.readline().strip()
        ctdo=fileobj.read()
        fileobj.close()           
        
        writer.add_document(remitente=rte, destinatarios=dtos, fecha=dat, asunto=ast, contenido=ctdo, nombrefichero=docname)
    
        print ("Creado indice para fichero " + docname)
    except:
        print ("Error: No se ha podido añadir el documento "+path+'\\'+docname)

def crea_agenda(dirage):
    try:
        dic={}
        fileobj=open(dirage+'\\'+"agenda.txt", "r")
        email=fileobj.readline()
        while email:
            nombre=fileobj.readline()
            dic[email.strip()]=nombre.strip()
            email=fileobj.readline()
    
        print ("Cargada agenda")
        return dic
    except:
        print ("Error: No se ha podido crear la agenda. Compruebe que existe el fichero "+dirage+'\\'+"agenda.txt")
           
def main():
    crea_index("Docs\Correos","Index")
    agenda=crea_agenda("Docs\Agenda")
    apartado_a("Index",agenda)
    apartado_b("Index")
    apartado_c("Index")


if __name__ == '__main__':
    main()