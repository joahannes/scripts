# -*- coding: UTF-8 -*-

from __future__ import division

import math
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

ALGORITHMS = ("DDRX", "Flooding") #
TRAFFICS = (100,200,300,400,500,600,700) #
COLORS = {"DDRX" : "#42413e", "Flooding" : "#efc034"} #

#CONFIDENCE INTERVAL - BAR ERROR
def confidence_interval(values):
    N = len(values)
    Z = 1.96
    std_dev = np.std(values)
    std_error = std_dev / math.sqrt(N)
    return Z * std_error

def plot_barra():

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

			#print(algorithm, " - values: ",values)
			values = np.divide(values,traffic)
			#print(algorithm, " - divide: ", np.divide(values,traffic))
			values = np.multiply(values,100)
			#print(algorithm, " - multiply: ", np.multiply(values,100))

			coverage_values.append(np.mean(values))
			#print(algorithm, " - mean:", np.mean(values))
			confidence_intervals.append(confidence_interval(values))
			#print(algorithm, " - confidence: ", confidence_interval(values))

		x = np.arange(2, 9, dtype=np.float)
		ax = plt.subplot(111)
		if(algorithm == "DDRX"):
			ax.bar(x-0.15, coverage_values, align='center', yerr=confidence_intervals, color=COLORS[algorithm], width=0.3, hatch='//', label="DDRX", error_kw=dict(elinewidth=1,ecolor='black'))

        if(algorithm == "Flooding"):
	        	ax.bar(x+0.15, coverage_values, align='center', yerr=confidence_intervals, color=COLORS[algorithm], width=0.3, hatch='\\', label="Flooding", error_kw=dict(elinewidth=1,ecolor='black'))

	ax.legend(numpoints=1, loc='upper center', ncol=2, fancybox=True, bbox_to_anchor=(0.5, +1.1))

	ax.set_ylabel(r"Cobertura (%)")
	ax.set_xlabel(u"Densidade (veiculos/km²")

	yticks = np.arange(0, 105, 10)
	
	ax.set_yticks(yticks)
	ax.set_xticks(x)
	ax.set_xticklabels(TRAFFICS)
	ax.set_xlim(1.3,8.7)

	ax.set_axisbelow(3)
	plt.grid()
	
	fig = plt.gcf()
	fig.set_size_inches(6.8, 5.5)
	fig.savefig('cobertura_barra.eps', format='eps', dpi=200)
	fig.savefig('cobertura_barra.png', format='png', dpi=200)

	plt.show()

	image_file = Image.open("cobertura_barra.png") # open colour image
	image_file = image_file.convert('L') # convert image to black and white
	image_file.save('cobertura_barra.png')

if __name__ == "__main__":
    pass
    print "Plotando grafico de BARRAS..."
    plot_barra()