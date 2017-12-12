#!/usr/bin/env python

# File name: log_mobilidade.py
# Author: Joahannes Costa
# Data create: 12/12/2017
# Data last modified: 12/12/2017
# Python version: 2.7
# Description: trata arquivos de mobilidade (extract_infos) e gera arquivos (build_summary_files) para plot.
# Obs: colocar na mesma pasta dos traces (.sumo.cfg)

from bs4 import BeautifulSoup
import os

TRAFFICS = (1600,2400,3200,4000,4800)
REPLICATIONS = 5

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

def extract_infos():

	print "Criando diretorio para log..."
	os.system("mkdir log")
	for traffic in TRAFFICS:
		for replication in range(REPLICATIONS):
			os.system("sumo -c "+str(traffic)+"_"+str(replication)+".sumo.cfg --tripinfo-output info_"+str(traffic)+"-"+str(replication)+".xml")
	
	os.system("mv info_* log/")

def build_summary_files():
	
	for traffic in TRAFFICS:
		summary_file = open("log/summary-"+str(traffic)+".txt", "w")

		for replication in range(REPLICATIONS):
			print "Gravando no arquivo:",traffic,replication
			sumo_output_file = open("log/info_"+str(traffic)+"-"+str(replication)+".xml")
			data = sumo_output_file.read()
			sumo_output_file.close()
			soup = BeautifulSoup(data, "xml") 
			
			for trip_tag in soup.findAll("tripinfo"):
				# break
				vehicle = trip_tag["id"]
				travel_time = trip_tag["duration"]
				travel_distance = trip_tag["routeLength"]
				startTime = trip_tag["depart"]
				#waitSteps = trip_tag["waitSteps"]
				lossTime = trip_tag["timeLoss"]
				stopTime = trip_tag["arrival"]
				
				#emissions_tag = trip_tag.find("emissions")
				#co2 = emissions_tag["CO2_abs"]
				#fuel = emissions_tag["fuel_abs"]
				
				#freeflow = float(travel_time) - float(lossTime)
				
				summary_file.write(str(replication)+'\t'+str(vehicle)+'\t'+str(lossTime)+'\t'+'1'+'\t'+'1'+'\t'+str(startTime)+'\t'+str(travel_time)+'\t'+str(stopTime)+'\t'+str(travel_distance)+'\n')

		summary_file.close()
	
if __name__ == "__main__":
	extract_infos()
	build_summary_files()
	print "\nFeito.\n"