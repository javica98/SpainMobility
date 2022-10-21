#!/usr/bin/env python
# coding: utf-8

# In[81]:


import pandas as pd
import copy
import csv
from string import digits
from datetime import datetime,timedelta,date
import re
import unicodedata


# In[ ]:


#Unir Archivos
#Input: Dataframe
def unificacion(listaArchivos):
    csv = pd.concat(listaArchivos)
    return csv


# In[ ]:


#Formateo de las fechas
#Input: Dataframe
def formateoFecha(archivo):
    for index, row in archivo.iterrows():
        prueba = row['Fecha']
        partes = re.split('/|-',prueba)
        mes = partes[1]
        if int(partes[0])>2000:
            año = partes[0]
            dia = partes[2]
        else:
            dia = partes[0]
            año = partes[2]
        archivo['Fecha'][index]= año + '-' + mes + '-' + dia
    return archivo


# In[88]:


#Elimina las variables introducidas.
#Input: Dataframe,lista de string con nombres de las variables a eliminar

def eliminacionVariables(archivo,listaVariables,):
    archivo=archivo.drop(listaVariables, axis=1)
    return archivo


# In[ ]:


#Agrupar por variables
#Input: Dataframe,lista de los nombres string de las variables que quieres unir (Fecha y Municipio)
def grouping(archivo,listaVariables):
    archivo = archivo.groupby(by = listaVariables).sum()
    archivo =archivo.reset_index()
    return (archivo)


# In[83]:


#Formateo del nombre del municipio
#Input: Dataframe
def formateoMunicipios(archivo):
    for index, row in archivo.iterrows():
        prueba = row['Municipio']
        if prueba.find('/')>-1:
            partes = prueba.split('/')
            parte1 = partes[0]
            parte2 = partes[1]
            if parte1.find('; ')>-1 or parte1.find(' (')>-1:
                trozos = parte1.replace(')','').replace(' (','; ').split('; ')
                if parte1.find("l'")>-1:
                    parte1 = trozos[1] + trozos[0]
                else:
                    parte1 = trozos[1] + ' ' + trozos[0]
            if parte2.find('; ')>-1 or parte2.find(' (')>-1:
                trozos = parte2.replace(')','').replace(' (','; ').split('; ')
                if parte2.find("l'")>-1:
                    parte2 = trozos[1] + trozos[0]
                else:
                    parte2 = trozos[1] + ' '+ trozos[0]
            prueba = parte1 + '/' + parte2
        else:
            if prueba.find('; ')>-1 or prueba.find(' (')>-1:
                trozos = prueba.replace(')','').replace(' (','; ').split('; ')
                if prueba.find("l'")>-1:
                    prueba = trozos[1] + trozos[0]
                else:
                    prueba = trozos[1] + ' '+ trozos[0]
        trans_tab = dict.fromkeys(map(ord, u'\u0301\u0308'), None)
        prueba = unicodedata.normalize('NFKC', unicodedata.normalize('NFKD', prueba).translate(trans_tab))
        archivo['Municipio'][index]=prueba.title()
    return archivo


# In[85]:


#Estimacion de las fechas y incidencia
#Input: Dataframe
def estimacionFechas(archivo):
    incidenciaFinal = archivo.sort_values(['Municipio','Fecha'],axis=0)

    ultMun='inicio'
    for index, row in incidenciaFinal.iterrows():
        if not pd.isna(row["Casos14"]):
            a='Casos14'
        elif not pd.isna(row["Casos7"]):
            a='Casos7'
        elif not pd.isna(row["Casos"]):
            a='Casos'
        if not ultMun==row['Municipio']:
            ultMun=row['Municipio']
            casosA=row[a]
            fechaA=datetime.strptime(row['Fecha'], '%Y-%m-%d').date()

        casosB=row[a]
        fechaB=datetime.strptime(row['Fecha'], '%Y-%m-%d').date()
        while not (fechaA+timedelta(days=1)==fechaB  or fechaA==fechaB):
            dif=(fechaB-fechaA).days
            fechaA=fechaA+timedelta(days=1)
            casosA=(casosB+(dif*casosA))/(dif+1)
            x={'Fecha':str(fechaA),'Municipio':row['Municipio'],a:round(casosA,2)}
            archivo=archivo.append(x,ignore_index=True)
        casosA=row[a]
        fechaA=datetime.strptime(row['Fecha'], '%Y-%m-%d').date() 
        archivo = archivo.sort_values(['Municipio','Fecha'],axis=0)

    for index, row in archivo.iterrows():    
        if pd.isna(row["Casos"]) and pd.isna(row['Casos14']):
            archivo["Casos"][index] = 0

    casos7 =[]
    cont=[]
    fechas=[]
    ultMun=''
    for index, row in archivo.iterrows():
        if pd.isna(row["Casos"]):
            casos7.append(round(int(row["Casos14"])/2,2))
        else:
            if not ultMun==row["Municipio"]:
                cont=[archivo['Casos'][index]]
                fechas=[archivo['Fecha'][index]]
            else:
                cont.append(archivo['Casos'][index])
                fechas.append(archivo['Fecha'][index])
                fechaX=datetime.strptime(row['Fecha'], '%Y-%m-%d')
                for f in fechas:
                    fecha0=datetime.strptime(f, '%Y-%m-%d')
                    if (fechaX-fecha0)>timedelta(days=7):
                        cont.pop(0)
                        fechas.pop(0)
            casos7.append(round(sum(cont),2))
        ultMun=row["Municipio"]
    archivo['Casos7']=casos7  

    casos14 =[]
    cont=[]
    fechas=[]
    ultMun=''
    for index, row in archivo.iterrows():
        if not pd.isna(row["Casos14"]):
            casos14.append(row["Casos14"])
        else:
            if not ultMun==row["Municipio"]:
                cont=[archivo['Casos'][index]]
                fechas=[archivo['Fecha'][index]]
            else:
                cont.append(archivo['Casos'][index])
                fechas.append(archivo['Fecha'][index])
                fechaX=datetime.strptime(row['Fecha'], '%Y-%m-%d')
                for f in fechas:
                    fecha0=datetime.strptime(f, '%Y-%m-%d')
                    if (fechaX-fecha0)>timedelta(days=14):
                        cont.pop(0)
                        fechas.pop(0)
            casos14.append(round(sum(cont),2))
        ultMun=row["Municipio"]

    archivo['Casos14']=casos14  
    for index, row in archivo.iterrows():    
        if pd.isna(row["Casos"]):
            archivo["Casos"][index] = round(archivo["Casos7"][index]/7,2)

    return archivo

