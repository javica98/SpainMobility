#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pandas as pd
from patsy import dmatrices
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import copy
import csv
import math


# In[44]:


csv= pd.read_csv('riesgo.csv')
csv = csv.sort_values(['Fecha'],axis=0)
grupos = csv.groupby('Aeropuerto')
aeropuertos = csv['Aeropuerto'].drop_duplicates().tolist()
fechas = csv['Fecha'].drop_duplicates().tolist()
plt.figure(figsize=(50,50))
for i in aeropuertos:
    a= grupos.get_group(i)
    plt.plot(a['Fecha'],a['CasosEstimados'],label=i)

plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
plt.title("Personas Infectadas Estimadas Diarias",fontsize=45)
plt.xlabel("Fecha",fontsize=50)
plt.ylabel("Personas Infectadas",fontsize=50)
plt.legend(prop={'size': 30})
plt.savefig("PersonasEstimadas.jpg")
plt.figure(figsize=(50,50))
plt.show()
    


# In[43]:


csv= pd.read_csv('riesgoPrincipal.csv')
csv = csv.sort_values(['Fecha'],axis=0)
grupos = csv.groupby('Aeropuerto')
aeropuertos = csv['Aeropuerto'].drop_duplicates().tolist()
fechas = csv['Fecha'].drop_duplicates().tolist()
plt.figure(figsize=(50,50))
for i in aeropuertos:
    a= grupos.get_group(i)
    plt.plot(a['Fecha'],a['CasosEstimados'],label=i)

plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
plt.title("Personas Infectadas Estimadas Diarias",fontsize=45)
plt.xlabel("Fecha",fontsize=50)
plt.ylabel("Personas Infectadas",fontsize=50)
plt.legend(prop={'size': 30})
plt.savefig("PersonasEstimadasPPrincipales.jpg")
plt.figure(figsize=(50,50))
plt.show()
    


# In[7]:


csv= pd.read_csv('Expansion.csv')
for index, row in csv.iterrows():
    csv['Flujo'][index]=row['Flujo']*2
print(csv)
csv.to_csv("DicRiesgo.csv")


# In[12]:


csv= pd.read_csv('Expansion.csv')
prob=[]
for index, row in csv.iterrows():
    prob.append(row['P']/row['Flujo'])
csv['Prob']=prob
print(csv)
csv.to_csv("DicRiesgo.csv")


# In[10]:


csv= pd.read_csv('MadridCon0.csv')
csv = csv.sort_values(['Distrito','Fecha'],axis=0)

distrito='ultimo'
flujo='ultimo'
ind='ultimo'
for index, row in csv.iterrows():
    if flujo!=0.0 and row['Flujo']==0.0 and distrito==row['Distrito']:
        csv['Flujo'][index]=flujo/2
        csv['Flujo'][ind]=flujo/2
    distrito=row['Distrito']
    flujo=row['Flujo']
    ind=index
csv.to_csv("MadridCon0.csv")


# In[30]:


csv= pd.read_csv('MadridMunicipiosCorrgido.csv')
poblacion=pd.read_csv('DicRiesgo.csv')
poblacionSeries=pd.Series(poblacion['Prob'].values.tolist(), 
            index=poblacion['Fecha'].values.tolist())
pob=[]
for index, row in csv.iterrows():
   
    if row['Flujo']==0:
        pob.append(0)
    else:
        p=poblacionSeries[row['Fecha']]
        pob.append(row['Flujo']*p)
csv['Casos']=pob
print(csv)
csv.to_csv("MadridMunicipiosCorrgido.csv")


# In[31]:


df=pd.read_csv('ModeloMadrid.csv')
df.head()
del df['Fecha']
df


# In[14]:


df.corr(method='pearson')
print(df)


# In[8]:


plt.matshow(df.corr())


# In[34]:


plt.plot(df['Casos'],df['Inc14'],'ro')
plt.ylabel('Incidencia 14 días')
plt.xlabel('Casos')


# In[11]:


plt.plot(df['Inc'],df['Inc14'],'ro')
plt.ylabel('Incidencia 14 días')
plt.xlabel('Incidencia actual')


# In[81]:


csv=pd.read_csv('ModeloMadrid.csv')
print(csv.corr(method='pearson'))
del csv['Municipio']
del csv['Flujo']
del csv['Poblacion']
del csv['Casos']

csv.to_csv("cor.csv")
grupos = csv.groupby('Fecha')
d16= grupos.get_group('2020-03-16')
d18= grupos.get_group('2020-03-18')
d20= grupos.get_group('2020-03-20')
d22= grupos.get_group('2020-03-22')
d24= grupos.get_group('2020-03-24')
d26= grupos.get_group('2020-03-26')
d28= grupos.get_group('2020-03-28')
d30= grupos.get_group('2020-03-30')
d31= grupos.get_group('2020-03-31')
d31.to_csv("cor.csv")
grupos = [d16,d18,d20,d22,d24,d26,d28,d30,d31]

