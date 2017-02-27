#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, getopt
from Network import Network

def main():
    #These are the values needed to find in the simulation
    #Throughput of the network
    E_T = 0.0
    #Average number of packets in queue
    E_D = 0.0



    time_to_ticks = 10e-6
    total_ticks = 10000000  # TICK
    lambda_factor = 4  # λ
    packet_size = 8000  # L
    number_of_computers =  4 #N
    LAN_speed = 1000000
    persistent = False




    #initialize the packet server
    network_simulation = Network(number_of_nodes=number_of_computers,
                            packet_arrival_rate=lambda_factor,
                            LAN_speed=LAN_speed,
                            packet_length=packet_size,
                            time_to_ticks=time_to_ticks,
                            total_ticks=total_ticks,
                            transmission_delay= 25.6e-6,
                            persistent=persistent)

    #run the simulation five times
    for i in range(0,3):
        results = network_simulation.run_simulation()
        print results
        throughput = results[0]
        delay = results[1]

        E_T += throughput
        E_D += delay


    #take average of five simulation
    E_T /= 5.0
    E_D /= 5.0

    #print it to console to show the values for the simulation
    print E_T, E_D

main()