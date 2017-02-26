#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, getopt

from Node import Packet_Server

def main(argv):
    #These are the values needed to find in the simulation
    #Average Packet Sojourn Time
    E_T = 0.0
    #Average number of packets in queue
    E_N = 0.0
    #Percentage of simulation that packet server is idle
    P_idle = 0.0
    #Percentage of packets lost in simulation
    P_lost = 0.0


    time_to_ticks = 1e6
    total_ticks = int(1e7)  # TICK
    lambda_factor = 700  # λ
    packet_size = 2000  # L
    transmission_rate = 1e6  # c
    queue_limit_size = -1
    number_of_computers =  4 #N




    service_time = (packet_size / transmission_rate) * time_to_ticks

    #initialize the packet server
    packet_server = Packet_Server(queue_size=queue_limit_size,
                                  service_period=service_time,
                                  time_to_ticks=time_to_ticks,
                                  lambda_factor=lambda_factor)

    #run the simulation five times
    for i in range(0,5):
        results = packet_server.run_simulation(total_ticks=total_ticks)

        #get stats for the simulation
        average_sojourn_time = results[0]
        percentage_packet_lost = results[1]
        average_packets_in_queue = results[2]
        percentage_of_idle_time =  results[3]

        E_T += average_sojourn_time
        E_N += average_packets_in_queue
        P_idle += percentage_of_idle_time
        P_lost += percentage_packet_lost

    #take average of five simulation
    E_T /= 5.0
    E_N /= 5.0
    P_idle /= 5.0
    P_lost /= 5.0
    #print it to console to show the values for the simulation
    print E_N, E_T, P_idle, P_lost

if __name__ == "__main__":
    main(sys.argv[1:])