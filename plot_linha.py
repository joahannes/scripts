# -*- coding: UTF-8 -*-

# File name: plot_linha.py
# Author: Joahannes Costa
# Data create: 14/12/2017
# Data last modified: 14/12/2017
# Python version: 2.7
# Description: plota graficos de linha para algoritmos de disseminacao

from __future__ import division

import math
import matplotlib.pyplot as plt
import numpy as np

# summary_file:
# 0 REPLICATION
# 1 HOST
# 2 LOSS
# 3 DELAY
# 4 RECEIVED
# 5 TRANSMITTED
# 6 DUPLICATES
# 7 COLLISIONS

ALGORITHMS = ("DDRX", "CARRO", "UV-CAST", "CC-DEGREE", "Flooding") #
TRAFFICS = (100,200,300,400,500,600,700) #

COLORS = {"DDRX" : "k", "CARRO" : "r", "UV-CAST" : "b", "CC-DEGREE" : "magenta", "Flooding" : "g"}
MARKS = {"DDRX" : "H", "CARRO" : "^", "UV-CAST" : "d", "CC-DEGREE" : "*", "Flooding" : "s"}
LINES = {"DDRX" : "-", "CARRO" : "--", "UV-CAST" : "-.", "CC-DEGREE" : "-", "Flooding" : ":"}

#VARIABLES PLOT
X_LEGEND = u'Densidade (veículos/km$^2$)'
x_lim = 750
x_fig = 6.8 #6.8
y_fig = 5.5 #5.5
formato = '.eps'
legenda_size = 16
#bbox_inches = 'tight', pad_inches = 0.05 -> remove borda desnecessaria da imagem

#CONFIDENCE INTERVAL - BAR ERROR
def confidence_interval(values):
	N = len(values)
	Z = 1.96
	std_dev = np.std(values)
	std_error = std_dev / math.sqrt(N)
	return Z * std_error
	
#COVERAGE
def plot_coverage():
	
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
					if line.split()[4] != "0":
						coverage += int(line.split()[4])
						
				else:
				# CHANGED
					if not coverage == 0:
						values.append(coverage)
						coverage = 0
						
				while replication != int(line.split()[0]):
					replication += 1
			
			values = np.divide(values, traffic)
			values = np.multiply(values, 100)
			
			coverage_values.append(np.mean(values))
			confidence_intervals.append(confidence_interval(values))
			
		plt.errorbar(TRAFFICS, coverage_values, yerr=confidence_intervals, label=algorithm, color=COLORS[algorithm], marker=MARKS[algorithm], linestyle=LINES[algorithm], markersize = 8, linewidth = 2, zorder=3)
	
	yticks = np.arange(90, 102, 2)
	plt.xlabel(X_LEGEND, fontsize=legenda_size)
	plt.ylabel('Cobertura (%)', fontsize=legenda_size)
	plt.xlim(50, x_lim)
	plt.xticks(TRAFFICS, fontsize=legenda_size)
	plt.yticks(yticks, fontsize=legenda_size)

	#plt.yscale("log")
	
	plt.grid()
	plt.legend(numpoints=1, loc=4, fancybox=True)
	
	fig = plt.gcf()
	
	fig.set_size_inches(x_fig, y_fig)   
	fig.savefig('cobertura' + formato, dpi=200, bbox_inches = 'tight', pad_inches = 0.05)
	
	plt.show()
	
#DELAY
def plot_delay():
	
	for algorithm in ALGORITHMS:
		delay_values = []
		confidence_intervals = []
		
		delay = float(0)
		
		for traffic in TRAFFICS:
			values = []
			file_input_name =  algorithm + "/summary-" + str(traffic) + ".txt"
			
			replication = 0
			delay = 0.0
			
			for line in open(file_input_name):
				if replication == int(line.split()[0]): 
					if line.split()[3] != "NA":
						delay += float(line.split()[3])
			
				else:
				# CHANGED
					if not delay == 0.0:
						values.append(delay)
						delay = 0.0
				
				while replication != int(line.split()[0]):
					replication += 1
			
			#values = np.divide(values,traffic)
			#values = np.multiply(values,60)
			
			delay_values.append(np.mean(values))
			confidence_intervals.append(confidence_interval(values))
		
		#print (algorithm, delay_values)	
		plt.errorbar(TRAFFICS, delay_values, yerr=confidence_intervals, label=algorithm, color=COLORS[algorithm], marker=MARKS[algorithm], linestyle=LINES[algorithm], markersize = 8, linewidth = 2, zorder=3)
	
	yticks = np.arange(0, 110, 10)
	plt.xlabel(X_LEGEND, fontsize=legenda_size)
	plt.ylabel('Atraso (s)', fontsize=legenda_size)
	plt.xlim(50, x_lim)
	plt.xticks(TRAFFICS, fontsize=legenda_size)
	plt.yticks(yticks, fontsize=legenda_size)
	
	plt.yscale("log")
	
	plt.grid()    
	plt.legend(numpoints=1, loc=2, fancybox=True)
	
	fig = plt.gcf()
	fig.set_size_inches(x_fig, y_fig)
	fig.savefig('atraso' + formato, dpi=200, bbox_inches = 'tight', pad_inches = 0.05)
	
	plt.show()
	