plt.xlim([0, 500])
plt.ylim([0, 500])

plt.scatter(d16['Inc'], d16['Inc14'], c='green') 
plt.scatter(d18['Inc'], d18['Inc14'], c='red') 
plt.scatter(d20['Inc'], d20['Inc14'], c='b') 
plt.scatter(d22['Inc'], d22['Inc14'], c='m') 
plt.scatter(d24['Inc'], d24['Inc14'], c='y') 
plt.scatter(d26['Inc'], d26['Inc14'], c='k') 
plt.scatter(d28['Inc'], d28['Inc14'], c='w') 
 

plt.show() 


# In[29]:


dias=[16,18,20,22,24,26,28,30,31]
correlacionCasos=[]
correlacionInc=[]
for i in grupos:
    del i['Fecha']
    cor = i.corr(method='pearson')
    correlacionCasos.append(cor['Inc14'][2])
    correlacionInc.append(cor['Inc14'][0])
print(correlacionInc)


# In[23]:


plt.plot(dias,correlacionCasos,'ro')
plt.ylim(-1, 1) # Set y-axis limits
plt.ylabel('Correlacion')
plt.xlabel('Dias')


# In[24]:


plt.plot(dias,correlacionInc,'ro')
plt.ylim(-1, 1) # Set y-axis limits
plt.ylabel('Correlacion')
plt.xlabel('Dias')


# In[45]:


df=pd.read_csv('ModeloMadrid.csv')
del df['Municipio']
del df['Flujo']
del df['Poblacion']
del df['Fecha']
mask = np.random.rand(len(df)) < 0.8
df_train = df[mask]
df_test = df[~mask]

y_train, X_train = dmatrices('Inc14 ~ Inc + Casos', df_train, return_type='dataframe')
y_test, X_test = dmatrices('Inc14 ~ Inc + Casos', df_test, return_type='dataframe')

poisson_training_results = sm.GLM(y_train, X_train, family=sm.families.Poisson()).fit()

print(poisson_training_results.summary())


# In[83]:


df=pd.read_csv('ModeloMadrid.csv')
del df['Municipio']
del df['Flujo']
df['Casos^1/3']=[i**(1/3) for i in df['Casos']]
df['Casos^1/5']=[i**(1/5) for i in df['Casos']]
df['log(Inc)']=[math.log10( i ) for i in df['Inc']]
df['log(Inc14)']=[math.log10( i ) for i in df['Inc14']]

df['Casos*']=[(i['Casos']*100.000/i['Poblacion']) for index,i in df.iterrows()]
df['Casos*^1/3']=[(i['Casos']*100.000/i['Poblacion'])*(1/3) for index,i in df.iterrows()]
df['Casos*^1/5']=[(i['Casos']*100.000/i['Poblacion'])*(1/5) for index,i in df.iterrows()]
del df['Poblacion']


# In[88]:


fig, ax = plt.subplots(3,2)
fig.set_size_inches(10,10)

ax[0,0].title.set_text('Casos-Inc14')
ax[0,0].plot(df['Casos'],df['Inc14'],'ro')
ax[1,0].title.set_text('Casos^(1/3)-Inc14')
ax[1,0].plot(df['Casos^1/3'],df['Inc14'],'ro')
ax[2,0].title.set_text('Casos^(1/5)-Inc14')
ax[2,0].plot(df['Casos^1/5'],df['Inc14'],'ro')
ax[0,1].title.set_text('Casos-log(Inc14)')
ax[0,1].plot(df['Casos'],df['log(Inc14)'],'ro')
ax[1,1].title.set_text('Casos^(1/3)-log(Inc14)')
ax[1,1].plot(df['Casos^1/3'],df['log(Inc14)'],'ro')
ax[2,1].title.set_text('Casos^(1/5)-log(Inc14)')
ax[2,1].plot(df['Casos^1/5'],df['log(Inc14)'],'ro')

plt.savefig("transformacionesCasos.jpg")
plt.show()


# In[131]:


fig, ax = plt.subplots(2,2)
fig.set_size_inches(10,10)
ax[0,0].title.set_text('Inc-Inc14')
ax[0,0].plot(df['Inc'],df['Inc14'],'ro')
ax[1,0].title.set_text('log(Inc)-Inc14')
ax[1,0].plot(df['log(Inc)'],df['Inc14'],'ro')

ax[0,1].title.set_text('Inc-log(Inc14)')
ax[0,1].plot(df['Inc'],df['log(Inc14)'],'ro')
ax[1,1].title.set_text('log(Inc)-log(Inc14)')
ax[1,1].plot(df['log(Inc)'],df['log(Inc14)'],'ro')

plt.savefig("transformacionesInc.jpg")
plt.show()


# In[132]:


tabla = df.corr(method='pearson')
tabla['Inc14']
tabla['log(Inc14)']


# In[ ]:




