#!/usr/bin/env python
# coding: utf8

# versão do python usada: Python 2.7.6

#### Gera todos os boxplots
#### uso: ./gera_boxplot.py

#===================== Referencia de boxplot===================== 
# http://blog.bharatbhole.com/creating-boxplots-with-matplotlib/

from __future__ import unicode_literals

import numpy as np
import matplotlib as mpl 
import re
import os

mpl.use('agg') ## agg backend is used to create plot as a .png file
import matplotlib.pyplot as plt 

import statistics as stat

num_medicoes = 10
num_entradas = 10

lista_results = ["results_8maq_1core", "results_4maq_2core", "results_2maq_4core", "results_1maq_8core"]
lista_diretorios = ["mandelbrotOpenMPI_omp", "mandelbrotOpenMPI_seq", "mandelbrot_seq"]
regioes = ['full', 'seahorse', 'elephant', 'triple_spiral']

# entradas = ['16', '32', '64', '128', '256', '512', '1024', '2048', '4096', '8192']

arq_med = open("medianas.txt", "w")
arq_med.write("Entradas: 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192\n\n")

###################### parser dos tempos de cada arquivo #############################
# cada arquivo .log tera um grafico
for results in lista_results[:1]:
	for diretorio in lista_diretorios:
		lista_arquivos = os.listdir(results+"/"+diretorio)

		# print diretorio

		for arquivo in lista_arquivos:
			arq = open(results+"/"+diretorio+"/"+arquivo, 'r')
			
			texto = arq.read() 

			tempos = re.findall(r"\d+[,.]\d+ seconds time elapsed", texto)
			numeros = []


			for x in tempos:
				aux = x.split(" seconds time elapsed")
				numeros.append(float(aux[0].replace(",", "."))) 
			arq.close()

			# # debug (fabio)
			# print results+"/"+diretorio+"/"+arquivo
	
			# # debug (ricardos)
	# 		print "\n("+arquivo+"):"
	# 		print numeros
	# 	print
	# print
	


		# 	data_to_plot = []
		# 	mediana = []

		# 	for j in range(0, num_entradas):
		# 		## define uma amostra
		# 		amostra = numeros[(num_medicoes * j) : (num_medicoes * (j+1))]
		# 		amostra.sort()

		# 		mediana.append(stat.median(amostra))

		# 		##  E a adiciona numa coleção global delas  
		# 		data_to_plot.append(amostra)

			
		# 	# Cria uma instancia de figura e eixos
		# 	fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 9))

		# 	# Cria o boxplot
		# 	box_plot = ax.boxplot(data_to_plot)


		# 	maximo = 0
		# 	for j in range(num_entradas):
		# 	 	if data_to_plot[j][-1] > maximo:
		# 	 		maximo = data_to_plot[j][-1]
			
		# 	ax.set_xticklabels(entradas)
		# 	ax.yaxis.grid(True)
			
		# 	plt.xlabel('Tamanho Da Entrada', fontsize=10, color='red')
		# 	plt.ylabel('Tempo Em Segundos', fontsize=10, color='red')

		# 	title = './'+diretorio
		# 	title += ', regiao: '

		# 	for regiao in regioes:
		# 		lista = re.findall(regiao, arquivo)			
		# 		# encontra o nome da regiao atual			
		# 		if len(lista) > 0:
		# 			title += regiao

		# 	if diretorio == 'mandelbrot_seq':
		# 		s = arquivo[-7:-4]
		# 		title += (', '+s.upper()+' I/O e aloc. memoria')
			
		# 	else:
		# 		lista = re.findall(r"\d+", arquivo)			
		# 		title += (', #threads: '+lista[0])

		# 	plt.title(title, fontsize=10)

		# 	############# codigo para imprimir as medianas em um txt ###############
		# 	arq_med.write(title+"\n")
		# 	arq_med.write('medianas: ')
		# 	j = 0
		# 	while j < len(mediana):
		# 		x = mediana[j]
		# 		mediana[j] = str(round(x, 2))
		# 		arq_med.write(mediana[j]+", ")
		# 		j += 1
		# 	arq_med.write("\n\n")
		# 	########################################################################

		# 	## Remove marcadores de eixos
		# 	ax.get_xaxis().tick_bottom()
		# 	ax.get_yaxis().tick_left()

		# 	maximo = round(maximo, 5) 
		# 	interval = round(maximo/30.0, 5)
		# 	print "maximo = ", maximo
		# 	print "interval = ", interval
		# 	print "*************************"
			
		# 	plt.yticks(np.arange(0, maximo + interval, interval))
			
		# 	# Salva a figura
		# 	fig.savefig('graphics/'+diretorio+'/'+arquivo[0:-4]+'.png', bbox_inches='tight')
						
		# print ''

print '>> file medianas.txt'
arq_med.close()
