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
nCod = 3
nConf = 4

lista_results = ["results_1maq_8core", "results_2maq_4core", "results_4maq_2core", "results_8maq_1core"]
lista_diretorios = ["mandelbrot_seq", "mandelbrotOpenMPI_seq", "mandelbrotOpenMPI_omp"]
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

maximo = {'full' : 0, 'seahorse' : 0, 'elephant' : 0, 'triple' : 0}
for results in lista_results[:4]:
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
			if amostras[modo_arq][nome_regiao][diretorio][results][-1] > maximo[nome_regiao]:
				maximo[nome_regiao] = amostras[modo_arq][nome_regiao][diretorio][results][-1]

			arq.close()
			

###########################################

# Cria o boxplot


for modoKey, modo in amostras.items():
	for regiaoKey, regiao in modo.items():

		# Cria uma instancia de figura e eixos
		fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 9))
		data_to_plot = []
		for i in range (nCod):
			tipoCodigo = regiao[lista_diretorios[i]]

			figIndivual, axIndivual = plt.subplots(nrows=1, ncols=1, figsize=(10, 9))			
			data_to_plotIndivual = []
			
			for j in range (nConf):
				tipoConfig = tipoCodigo[lista_results[j]]
				data_to_plot.append(tipoConfig)
				data_to_plotIndivual.append(tipoConfig)		
			data_to_plot.append([0,0,0,0,0,0,0,0,0,0]) #para criar um espaco entre os result dos dif codigos
			box_plotIndivual = axIndivual.boxplot(data_to_plotIndivual)
			axIndivual.set_xticklabels(["1maq_8core", "2maq_4core", "4maq_2core", "8maq_1core"], rotation = 90)
			axIndivual.yaxis.grid(True)

			plt.xlabel('Número de máquinas e cores', fontsize=10, color='red')
			plt.ylabel('Tempo Em Segundos', fontsize=10, color='red')	

			title = 'regiao: '+regiaoKey+' '+modoKey+' I/O e aloc. memoria com N = 8192 '+lista_diretorios[i]
			plt.title(title, fontsize=10)

			## Remove marcadores de eixos
			axIndivual.get_xaxis().tick_bottom()
			axIndivual.get_yaxis().tick_left()

			maxRegiao = round(maximo[regiaoKey], 5) 
			interval = round(maxRegiao/30.0, 5)
			
			plt.yticks(np.arange(0, maxRegiao + interval, interval))

			# Salva a figura
			figIndivual.savefig('graphics/'+lista_diretorios[i]+'/'+regiaoKey+'_'+modoKey+'.png', bbox_inches='tight')
			plt.cla()
			plt.close()



		box_plot = ax.boxplot(data_to_plot)
		
		ax.set_xticklabels(["1maq_8core_seq", "2maq_4core_seq", "4maq_2core_seq", "8maq_1core_seq","","1maq_8core_openMPI_seq", "2maq_4core_openMPI_seq", "4maq_2core_openMPI_seq", "8maq_1core_openMPI_seq","","1maq_8core_openMPI_omp", "2maq_4core_openMPI_omp", "4maq_2core_openMPI_omp", "8maq_1core_openMPI_omp"], rotation = 90)
		ax.yaxis.grid(True)

		plt.xlabel('Número de máquinas e cores', fontsize=10, color='red')
		plt.ylabel('Tempo Em Segundos', fontsize=10, color='red')	

		title = 'regiao: '+regiaoKey+' '+modoKey+' I/O e aloc. memoria com N = 8192'
		plt.title(title, fontsize=10)

		## Remove marcadores de eixos
		ax.get_xaxis().tick_bottom()
		ax.get_yaxis().tick_left()

		maxRegiao = round(maximo[regiaoKey], 5) 
		interval = round(maxRegiao/30.0, 5)
		print "maximo = ", maxRegiao
		print "interval = ", interval
		print "*************************"

		plt.yticks(np.arange(0, maxRegiao + interval, interval))

		# Salva a figura
		fig.savefig('graphics/'+regiaoKey+'_'+modoKey+'.png', bbox_inches='tight')
		plt.cla()
		plt.close()