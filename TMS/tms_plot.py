# -*- coding: UTF-8 -*-

# File name: plot_tms.py
# Author: Joahannes Costa
# Data create: 03/12/2017
# Data last modified: 14/12/2017
# Python version: 2.7
# Description: captura dados dos arquivos summary e plota graficos de barras

from __future__ import division

import math
import numpy as np
import matplotlib.pyplot as plt

#Variaveis
ALGORITHMS = ("Mobilidade", "TMS", "TMS-DDRX") #
TRAFFICS = (700, 900, 1100, 1300, 1500) #
COLORS = {"Mobilidade" : "r", "TMS" : "blue", "TMS-DDRX" : "gold"}
formato = ".eps"
x_fig = 7.8 #7.8
y_fig = 5.5 #6.1
legenda_fig = u"Densidade (veiculos/km²)" #Legenda eixo X
legenda_size = 16 # Tamanho da fonte
#bbox_inches = 'tight', pad_inches = 0.05 -> elimina borda desnecessaria da imagem

# summary_file:
# 0 REPLICATION
# 1 HOST
# 2 STOPPED_CONGEST
# 3 MESSAGES_RECEIVED
# 4 TRANSMITTED
# 5 START_TIME
# 6 TOTALTIME
# 7 STOP_TIME
# 8 TOTAL_DISTANCE

def confidence_interval(values):
	N = len(values)
	Z = 1.96
	std_dev = np.std(values)
	std_error = std_dev / math.sqrt(N)
	return Z * std_error

#COBERTURA
def plot_cobertura():
	
	for algorithm in ALGORITHMS:
		coverage_values = []
		confidence_intervals = []
		
		coverage = float(0)
		
		for traffic in TRAFFICS:
			values = []
			file_input_name =  algorithm + "/summary-" + str(traffic) + ".txt"
			
			replication = 0
			coverage = 0.0
			
			for line in open(file_input_name):
				
				if replication == int(line.split()[0]):
					if line.split()[3] != "0":
						coverage += 1
				
				else:
				# CHANGED
					if not coverage == 0:
						values.append(coverage)
						coverage = 0
				
				while replication != int(line.split()[0]):
					replication += 1
			
			values = np.divide(values,traffic)
			values = np.multiply(values,100)
			
			coverage_values.append(np.mean(values))
			confidence_intervals.append(confidence_interval(values))
			
		x = np.arange(2, 7, dtype=np.float)
		ax = plt.subplot(111)
		
		if(algorithm == "TMS"):
			ax.bar(x-0.15, coverage_values, align='center', yerr=confidence_intervals, color=COLORS[algorithm], width=0.3, hatch='//', label="FASTER", error_kw=dict(elinewidth=1,ecolor='black'))
		
		if(algorithm == "TMS-DDRX"):
			ax.bar(x+0.15, coverage_values, align='center', yerr=confidence_intervals, color=COLORS[algorithm], width=0.3, hatch='\\', label="FASTER-DDRX", error_kw=dict(elinewidth=1,ecolor='black'))
	
	ax.legend(loc=2, ncol=2, fancybox=True, fontsize=legenda_size)
	
	ax.set_ylabel(u"Cobertura (%)", fontsize=legenda_size)
	ax.set_xlabel(legenda_fig, fontsize=legenda_size)
	
	yticks = np.arange(0, 120, 20)
	ax.set_yticks(yticks)
	ax.set_ylim(0,118)
	ax.set_yticklabels(yticks, fontsize=legenda_size)
	
	ax.set_xticks(x)
	ax.set_xticklabels(TRAFFICS, fontsize=legenda_size)
	ax.set_xlim(1.4,6.6)
	
	ax.set_axisbelow(3)
	plt.grid()
	
	fig = plt.gcf()
	fig.set_size_inches(x_fig, y_fig) #x, y
	fig.savefig('tms_cobertura' + formato, dpi=200, bbox_inches = 'tight', pad_inches = 0.05)
	
	plt.show()

