from __future__ import print_function
import json
import pandas as pd
import random
import langid
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import csv
from nltk.stem.porter import PorterStemmer
import nltk
from nltk.tokenize import RegexpTokenizer

## CODIGO PARA FAZER MATRIZ TFIDF E CLUSTERIZACAO

## Abrir base de dados com amostra aleatoria de linhas - por causa da memoria do computador
filename = "trumpwinstotal2.csv"
n = sum(1 for line in open(filename)) - 1 #total de linhas do documento (78947), excluindo primeira
s = 40000 #tamanho da amostra que roda no meu computador
skip = sorted(random.sample(range(1,n+1),n-s)) #a primeira linha nao sera incluida
colnames = ['id_original', 'data', 'usuario', 'localizacao', 'texto']
data = pd.read_csv(filename, comment='#',encoding = 'utf8', header=0, skiprows=skip, names=colnames, error_bad_lines=False)
print('Base de dados importada')

## excelente site - http://brandonrose.org/clustering
## PARA FAZER A TABELA FREQUENCIA DOS TERMOS DOS TEXTOS

textos = data.texto.astype('U')
ids = data.id_original
dia = data.data.astype('U')
usuario = data.usuario.astype('U')
localizacao = data.localizacao.astype('U')

print('Lista de textos aleatorios criada de 78856 textos')
print('Quantiadade de textos:')
print(len(textos))

stemmer = PorterStemmer()
tokenizer = RegexpTokenizer(r'\w+') #sem pontuacao

def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed

def tokenize(textos):
    tokens = tokenizer.tokenize(textos)
    stems = stem_tokens(tokens, stemmer)
    return stems


tfidf_vectorizer = TfidfVectorizer(stop_words='english',tokenizer=tokenize, use_idf=True, smooth_idf=False, encoding = 'utf8')
tfidf_matrix = tfidf_vectorizer.fit_transform(textos)
terms = tfidf_vectorizer.get_feature_names()

matrix=dict(zip(terms, tfidf_matrix))
print('Matriz de tfidf feita. Tamanho da matriz:')
print(tfidf_matrix.shape)
print('Matriz de tfidf:')
print(matrix) 
print()
print()

# dist = 1 - cosine_similarity(tfidf_matrix)

### para fazer a clusterizacao
num_clusters = 10
print('Definicao do numero de clusters')

print('Fazendo a clusterizacao...')

km = KMeans(n_clusters=num_clusters)
km.fit(tfidf_matrix)

#clusters = km.labels_.tolist() # JOGA FORA OS CLUSTERS E JOGA FORA E DÁ NOME

# inspeciona clusters 
#data['cluster'] = km.labels_ #cria coluna com numero do cluster de cada amostra - fica com o atributo labels

clusters = km.labels_

data['cluster'] = clusters

print('Colunas da base:')
print(list(data))

#frame = pd.DataFrame(textos, index = [clusters], columns = {'clusters'})

print()
print()
print('Quantos textos por cluster:')
print(data['cluster'].value_counts())

#print(data[['texto','cluster']]) #mostra para cada texto o cluster que faz parte 

#print("Textos por cluster:")

#for i in (data_ordenada):
#	print(set('% | %' % data.texto, data.cluster))

print()
print() 

#### Agrupar textos por cluster:


grouped = data.groupby(data['cluster'])

print('Agrupados!')

for i in grouped:
	print('%s ; %s' % (i, 'tweet'))
	with open('clusters-textostrump.csv','a') as csvfile:
		writer = csv.writer(csvfile)
		[writer.writerow(r) for r in grouped] 
	
print()
print() 


### PRINTAR PALAVRAS MAIS CENTRAIS DE CADA CLUSTER. which are the top n (I chose n=6) 
######words that are nearest to the cluster centroid. This gives a good sense of the main 
########topic of the cluster.

print("Principais termos por cluster:")
print()
# Sort os centros do cluster pela proximidade do centroide
order_centroids = km.cluster_centers_.argsort()[:, ::-1] 

for i in range(num_clusters):
	print("Cluster %d words:" % i, end='')
    
	for ind in order_centroids[i, :100]: #Determinação numero de palavras por cluster
		print(' %s' % terms[ind].split(' '), end=',')
      		
	print() #add whitespace
	print() #add whitespace
