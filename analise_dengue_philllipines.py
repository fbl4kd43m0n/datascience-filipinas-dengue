#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 20:27:21 2019

@author: fransalles
"""

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
%matplotlib inline
color = sns.color_palette()

data = pd.read_csv('denguecases.csv')
data.info()

# Checking missing data
def missing_data(data):
    total = data.isnull().sum()
    percent = (data.isnull().sum()/data.isnull().count()*100)
    tt = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
    types = []
    for col in data.columns:
        dtype = str(data[col].dtype)
        types.append(dtype)
    tt['Types'] = types
    return(np.transpose(tt))

missing_data(data)

# The number of cases in any month corresponding to a year are given as floats. Let's round off
data['Dengue_Cases'] = data['Dengue_Cases'].apply(lambda x : np.round(x).astype(np.uint8))
data.head()

# How many regions are there?
regions_count = data.Region.value_counts()
print("Número total de regiões : ", len(regions_count))
print("Regiões com o número de ocorrências: ")
print(regions_count)

print("Número mínimo de casos de dengue...: ", np.min(data.Dengue_Cases.values))
print("Número máximo de casos de dengue...: ", np.max(data.Dengue_Cases.values))
print("Média do número de casos de dengue.: ", int(np.mean(data.Dengue_Cases.values)))

# Número de casos por ano
# What's the count of cases for each year?
data_groups = data.groupby(['Year'])
ano = []
casos = []

for name, group in data_groups:
    ano.append(name)
    casos.append(group['Dengue_Cases'].sum())

plt.figure(figsize=(10,8))    
sns.barplot(x=ano, y=casos, color=color[2])
plt.title('Número total de casos de dengue por ano')
plt.xlabel('Ano', fontsize=16)
plt.ylabel('Quantidade', fontsize=16)
plt.show()

# 2012, 2013 e 2014 foram os anos com os maiores casos de dengue
# de 2011 a 2013 houve um crescente significativo na quantidade de casos
# de dengue.
# de 2013 a 2016 houve um decréscimo significativo na quantidade de casos
# de dengue.

# E as regiões? Qual é a quantidade de casos de acordo a região?
data_grupos = data.groupby(['Region'])

regioes = []
casos = []

for name, group in data_grupos:
    regioes.append(name)
    casos.append(group['Dengue_Cases'].sum())

plt.figure(figsize=(10,8))    
sns.barplot(y=regioes, x=casos, color=color[3], orient='h')
plt.title('Número de casos de dengue por região')
plt.xlabel('Quantidade', fontsize=16)
plt.ylabel('Região', fontsize=16)
plt.yticks(range(len(regioes)), regioes)
plt.show()

'''
CAR (Região Administrativa de Cordilheira) é a região onde o número máximo de 
casos de dengue é encontrado. Conforme Wiki, é a área menos densamente povoada. 
Mesmo assim, tantos números de casos? Isso pode ser por causa da falta de 
consciência entre as pessoas que vivem lá. Por outro lado, a ARMM é a região 
com menor número de casos de dengue.
'''

# E com respeito à quantidade de casos de dengue por região em cada ano?
data_groups = data.groupby(['Year'])

f,axs = plt.subplots(5,2, figsize=(20,40), sharex=False, sharey=False)
for i,(year, group) in enumerate(data_groups):
    regions = []
    cases = []
    region_group = group.groupby(['Region'])
    for region, df in region_group:
        regions.append(region)
        cases.append(df['Dengue_Cases'].sum())
    sns.barplot(y=regions, x=cases, color=color[4], orient='h', ax=axs[i//2, i%2])
    axs[i//2, i%2].set_title(year, fontsize=14)
    axs[i//2, i%2].set_xlabel("Casos", fontsize=14)
    axs[i//2, i%2].set_ylabel("Região", fontsize=14)
f.delaxes(axs[4][1])
plt.show()    



'''
Os gráficos acima são muito interessantes. Anteriormente descobrimos que o CAR 
era a região com o número máximo de casos, mas isso não é verdade para todos os 
anos. Aqui estão algumas boas percepções:

O gráfico de 2008 e 2009 é quase similar.
Número máximo de casos foram relatados para a Região vii durante 2008-10.
Houve um aumento repentino no número de casos relatados na Região xii durante 2010-11.
A ARMM é a única região em que o número de casos de dengue sempre foi o menor. 
Isso significa que as pessoas estão cientes aqui sobre isso.
A partir de 2011-13, houve uma queda no número de casos para a Região vii, mas 
houve um aumento súbito no número de casos de dengue para esta região nos 
últimos anos (2014-16). Eu não sei o que aconteceu aqui.
'''

# Vamos fazer algumas análises dos meses agora
data_groups = data.groupby(['Year'])
months = ('Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 
          'Setembro', 'Outubro', 'Novembro', 'Dezembro')
f,axs = plt.subplots(5,2, figsize=(20,40), sharex=False, sharey=False)
for i,(year, group) in enumerate(data_groups):
    sns.barplot(y=group['Month'], x=group['Dengue_Cases'], color=color[5], orient='h', ax=axs[i//2, i%2])
    axs[i//2, i%2].set_title(year, fontsize=14)
    axs[i//2, i%2].set_xlabel("Casos", fontsize=14)
    axs[i//2, i%2].set_ylabel("Mês", fontsize=14)
    axs[i//2, i%2].set_xticks(range(len(months)), months)
f.delaxes(axs[4][1])
plt.show()