#PACOTES_TRANSMITIDOS
def plot_transmitidos():
	
	for algorithm in ALGORITHMS:
		transmitted_values = []
		confidence_intervals = []
		
		for traffic in TRAFFICS:
			values = []
			file_input_name =  algorithm + "/summary-" + str(traffic) + ".txt"
			
			replication = 0
			transmitidos = 0
			
			for line in open(file_input_name):
				if replication == int(line.split()[0]):
					if line.split()[4] != "0":
						transmitidos += 1
				
				else:
				# CHANGED
					if not transmitidos == 0:
						values.append(transmitidos)
						transmitidos = 0
				
				while replication != int(line.split()[0]):
					replication += 1
			
			#values = np.divide(values,traffic)
			#values = np.multiply(values,100)
			
			transmitted_values.append(np.mean(values))
			confidence_intervals.append(confidence_interval(values))
		#print (algorithm, traffic, transmitted_values)
		x = np.arange(2, 7, dtype=np.float)
		ax = plt.subplot(111)
		
		if(algorithm == "TMS"):
			ax.bar(x-0.15, transmitted_values, align='center', yerr=confidence_intervals, color=COLORS[algorithm], width=0.3, hatch='//', label="FASTER", error_kw=dict(elinewidth=1,ecolor='black'))
		
		if(algorithm == "TMS-DDRX"):
			ax.bar(x+0.15, transmitted_values, align='center', yerr=confidence_intervals, color=COLORS[algorithm], width=0.3, hatch='\\', label="FASTER-DDRX", error_kw=dict(elinewidth=1,ecolor='black'))
	
	ax.legend(loc=2, ncol=1, fancybox=True, fontsize=legenda_size)
	
	ax.set_ylabel(u"Número de pacotes transmitidos", fontsize=legenda_size)
	ax.set_xlabel(legenda_fig, fontsize=legenda_size)
	
	yticks = np.arange(0, 400, 50)
	ax.set_yticks(yticks)
	ax.set_yticklabels(yticks, fontsize=legenda_size)

	ax.set_xticks(x)
	ax.set_xticklabels(TRAFFICS, fontsize=legenda_size)
	ax.set_xlim(1.4,6.6)
	
	ax.set_axisbelow(3)
	plt.grid()
	
	fig = plt.gcf()
	fig.set_size_inches(x_fig, y_fig) #x, y
	fig.savefig('tms_transmitidos' + formato, dpi=200, bbox_inches = 'tight', pad_inches = 0.05)
	
	plt.show()

#VELOCIDADE_MEDIA
def plot_velocidadeMedia():
	
	for algorithm in ALGORITHMS:
		speed_values = []
		confidence_intervals = []
		
		velocidadeMedia = float(0)
		
		for traffic in TRAFFICS:
			values = []
			file_input_name =  algorithm + "/summary-" + str(traffic) + ".txt"
			
			replication = 0
			velocidadeMedia = 0.0
			
			for line in open(file_input_name):
				
				if replication == int(line.split()[0]):
					#print(traffc , " - " , replication , file_input_name , line)
					if line.split()[6] != "0":
						velocidadeMedia += float(line.split()[8]) / float(line.split()[6])
						
				else:
				# CHANGED
					if not velocidadeMedia == 0:
						values.append(velocidadeMedia)
						velocidadeMedia = 0.0
				
				while replication != int(line.split()[0]):
					replication += 1
					
			#print ("\n")
			values = np.divide(values,traffic)
			#values = np.divide(values,3.6)
			
			speed_values.append(np.mean(values))
			confidence_intervals.append(confidence_interval(values))
		
		x = np.arange(2, 7, dtype=np.float)
		ax = plt.subplot(111)
		
		if(algorithm == "Mobilidade"):
			ax.bar(x-0.25, speed_values, align='center', yerr=confidence_intervals, color=COLORS[algorithm], width=0.25, hatch='', label="MOC", error_kw=dict(elinewidth=1,ecolor='black'))
		
		if(algorithm == "TMS"):
			ax.bar(x, speed_values, align='center', yerr=confidence_intervals, color=COLORS[algorithm], width=0.25, hatch='//', label="FASTER", error_kw=dict(elinewidth=1,ecolor='black'))
			
		if(algorithm == "TMS-DDRX"):
			ax.bar(x+0.25, speed_values, align='center', yerr=confidence_intervals, color=COLORS[algorithm], width=0.25, hatch='\\', label="FASTER-DDRX", error_kw=dict(elinewidth=1,ecolor='black'))
	
	ax.legend(loc=1, ncol=2, fancybox=True, fontsize=legenda_size)
	
	ax.set_ylabel(u"Velocidade Média (km/h)", fontsize=legenda_size)
	ax.set_xlabel(legenda_fig, fontsize=legenda_size)
	
	yticks = np.arange(0, 10, 1)
	ax.set_yticks(yticks)
	ax.set_yticklabels(yticks, fontsize=legenda_size)

	ax.set_xticks(x)
	ax.set_xticklabels(TRAFFICS, fontsize=legenda_size)
	ax.set_xlim(1.4,6.6)
	
	ax.set_axisbelow(3)
	plt.grid()
	
	fig = plt.gcf()
	fig.set_size_inches(x_fig, y_fig) #x, y
	fig.savefig('tms_velocidadeMedia' + formato, dpi=200, bbox_inches = 'tight', pad_inches = 0.05)
	
	plt.show()

