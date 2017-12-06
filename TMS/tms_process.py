#!/usr/bin/env python

# File name: process_tms.py
# Author: Joahannes Costa
# Data create: 03/12/2017
# Data last modified: 03/12/2017
# Python version: 2.7
# Description: adicionar captura de delay

#import os

ALGORITHMS = ("Routing-PANDDDORA-RAD", "GEDDAI")
TRAFFICS = (700,900,1100,1300,1500)
REPLICATIONS = 10

# (0 REPLICATION, 1 HOST, 2 STOPPED_CONGEST, 3 MESSAGES_RECEIVED, 4 TRANSMITTED, 5 START_TIME, 6 - TOTALTIME, 7 - STOP_TIME, 8 TOTAL_DISTANCE)
def build_summary_files():
	
	for algorithm in ALGORITHMS:
		
		#results_files = os.listdir( algorithm + "/simulations/results/c4/")
		
		for traffic in TRAFFICS:
			
			summary_file = open( algorithm + "/summary-" + str(traffic) + ".txt", "w")
			
			#print (summary_file , "teste")
			
			for replication in range(REPLICATIONS):
				
				sca_file = open( algorithm + "/simulations/results/c4/" + str(traffic) + "-" + str(replication) + ".sca")
				line = sca_file.readline()
				
				#print (replication, line , "teste", sca_file)
				
				while line:
					if "scalar VANET.host" in line:
						line_splited = line.split()
						
						if "stoppedTime:sum" in line:
							host = line_splited[1].split("]")[0][11:]
							summary_file.write(str(replication) + "\t" + host + "\t")
							
							stoppedTime = line_splited[3]
							summary_file.write(stoppedTime + "\t")
						
						if "messagesReceived:sum" in line:
							received = line_splited[3]
							summary_file.write(received + "\t")
							
						if "messagesTransmitted:sum" in line:
							transmitted = line_splited[3]
							summary_file.write(transmitted + "\t")
						
						if "startTime" in line:
							startTime = line_splited[3]
							summary_file.write(startTime + "\t")	

						if "totalTime" in line:
							timeTotal = line_splited[3]
							summary_file.write(timeTotal + "\t")
							
						if "stopTime" in line:
							stopTime = line_splited[3]
							summary_file.write(stopTime + "\t")
							
						if "totalDistance" in line:
							distance = line_splited[3]
							summary_file.write(distance + "\n")
							
					line = sca_file.readline()
					
				sca_file.close()
				
			summary_file.close()
			
if __name__ == "__main__":
	pass
	build_summary_files()
