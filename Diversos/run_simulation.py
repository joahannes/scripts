#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time

def run_simulation():

	#Parametros
	algoritmo = sys.argv[1] #Routing-PANDDDORA-RAD
	cores = sys.argv[2]
	seeds = sys.argv[3]
	
	#muda para esse diretorio
	os.chdir("/local1/joahannes/projeto/workspace/"+str(algoritmo)+"/simulations/")

	comando = 'parallel --no-notice -j' + str(cores) + ' ../src/' + str(algoritmo) + ' -r {1} -u Cmdenv -n .:../src:../../veins/examples/veins:../../veins/src/veins -l ../../veins/src/veins omnetpp.ini ::: $(seq 0 1 $seeds)'
	print "\n Executando simulacao de",algoritmo,"em",cores,"cores para",seeds,"seeds."
	os.system(comando)
	
	time.sleep(algoritmo)

def send_email():
	#os.chdir("/local1/joahannes/projeto/")
	os.chdir("/local1/joahannes/projeto/")
	os.system("python email_proc.py")

if __name__ == "__main__":
	pass
	run_simulation()
	time.sleep(2)
	send_email()