#TEMPO_TOTAL
def plot_tempoTotal():
	
	for algorithm in ALGORITHMS:
		coverage_values = []
		confidence_intervals = []
		
		for traffic in TRAFFICS:
			values = []
			file_input_name =  algorithm + "/summary-" + str(traffic) + ".txt"
			
			replication = 0
			tempoTotal = 0.0
			
			for line in open(file_input_name):
				if replication == int(line.split()[0]):
					if line.split()[6] != "0":
						if float(line.split()[5]) > 300:
							tempoTotal += float(line.split()[6]) + float(line.split()[5])
						else:
							tempoTotal += float(line.split()[6])

				else:
				# CHANGED
					if not tempoTotal == 0:
						values.append(tempoTotal)
						tempoTotal = 0

				while replication != int(line.split()[0]):
					#print(algorithm, " - media: ",np.mean(values))
					replication += 1
			
			values = np.divide(values,traffic)
			values = np.divide(values,60)
			
			coverage_values.append(np.mean(values))
			confidence_intervals.append(confidence_interval(values))
			
		x = np.arange(2, 7, dtype=np.float)
		ax = plt.subplot(111)
		if(algorithm == "Mobilidade"):
			ax.bar(x-0.25, coverage_values, align='center', yerr=confidence_intervals, color=COLORS[algorithm], width=0.25, hatch='', label="MOC", error_kw=dict(elinewidth=1,ecolor='black'))
			
		if(algorithm == "TMS"):
			ax.bar(x, coverage_values, align='center', yerr=confidence_intervals, color=COLORS[algorithm], width=0.25, hatch='//', label="FASTER", error_kw=dict(elinewidth=1,ecolor='black'))
			
		if(algorithm == "TMS-DDRX"):
			ax.bar(x+0.25, coverage_values, align='center', yerr=confidence_intervals, color=COLORS[algorithm], width=0.25, hatch='\\', label="FASTER-DDRX", error_kw=dict(elinewidth=1,ecolor='black'))
		
	#ax.legend(numpoints=1, loc='upper center', ncol=3, fancybox=True, bbox_to_anchor=(0.5, +1.15))
	ax.legend(loc=2, ncol=2, fancybox=True, fontsize=legenda_size)
	
	ax.set_ylabel(u"Tempo total de viagem (minutos)", fontsize=legenda_size)
	ax.set_xlabel(legenda_fig, fontsize=legenda_size)

	yticks = np.arange(0, 8, 1)
	ax.set_yticks(yticks)
	ax.set_yticklabels(yticks, fontsize=legenda_size)

	ax.set_xticks(x)
	ax.set_xticklabels(TRAFFICS, fontsize=legenda_size)
	ax.set_xlim(1.4,6.6)

	ax.set_axisbelow(3) #grid atras
	plt.grid()
	
	fig = plt.gcf()
	fig.set_size_inches(x_fig, y_fig) #x, y
	fig.savefig('tms_tempoTotal' + formato, dpi=200, bbox_inches = 'tight', pad_inches = 0.05)
	plt.show()

#DISTANCIA_TOTAL
def plot_distanciaTotal():
	
	for algorithm in ALGORITHMS:
		distance_values = []
		confidence_intervals = []
		
		for traffic in TRAFFICS:
			values = []
			file_input_name =  algorithm + "/summary-" + str(traffic) + ".txt"
			
			replication = 0
			distanciaTotal = 0.0
			
			for line in open(file_input_name):
				#print(traffic , " - " , replication , file_input_name , line)
				if replication == int(line.split()[0]):
					if line.split()[8] != "0":
						distanciaTotal += float(line.split()[8])
				
				else:
				# CHANGED
					if not distanciaTotal == 0:
						values.append(distanciaTotal)
						distanciaTotal = 0
				
				while replication != int(line.split()[0]):
					replication += 1
			
			values = np.divide(values,traffic)
			values = np.divide(values,1000) #metros para km
			
			distance_values.append(np.mean(values))
			confidence_intervals.append(confidence_interval(values))
			
		x = np.arange(2, 7, dtype=np.float)
		ax = plt.subplot(111)
		
		if(algorithm == "Mobilidade"):
			ax.bar(x-0.25, distance_values, align='center', yerr=confidence_intervals, color=COLORS[algorithm], width=0.25, hatch='', label="MOC", error_kw=dict(elinewidth=1,ecolor='black'))
			
		if(algorithm == "TMS"):
			ax.bar(x, distance_values, align='center', yerr=confidence_intervals, color=COLORS[algorithm], width=0.25, hatch='//', label="FASTER", error_kw=dict(elinewidth=1,ecolor='black'))
			
		if(algorithm == "TMS-DDRX"):
			ax.bar(x+0.25, distance_values, align='center', yerr=confidence_intervals, color=COLORS[algorithm], width=0.25, hatch='\\', label="FASTER-DDRX", error_kw=dict(elinewidth=1,ecolor='black'))
	
	
	#ax.legend(numpoints=1, loc='upper center', ncol=3, fancybox=True, bbox_to_anchor=(0.5, +1.15))
	ax.legend(loc=2, ncol=2, fancybox=True, fontsize=legenda_size)
	
	ax.set_ylabel(u"Distância total (km)", fontsize=legenda_size)
	ax.set_xlabel(legenda_fig, fontsize=legenda_size)
	
	yticks = np.arange(0, 1.25, 0.2)
	ax.set_yticks(yticks)
	ax.set_yticklabels(yticks, fontsize=legenda_size)

	ax.set_xticks(x)
	ax.set_xticklabels(TRAFFICS, fontsize=legenda_size)
	ax.set_xlim(1.4,6.6)
	
	ax.set_axisbelow(3) #grid atras
	plt.grid()

	fig = plt.gcf()
	fig.set_size_inches(x_fig, y_fig) #x, y
	fig.savefig('tms_distanciaTotal' + formato, dpi=200, bbox_inches = 'tight', pad_inches = 0.05)

	plt.show()

