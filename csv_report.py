#!/usr/bin/env python3

# importar re para exp. reg
import re
from operator import itemgetter
import csv #crear csv al final

archivo = "syslog.log"

# dictionaries
per_usrnm = dict()
error = dict()

with open(archivo) as f:
    for l in f.readlines():
        resultado = re.search(r"(?P<info>[A-Z]{4,5})\s(?P<status>[\w' ]*)(?P<codigo>[\[[#\d]*\]|\w{0}) \((?P<a>(.*))\)", l)
        # separo por grupos
        info, detalle, usuario = resultado.group(1), resultado.group(2), resultado.group(4)

        # lleno error por detalle y cantidad
        if detalle not in error.keys():
            error[detalle] = 1
        else:
            error[detalle] += 1
            

        # default values para pre-crear diccionario con keys
        if usuario not in per_usrnm.keys():
            per_usrnm[usuario] = {}
            per_usrnm[usuario]['INFO'] = 0
            per_usrnm[usuario]['ERROR'] = 0
        #values por categoria
        #    por ejemplo [usuario]['INFO']   
        per_usrnm[usuario][info] += 1

        
#Listas con sorted según solicitado en examen

error_sorted = sorted(error.items(), key=itemgetter(1), reverse=True)

per_usrnm_sorted = sorted(per_usrnm.items(), key=itemgetter(0))

#elimino de la memoria al archivo abierto
f.close()

#presets de columnas

error_sorted.insert(0, ('Error', 'Count'))
userheader = ['Username', 'INFO', 'ERROR']

#print("error_sorted", type(error_sorted))
#print("per_usrnm_sorted", type(per_usrnm_sorted))

errorred = {}
userred = {}

for e, c in error_sorted:
    errorred[e] = c

for u, i in per_usrnm_sorted:
    userred[u] = i

#print(type(errorred),"\n", errorred)
#print(type(userred),"\n", userred)

userlist = list()
infolist = list()
errorlist = list()

for i, e in userred.items():
    for key in e:
        userlist.append(i)
        if key == 'ERROR':
            errorlist.append(e[key])
        if key == 'INFO':
            infolist.append(e[key])

# delete duplicated items in userlist       
userlista = []

for us in userlist:
    if us not in userlista:
        userlista.append(us)
            
userlistaf = dict((z[0], list(z[1:])) for z in zip(userlista, infolist, errorlist))

with open('user_statistics.csv', 'w', encoding='UTF-8', newline='') as ucsv:
    writer = csv.writer(ucsv)
    
    for key, value in userlistaf.items():
        writer.writerow([key, value])
        
# workaround

datan = ""

with open('user_statistics.csv') as ag:
    datan = ag.read().replace('"[','').replace(']"','').replace(' ','')

with open('user_statistics.csv', 'w') as ag:
    ag.write(datan)
    
# añadir header userheader a user_statistics.csv

with open('user_statistics.csv',newline='') as f:
    r = csv.reader(f)
    datax = [line for line in r]
with open('user_statistics.csv','w',newline='') as f:
    w = csv.writer(f)
    w.writerow(userheader)
    w.writerows(datax)

def csvCSVWrite(): # OK para errores
    with open('error_message.csv', 'w', encoding='UTF-8', newline='') as ecsv:
        writer = csv.writer(ecsv)
        for key, value in errorred.items():
            writer.writerow([key, value])

csvCSVWrite()