#PACKETS TRANSMITTED
def plot_transmitted():
	
	for algorithm in ALGORITHMS:
		transmitted_values = []
		confidence_intervals = []
		
		for traffic in TRAFFICS:
			values = []
			file_input_name =  algorithm + "/summary-" + str(traffic) + ".txt"
			
			replication = 0
			transmitted = 0
			
			for line in open(file_input_name):
				if replication == int(line.split()[0]): 
					if line.split()[5] != "0":
						transmitted += int(line.split()[5])
				
				else:
				# CHANGED
					if not transmitted == 0:
						values.append(transmitted)
						transmitted = 0
						
				while replication != int(line.split()[0]):
					replication += 1
			
			#values = np.divide(values,traffic)
			#values = np.multiply(values,100)
			
			transmitted_values.append(np.mean(values))
			confidence_intervals.append(confidence_interval(values))
		
		#print (algorithm, transmitted_values)
		plt.errorbar(TRAFFICS, transmitted_values, yerr=confidence_intervals, label=algorithm, color=COLORS[algorithm], marker=MARKS[algorithm], linestyle=LINES[algorithm], markersize = 8, linewidth = 2, zorder=3)
	
	yticks = np.arange(0, 110, 10)
	plt.xlabel(X_LEGEND, fontsize=legenda_size)
	plt.ylabel('Total de Pacotes Transmitidos', fontsize=legenda_size)
	plt.xlim(50, x_lim)
	plt.xticks(TRAFFICS, fontsize=legenda_size)
	plt.yticks(yticks, fontsize=legenda_size)
	
	plt.yscale("log")
	
	plt.grid()
	plt.legend(numpoints=1, loc=2, fancybox=True)
	
	fig = plt.gcf()
	fig.set_size_inches(x_fig, y_fig)
	fig.savefig('transmitidos' + formato, dpi=200, bbox_inches = 'tight', pad_inches = 0.05)
	
	plt.show()
	
#COLISIONS
def plot_colisions():
	
	for algorithm in ALGORITHMS:
		colisions_values = []
		confidence_intervals = []
		
		for traffic in TRAFFICS:
			values = []
			file_input_name =  algorithm + "/summary-" + str(traffic) + ".txt"
			
			replication = 0
			colisions = 0
			
			for line in open(file_input_name):
				if replication == int(line.split()[0]): 
					if line.split()[7] != "0":
						colisions += int(line.split()[7])
				
				else:
				# CHANGED
					if not colisions == 0:
						values.append(colisions)
						colisions = 0
				
				while replication != int(line.split()[0]):
					replication += 1
			
			#values = np.divide(values,traffic)
			#values = np.multiply(values,100)
			
			colisions_values.append(np.mean(values))
			confidence_intervals.append(confidence_interval(values))
		
		#print (algorithm, colisions_values)
		plt.errorbar(TRAFFICS, colisions_values, yerr=confidence_intervals, label=algorithm, color=COLORS[algorithm], marker=MARKS[algorithm], linestyle=LINES[algorithm], markersize = 8, linewidth = 2, zorder=3)
	
	yticks = np.arange(0, 20, 1)
	plt.xlabel(X_LEGEND, fontsize=legenda_size)
	plt.ylabel(u'Número de Colisões', fontsize=legenda_size)
	plt.xlim(50, x_lim)
	plt.xticks(TRAFFICS, fontsize=legenda_size)
	plt.yticks(yticks, fontsize=legenda_size)
	
	plt.yscale("log")
	
	plt.grid()
	plt.legend(numpoints=1, loc=2, fancybox=True)
	
	fig = plt.gcf()
	fig.set_size_inches(x_fig, y_fig)
	fig.savefig('colisoes' + formato, dpi=200, bbox_inches = 'tight', pad_inches = 0.05)
	
	plt.show()
	
if __name__ == "__main__":
	pass
	
	print("Grafico de COBERTURA...")
	plot_coverage()
	
	print("Grafico de ATRASO...")
	plot_delay()
	
	print("Grafico de PACOTES_TRANSMITIDOS...")
	plot_transmitted()
	
	print("Grafico de COLISOES...")
	plot_colisions()
	