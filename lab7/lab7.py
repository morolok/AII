import os
from datetime import datetime
from whoosh.index import create_in,open_dir
from whoosh.fields import Schema, TEXT, DATETIME, ID
from whoosh.qparser import QueryParser, MultifieldParser
from whoosh import qparser

dircorreos = "Correos"
diragenda = "Agenda"
dirindex = "Index"

def get_schema():
    return Schema(remitente=TEXT(stored=True), destinatarios=TEXT(stored=True), fecha=DATETIME(stored=True), asunto=TEXT(stored=True), 
        cuerpo=TEXT(stored=True), nombreFichero=ID(stored=True))

def add_doc(writer, directorio, documento):
    try:
        fichero = open(directorio + '\\' + documento, "r")
        remitente = fichero.readline().strip()
        destinatarios = fichero.readline().strip()
        fecha = fichero.readline().strip()
        fechaFormateada = datetime.strptime(fecha, '%Y%m%d')
        asunto = fichero.readline().strip()
        cuerpo = fichero.readline().strip()
        fichero.close()
        writer.add_document(remitente=remitente, destinatarios=destinatarios, fecha=fechaFormateada, asunto=asunto, cuerpo=cuerpo,
            nombreFichero=documento)
        print(documento + " procesado con éxito")
    except:
        print("Error con el documento " + documento + " en el método add_doc")

def crear_index():
    if not os.path.exists(dirindex):
        os.mkdir(dirindex)
    index = create_in(dirindex, schema=get_schema())
    writer = index.writer()
    for documento in os.listdir(dircorreos):
        add_doc(writer, dircorreos, documento)
    writer.commit()

def crear_agenda():
    try:
        agenda = open(diragenda + '\\' + "agenda.txt", "r")
        contactos = {}
        lineas = agenda.readlines()
        while lineas:
            correo = lineas.pop(0).replace("\n", "")
            persona = lineas.pop(0).replace("\n", "")
            contactos[correo] = persona
        print("Agenda cargada con éxito")
        return contactos
    except:
        print("Error al cargar la agenda")

def apartado_a():
    consulta = input("Introduzca consulta sobre asunto o contenido del correo: ")
    index = open_dir(dirindex)
    res = ""
    with index.searcher() as searcher:
        query = MultifieldParser(["asunto", "cuerpo"], index.schema).parse(consulta)
        correos = searcher.search(query, terms=True)
        for c in correos:
            remitente = c['remitente']
            asunto = c['asunto']
            persona = agenda[remitente]
            res += "\nRemitente: " + persona + "\n" + "Asunto: " + asunto + "\n"
    print(res)

def apartado_b():
    consulta = input("Introduzca la fecha (AñoMesDía): ")
    consulta2 = '{'+ consulta + 'TO]'
    index = open_dir(dirindex)
    res = ""
    try:
        with index.searcher() as searcher:
            query = QueryParser("fecha", index.schema).parse(consulta2)
            correos = searcher.search(query)
            for c in correos:
                remitente = c['remitente']
                destinatarios = c['destinatarios']
                asunto = c['asunto']
                fecha = c['fecha'].strftime('%d-%m-%Y')
                res += "\nFecha: " + fecha + "\n" + "Remitente: " + remitente + "\n" + "Destinatarios: " + destinatarios + "Asunto: " + asunto + "\n"
        print(res)
    except:
        print("Fecha mal introducida")

def apartado_c():
    consulta = input("Introduzca la palabra de spam: ")
    index = open_dir(dirindex)
    res = ""
    with index.searcher() as searcher:
        query = QueryParser("asunto", index.schema).parse(consulta)
        #query = QueryParser("asunto", index.schema, group=qparser.OrGroup).parse(consulta)
        correos = searcher.search(query, terms=True)
        for c in correos:
            nombreFichero = c['nombreFichero']
            res += "\n" + "Nombre del fichero: " + nombreFichero + "\n"
    print(res)
    

print("\n========== Método crear_index ==========\n")
crear_index()

print("\n========== Método crear_agenda ==========\n")
agenda = crear_agenda()
print(agenda)

print("\n========== Método apartado_a ==========\n")
#apartado_a()

print("\n========== Método apartado_b ==========\n")
#apartado_b()

print("\n========== Método apartado_c ==========\n")
#apartado_c()