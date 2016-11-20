#### CODIGO PARA CRIAR BASE DE DADOS SELECIONADA POR DATA E COM INFORMACOES QUE PODEM SER UTEIS

import json
import re
import langid

f = open('stream_trumpwins.txt')

r = "^\{\"created_at\":\"Wed Nov 09"

print('id_original, data, usuario, localizacao, texto')

for l in f:

	match = re.search(r,l)
	
	if match:

 		obj = json.loads(l)
 			
 		if "created_at" in obj:
 			
 			id_original = obj['id']
 			data = obj['created_at']
 			usuario = obj['user']['screen_name']
 			localizacao = obj['user']['location']
 			texto = obj['text'].replace('"',"'").replace("\n"," - ").lower()
 			texto = re.sub(":(\w)", "\:\\1",texto) # para tirar emoticon
 			texto = re.sub("http.*?( |$)","",texto) # para tirar links
 			texto = re.sub("^rt @.*?: ","",texto) # pra tirar inicio do tweet que mostra ser retweet
 			
 			#Selecionar apenas lingua inglesa
 			if langid.classify(texto)[0] == 'en':
 			
 				print(('%s,%s,%s,%s,%s') % (id_original, data, usuario, localizacao, texto.encode('utf-8').decode('utf-8').encode('cp1252','ignore').decode('cp1252')))
