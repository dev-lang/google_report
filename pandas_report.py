#!/usr/bin/env python3
''' importar re para exp. reg '''
import re
from operator import itemgetter
import csv #crear csv al final
import pandas as pd

archivo = "syslog.log"

''' dictionaries '''
per_usrnm = dict()
error = dict()

with open(archivo) as f:
    for l in f.readlines():
        #resultado = re.search(r"(?P<info>[A-Z]{4,5})(?P<status>[\w' ]*)(?P<codigo>[\[[#\d]*\]|\w{0})(?P<usuario>\(*.*\))", l)
        #resultado = re.search(r"(?P<info>[A-Z]{4,5})(?P<status>[\w' ]*)(?P<codigo>[\[[#\d]*\]|\w{0}) \((?P<a>(.*))\)", l)
        resultado = re.search(r"(?P<info>[A-Z]{4,5})\s(?P<status>[\w' ]*)(?P<codigo>[\[[#\d]*\]|\w{0}) \((?P<a>(.*))\)", l)
        ''' separo por grupos '''
        info = resultado[1]
        detalle = resultado[2]
        usuario = resultado [4]

        ''' lleno error por detalle y cantidad '''
        if detalle not in error.keys():
            error[detalle] = 1
        else:
            error[detalle] += 1

        ''' default values para pre-crear diccionario con keys '''
        if usuario not in per_usrnm.keys():
            per_usrnm[usuario] = {}
            per_usrnm[usuario]['INFO'] = 0
            per_usrnm[usuario]['ERROR'] = 0
        ''' values por categoria
            por ejemplo [usuario]['INFO'] '''
        per_usrnm[usuario][info] += 1

''' Listas con sorted según solicitado en examen '''
error_sorted = sorted(error.items(), key=itemgetter(1), reverse=True)
per_usrnm_sorted = sorted(per_usrnm.items(), key=itemgetter(0))

''' elimino de la memoria al archivo abierto '''
f.close()

''' presets de columnas '''
dferror = pd.DataFrame (error_sorted, columns = ['Error', 'Count'])
dfperuser = pd.DataFrame (per_usrnm_sorted, columns = ['Username', 'B'])
''' splitear columnas desde formato dict a dos con los valores solicitados
    primero dropeo y despues aplico pd.series para splitear haciendo un concatenado de ambos datos '''
dfperuser = pd.concat([dfperuser.drop(['B'], axis=1), dfperuser['B'].apply(pd.Series)], axis=1)

''' función reutilizable para poder exportar a formato csv desde pandas '''
def csvPandasWrite(dfprocesar, indice, archivosalida):
    df = dfprocesar
    df = df.set_index(indice)
    df.to_csv(archivosalida, sep=',', encoding='utf-8')

csvPandasWrite(dferror, 'Error', 'user_statistics.csv')
csvPandasWrite(dfperuser, 'Username', 'error_message.csv')