#TEMPO_CONGESTIONAMENTO
def plot_tempoCongestionamento():
	
	for algorithm in ALGORITHMS:
		congestion_values = []
		confidence_intervals = []
		
		tempoCongestionamento = float(0)
		
		for traffic in TRAFFICS:
			values = []
			file_input_name =  algorithm + "/summary-" + str(traffic) + ".txt"
			
			replication = 0
			tempoCongestionamento = 0.0
			
			for line in open(file_input_name):
				
				if replication == int(line.split()[0]) :
					#print(traffic , " - " , replication , file_input_name , line)
					if line.split()[2] != "0":
						tempoCongestionamento += float(line.split()[2])
				else:
				# CHANGED
					if not tempoCongestionamento == 0:
						values.append(tempoCongestionamento)
						tempoCongestionamento = 0.0
				
				while replication != int(line.split()[0]):
					#print (algorithm, traffic, replication, values)
					replication += 1
					#print (algorithm, traffic, replication, values)
					#teste.append(replication)
					
			#print ("\n")
			values = np.divide(values,traffic)
			values = np.divide(values,60)
			
			congestion_values.append(np.mean(values))
			confidence_intervals.append(confidence_interval(values))
		
		x = np.arange(2, 7, dtype=np.float)
		ax = plt.subplot(111)
		
		if(algorithm == "Mobilidade"):
			ax.bar(x-0.25, congestion_values, align='center', yerr=confidence_intervals, color=COLORS[algorithm], width=0.25, hatch='', label="MOC", error_kw=dict(elinewidth=1,ecolor='black'))
		
		if(algorithm == "TMS"):
			ax.bar(x, congestion_values, align='center', yerr=confidence_intervals, color=COLORS[algorithm], width=0.25, hatch='//', label="FASTER", error_kw=dict(elinewidth=1,ecolor='black'))
			
		if(algorithm == "TMS-DDRX"):
			ax.bar(x+0.25, congestion_values, align='center', yerr=confidence_intervals, color=COLORS[algorithm], width=0.25, hatch='\\', label="FASTER-DDRX", error_kw=dict(elinewidth=1,ecolor='black'))
	
	ax.legend(loc=2, ncol=2, fancybox=True, fontsize=legenda_size)
	
	ax.set_ylabel(u"Tempo de Congestionamento (minutos)", fontsize=legenda_size)
	ax.set_xlabel(legenda_fig, fontsize=legenda_size)
	
	yticks = np.arange(0, 8, 1)
	ax.set_yticks(yticks)
	ax.set_yticklabels(yticks, fontsize=legenda_size)

	ax.set_xticks(x)
	ax.set_xticklabels(TRAFFICS, fontsize=legenda_size)
	ax.set_xlim(1.4,6.6)
	
	ax.set_axisbelow(3)
	plt.grid()
	
	fig = plt.gcf()
	fig.set_size_inches(x_fig, y_fig) #x, y
	fig.savefig('tms_tempoCongestionamento' + formato, dpi=200, bbox_inches = 'tight', pad_inches = 0.05)
	
	plt.show()

if __name__ == "__main__":
	pass
	print "\n *** TMS ***"
	
	print "\nGrafico de COBERTURA..."
	plot_cobertura()

	print "\nGrafico de TRANSMISSOES..."
	plot_transmitidos();
	
	print "\nGrafico de TEMPO TOTAL DE VIAGEM..."
	plot_tempoTotal()
	
	print "\nGrafico de DISTANCIA TOTAL..."
	plot_distanciaTotal()
	
	print "\nGrafico de VELOCIDADE MEDIA..."
	plot_velocidadeMedia()
	
	print "\nGrafico de TEMPO DE CONGESTIONAMENTO..."
	plot_tempoCongestionamento()
	