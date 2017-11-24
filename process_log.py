#!/usr/bin/env python

import os

ALGORITHMS = ("CC-DEGREE","DDRX")
TRAFFICS = (100,200,300,400,500,600,700)
REPLICATIONS = 10                

# VARIABLES LOG
# 0 REPLICATION, 1 HOST, 2 LOSS, 3 DELAY, 4 RECEIVED, 5 TRANSMITTED, 6 DUPLICATES, 7 COLLISIONS

def build_summary_files():
    
    for algorithm in ALGORITHMS:
        results_files = os.listdir( algorithm + "/simulations/results")
        for traffic in TRAFFICS:
            summary_file = open( algorithm + "/summary-" + str(traffic) + ".txt", "w")
            
            for replication in range(REPLICATIONS):
                # Get the time the packets was sent by the source vehicle
                sender_times = {}
                for line in open( algorithm + "/simulations/results/" + str(traffic) + "-" + str(replication) + "-sender"):
                    packet_id = int(line.split()[2])
                    packet_sent_time = float(line.split()[0])
                    sender_times[packet_id] = packet_sent_time                    
                                
                sca_file = open( algorithm + "/simulations/results/" + str(traffic) + "-" + str(replication) + ".sca")
                
                line = sca_file.readline()
                
                while line:
                    if "scalar VANET.host" in line:                        
                        line_splited = line.split()
                        
                        if "messagesReceived:sum" in line: #CHANGE: isInROI:sum -> CC-DEGREE and UV-CAST
                            host = line_splited[1].split("]")[0][11:]
                            summary_file.write(str(replication) + "\t" + host + "\t")
                            
                            receiver_file = str(traffic) + "-" + str(replication) + "-receiver-" + str(host)
                                  
                            # Calculate average packet loss and average delay for those that received at least one packet                      
                            if receiver_file in results_files:
                                receiver_times = {}
                                
                                for line in open("./" + algorithm + "/simulations/results/" + receiver_file):
                                    packet_id = int(line.split()[2])
                                    packet_sent_time = float(line.split()[0])
                                    receiver_times[packet_id] = packet_sent_time
                                
                                packet_loss = ((float(len(sender_times) - len(receiver_times))) / float(len(sender_times))) * 100.0
                                
                                delays_sum = 0.0                                
                                for k, v in receiver_times.items():
                                    delays_sum += v - sender_times[k]
                                average_delay = delays_sum / float(len(receiver_times))
                                
                                summary_file.write(str(packet_loss) + "\t" + str(average_delay) + "\t")
                            else:
                                summary_file.write("NA \t NA \t")                                                                                                    
                            
                            received = line_splited[3]
                            summary_file.write(received + "\t")                                                                   
                            
                        if "messagesTransmitted:sum" in line:                        
                            transmitted = line_splited[3]                             
                            summary_file.write(transmitted + "\t")
                            
                        if "duplicatedMessages:sum" in line:                        
                            duplicated = line_splited[3]                             
                            summary_file.write(duplicated + "\t")
                            
                        if "TotalLostPackets" in line: #CHANGE: collisions:sum -> CC-DEGREE and UV-CAST                      
                            lost = line_splited[3]                             
                            summary_file.write(lost + "\n")
                                                                                                                                                             
                    line = sca_file.readline()
                sca_file.close()
            summary_file.close()                                                                                                                                         
    
if __name__ == "__main__":
    pass
    build_summary_files()    
    
