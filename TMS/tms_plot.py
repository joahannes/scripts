# -*- coding: UTF-8 -*-

# File name: tms_plot.py
# Author: Joahannes Costa
# Data create: 03/12/2017
# Data last modified: 06/12/2017
# Python version: 2.7
# Description: captura dados dos arquivos summary e plota graficos de barras

from __future__ import division

import math
import numpy as np
import matplotlib.pyplot as plt

ALGORITHMS = ("Mobilidade", "TMS", "TMS-DDRX") #
TRAFFICS = (700, 900, 1100, 1300,1500) #
COLORS = {"Mobilidade" : "r", "TMS" : "blue", "TMS-DDRX" : "gold"} # TMS: #42413e, TMS-DDRX: #efc034
formato = ".png"

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
			ax.bar(x-0.15, coverage_values, align='center', yerr=confidence_intervals, color=COLORS[algorithm], width=0.3, hatch='//', label="TMS", error_kw=dict(elinewidth=1,ecolor='black'))
		
		if(algorithm == "TMS-DDRX"):
			ax.bar(x+0.15, coverage_values, align='center', yerr=confidence_intervals, color=COLORS[algorithm], width=0.3, hatch='\\', label="TMS-DDRX", error_kw=dict(elinewidth=1,ecolor='black'))
	
	ax.legend(loc=2, ncol=2, fancybox=True)
	
	ax.set_ylabel(u"Cobertura (%)")
	ax.set_xlabel(u"Densidade (veiculos/km²")
	
	yticks = np.arange(0, 120, 20)
	ax.set_yticks(yticks)
	ax.set_ylim(0,118)
	
	ax.set_xticks(x)
	ax.set_xticklabels(TRAFFICS)
	ax.set_xlim(1.4,6.6)
	
	ax.set_axisbelow(3)
	plt.grid()
	
	fig = plt.gcf()
	fig.set_size_inches(7.8, 6.1) #x, y
	fig.savefig('tms_cobertura' + formato, dpi=200)
	
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
		
		x = np.arange(2, 7, dtype=np.float)
		ax = plt.subplot(111)
		
		if(algorithm == "TMS"):
			ax.bar(x-0.15, transmitted_values, align='center', yerr=confidence_intervals, color=COLORS[algorithm], width=0.3, hatch='//', label="TMS", error_kw=dict(elinewidth=1,ecolor='black'))
		
		if(algorithm == "TMS-DDRX"):
			ax.bar(x+0.15, transmitted_values, align='center', yerr=confidence_intervals, color=COLORS[algorithm], width=0.3, hatch='\\', label="TMS-DDRX", error_kw=dict(elinewidth=1,ecolor='black'))
	
	ax.legend(loc=2, ncol=2, fancybox=True)
	
	ax.set_ylabel(u"Número de pacotes transmitidos (%)")
	ax.set_xlabel(u"Densidade (veiculos/km²")
	
	#yticks = np.arange(0, 105, 10)
	#ax.set_yticks(yticks)

	ax.set_xticks(x)
	ax.set_xticklabels(TRAFFICS)
	ax.set_xlim(1.4,6.6)
	
	ax.set_axisbelow(3)
	plt.grid()
	
	fig = plt.gcf()
	fig.set_size_inches(7.8, 6.1) #x, y
	fig.savefig('tms_transmitidos' + formato, dpi=200)
	
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
						if int(line.split()[5]) > 300:
							tempoTotal += int(line.split()[6]) + int(line.split()[5])
						else:
							tempoTotal += int(line.split()[6])

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
			ax.bar(x-0.2, coverage_values, align='center', yerr=confidence_intervals, color=COLORS[algorithm], width=0.2, hatch='', label="Mobilidade", error_kw=dict(elinewidth=1,ecolor='black'))
			
		if(algorithm == "TMS"):
			ax.bar(x, coverage_values, align='center', yerr=confidence_intervals, color=COLORS[algorithm], width=0.2, hatch='//', label="TMS", error_kw=dict(elinewidth=1,ecolor='black'))
			
		if(algorithm == "TMS-DDRX"):
			ax.bar(x+0.2, coverage_values, align='center', yerr=confidence_intervals, color=COLORS[algorithm], width=0.2, hatch='\\', label="TMS-DDRX", error_kw=dict(elinewidth=1,ecolor='black'))
		
	#ax.legend(numpoints=1, loc='upper center', ncol=3, fancybox=True, bbox_to_anchor=(0.5, +1.15))
	ax.legend(loc=2, ncol=3, fancybox=True)
	
	ax.set_ylabel(u"Tempo total de viagem (minutos)")
	ax.set_xlabel(u"Densidade (veiculos/km²")

	#yticks = np.arange(0, 105, 10)
	#ax.set_yticks(yticks)

	ax.set_xticks(x)
	ax.set_xticklabels(TRAFFICS)
	ax.set_xlim(1.4,6.6)

	ax.set_axisbelow(3) #grid atras
	plt.grid()
	
	fig = plt.gcf()
	fig.set_size_inches(7.8, 6.1) #x, y
	fig.savefig('tms_tempoTotal' + formato, dpi=200)
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
			ax.bar(x-0.2, distance_values, align='center', yerr=confidence_intervals, color=COLORS[algorithm], width=0.2, hatch='', label="Mobilidade", error_kw=dict(elinewidth=1,ecolor='black'))
			
		if(algorithm == "TMS"):
			ax.bar(x, distance_values, align='center', yerr=confidence_intervals, color=COLORS[algorithm], width=0.2, hatch='//', label="TMS", error_kw=dict(elinewidth=1,ecolor='black'))
			
		if(algorithm == "TMS-DDRX"):
			ax.bar(x+0.2, distance_values, align='center', yerr=confidence_intervals, color=COLORS[algorithm], width=0.2, hatch='\\', label="TMS-DDRX", error_kw=dict(elinewidth=1,ecolor='black'))
	
	
	ax.legend(numpoints=1, loc='upper center', ncol=3, fancybox=True, bbox_to_anchor=(0.5, +1.15))
	#ax.legend(loc=2, ncol=2, fancybox=True)
	
	ax.set_ylabel(u"Distância total (km)")
	ax.set_xlabel(u"Densidade (veiculos/km²")
	
	#yticks = np.arange(0, 105, 10)
	#ax.set_yticks(yticks)

	ax.set_xticks(x)
	ax.set_xticklabels(TRAFFICS)
	ax.set_xlim(1.4,6.6)
	
	ax.set_axisbelow(3) #grid atras
	plt.grid()

	fig = plt.gcf()
	fig.set_size_inches(7.8, 6.1) #x, y
	fig.savefig('tms_distanciaTotal' + formato, dpi=200)

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
				if replication == int(line.split()[0]):
					#print(traffic , " - " , replication , file_input_name , line)
					if line.split()[2] != "0":
						if int(line.split()[5]) > 300:
							#print (algorithm, traffic, replication, "START_TIME MAIOR.")
							tempoCongestionamento += int(line.split()[2]) + int(line.split()[5])
						else:
							tempoCongestionamento += int(line.split()[2])
				
				else:
				# CHANGED
					if not tempoCongestionamento == 0:
						values.append(tempoCongestionamento)
						tempoCongestionamento = 0
				
				while replication != int(line.split()[0]):
					replication += 1

			#print (algorithm, traffic, np.mean(tempoCongestionamento))
			values = np.divide(values,traffic)
			values = np.divide(values,60)
			
			congestion_values.append(np.mean(values))
			confidence_intervals.append(confidence_interval(values))
		
		x = np.arange(2, 7, dtype=np.float)
		ax = plt.subplot(111)
		
		if(algorithm == "Mobilidade"):
			ax.bar(x-0.2, congestion_values, align='center', yerr=confidence_intervals, color=COLORS[algorithm], width=0.2, hatch='', label="Mobilidade", error_kw=dict(elinewidth=1,ecolor='black'))
		
		if(algorithm == "TMS"):
			ax.bar(x, congestion_values, align='center', yerr=confidence_intervals, color=COLORS[algorithm], width=0.2, hatch='//', label="TMS", error_kw=dict(elinewidth=1,ecolor='black'))
			
		if(algorithm == "TMS-DDRX"):
			ax.bar(x+0.2, congestion_values, align='center', yerr=confidence_intervals, color=COLORS[algorithm], width=0.2, hatch='\\', label="TMS-DDRX", error_kw=dict(elinewidth=1,ecolor='black'))
	
	ax.legend(loc=2, ncol=3, fancybox=True)
	
	ax.set_ylabel(u"Tempo de Congestionamento (minutos)")
	ax.set_xlabel(u"Densidade (veiculos/km²")
	
	#yticks = np.arange(0, 105, 10)
	#ax.set_yticks(yticks)

	ax.set_xticks(x)
	ax.set_xticklabels(TRAFFICS)
	ax.set_xlim(1.4,6.6)
	
	ax.set_axisbelow(3)
	plt.grid()
	
	fig = plt.gcf()
	fig.set_size_inches(7.8, 6.1) #x, y
	fig.savefig('tms_tempoCongestionamento' + formato, dpi=200)
	
	plt.show()

if __name__ == "__main__":
	pass
	print "\n *** TMS ***"
	
	'''
	plot_cobertura()
	plot_transmitidos();
	'''
	
	print "\nGrafico de TEMPO TOTAL DE VIAGEM..."
	plot_tempoTotal()
	
	print "\nGrafico de DISTANCIA TOTAL..."
	plot_distanciaTotal()
	
	print "\nGrafico de TEMPO DE CONGESTIONAMENTO..."
	plot_tempoCongestionamento()
	