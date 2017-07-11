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

lista_results = ["results_8maq_1core", "results_4maq_2core", "results_2maq_4core", "results_1maq_8core"]
lista_diretorios = ["mandelbrotOpenMPI_omp", "mandelbrotOpenMPI_seq", "mandelbrot_seq"]
regioes = ['full', 'seahorse', 'elephant', 'triple_spiral']

###################### parser dos tempos de cada arquivo #############################
# cada arquivo .log tera um grafico

amostras = {
	'com':{
		'full': {'mandelbrotOpenMPI_omp': {},'mandelbrotOpenMPI_seq': {},'mandelbrot_seq': {}}, 
		'seahorse': {'mandelbrotOpenMPI_omp': {},'mandelbrotOpenMPI_seq': {},'mandelbrot_seq': {}},
		'elephant': {'mandelbrotOpenMPI_omp': {},'mandelbrotOpenMPI_seq': {},'mandelbrot_seq': {}},
		'triple': {'mandelbrotOpenMPI_omp': {},'mandelbrotOpenMPI_seq': {},'mandelbrot_seq': {}}
	},
	'sem':{
		'full': {'mandelbrotOpenMPI_omp': {},'mandelbrotOpenMPI_seq': {},'mandelbrot_seq': {}}, 
		'seahorse': {'mandelbrotOpenMPI_omp': {},'mandelbrotOpenMPI_seq': {},'mandelbrot_seq': {}},
		'elephant': {'mandelbrotOpenMPI_omp': {},'mandelbrotOpenMPI_seq': {},'mandelbrot_seq': {}},
		'triple': {'mandelbrotOpenMPI_omp': {},'mandelbrotOpenMPI_seq': {},'mandelbrot_seq': {}}
	}  
}

for results in lista_results[:2]:
	for diretorio in lista_diretorios:
		lista_arquivos = os.listdir(results+"/"+diretorio)

		for arquivo in lista_arquivos:
			arq = open(results+"/"+diretorio+"/"+arquivo, 'r')
			
			nome_arq_aux = arquivo.split("_")
			nome_regiao = nome_arq_aux[0]
			modo_arq = nome_arq_aux[-1].split(".")[0]

			texto = arq.read() 

			tempos = re.findall(r"\d+[,.]\d+ seconds time elapsed", texto)
			numeros = []

			for x in tempos:
				aux = x.split(" seconds time elapsed")
				numeros.append(float(aux[0].replace(",", "."))) 

			amostras[modo_arq][nome_regiao][diretorio][results] = numeros            
			amostras[modo_arq][nome_regiao][diretorio][results].sort()
			arq.close()
			

###########################################
# mediana = []

## define uma amostra
# amostra = numeros[:]
# amostra.sort()

# mediana.append(stat.median(amostra))

##  E a adiciona numa coleção global delas  
# data_to_plot.append(amostra)



# Cria o boxplot
for modoKey, modo in amostras.items():
	for regiaoKey, regiao in modo.items():

		# Cria uma instancia de figura e eixos
		fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 9))
		data_to_plot = []

		for _, tipoCodigo in regiao.items():
			for _, tipoConfig in tipoCodigo.items():
				data_to_plot.append(tipoConfig)
		
		box_plot = ax.boxplot(data_to_plot)
		
		maximo = 0
		
		for amostra in data_to_plot:
			if amostra[-1] > maximo:
				maximo = amostra[-1]

		ax.set_xticklabels(["8maq_1core", "4maq_2core", "2maq_4core", "1maq_8core_openMPI_seq", "8maq_1core", "4maq_2core", "2maq_4core", "1maq_8core_seq","8maq_1core", "4maq_2core", "2maq_4core", "1maq_8core_openMPI_omp"])
		ax.yaxis.grid(True)

		plt.xlabel('Número de máquinas e cores', fontsize=10, color='red')
		plt.ylabel('Tempo Em Segundos', fontsize=10, color='red')
		
		# a = raw_input()

# 	title = 'região: '

# for regiao in regioes:
# 	lista = re.findall(regiao, arquivo)			
# 	# encontra o nome da regiao atual			
# 	if len(lista) > 0:
# 		title += regiao

# s = arquivo[-7:-4]
# title += (', '+s.upper()+' I/O e aloc. memoria')

# plt.title(title, fontsize=10)

		## Remove marcadores de eixos
		ax.get_xaxis().tick_bottom()
		ax.get_yaxis().tick_left()

		maximo = round(maximo, 5) 
		interval = round(maximo/30.0, 5)
		print "maximo = ", maximo
		print "interval = ", interval
		print "*************************"

		plt.yticks(np.arange(0, maximo + interval, interval))

		# Salva a figura
		fig.savefig('graphics/'+regiaoKey+'_'+modoKey+'.png', bbox_inches='tight')
