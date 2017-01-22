#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
import random
import numpy

from packet import Packet
from Queue import Queue


#represents when the next packet arrives into the queue
packet_arrival_time = 12
#represents when the next packet leaves the queue
packet_departure_time = -1
#counter which represents the total waiting time for a packet from arrival to departure of the queue
packet_waiting_time = 0
total_soujourn_time = 0
total_packets_departed = 0
total_packets_enqueued = 0
total_packets_enqueued_over_ticks = 0

test = True

#constants to convert between units of time and ticks
time_to_ticks = 1e7

if test:
    total_ticks = 10000000
    lambda_factor = 100
    packet_size = 2000
    transmission_rate = 1e6
    queue_limit_size = -1
else:
    total_ticks = int(raw_input("Number of Ticks: ")) #TICK
    lambda_factor = float(raw_input("Lambda: ")) #λ
    packet_size = int(raw_input("Packet Length: ")) #L
    transmission_rate = int(raw_input("Transmission Rate: ")) #c
    queue_limit_size = -1
    queue_limit = raw_input("Queue Limit [Y/N]?") #K
    queue_limit = (queue_limit == 'Y' or queue_limit == 'y')

    if queue_limit:
        queue_limit_size = int(raw_input("Queue Length"))

#round up the service time, if service time is 4.322 for example, that still takes 5 ticks
service_time = (packet_size/transmission_rate)*time_to_ticks


packet_queue = Queue(limit=queue_limit_size)




#stats
total_packets_enqueued = 0
total_packets_generated = 0
idle_tick_count = 0
packets_dropped = 0



t_departure_tick = -1
t_arrival_tick = 0


def random_uniform():
    return random.uniform(0,1)

#calculates the number of ticks until the next packet is sent out
def calc_arrival_time():

    u = random_uniform() #generate random number between 0...1
    arrival_time = (-1/float(lambda_factor)) * math.log(1.0-u) * time_to_ticks
    #return arrival_time
    return arrival_time


#create a packet, given the arrival time, packet size(default to 1) and the tick it was created on
def create_new_packet(tick, interarrival_time):
    return Packet(tick)

#
def generate_packet(current_tick):
    global packet_queue
    global total_packets_enqueued
    global total_packets_enqueued_over_ticks
    global total_packets_generated
    global packets_dropped
    global t_arrival_tick
    global t_departure_tick
    global idle_tick_count
    global packet_waiting_time

    #get current number of packets in the queue and add it to our running counter
    current_packets_in_queue = packet_queue.size
    total_packets_enqueued_over_ticks += current_packets_in_queue


    # check if queue is empty, if it is, the queue is idle
    if len(packet_queue) == 0 and current_tick > t_departure_tick:
        idle_tick_count += 1
    #check if its time to create a packet
    if current_tick >= t_arrival_tick:
        #update our arrival tick counter, this is the tick when the next packet is created
        t_arrival_tick += calc_arrival_time()

        #new packet object created with current_tick as the tick it was created at
        packet = Packet(current_tick)

        #enqueue the packet and calculate when the next packet is sent
        #packet_waiting_time is a variable holding the wait time in ticks until a new packet can be serviced
        packet.packet_service_start_tick = current_tick + packet_waiting_time
        #try to enqueue the packet, if the packet is full then the packet is dropped
        enqueue_success = packet_queue.enqueue(packet)
        total_packets_generated += 1
        if(enqueue_success):
            total_packets_enqueued += 1
            # delay time for next packet arriving in queue is increased with a new packet waiting in the queue
            packet_waiting_time += service_time
            if packet_queue.size == 1:
                t_departure_tick = current_tick + service_time
        else:
            packets_dropped += 1











def service_packet(current_tick):
     global packet_waiting_time
     global total_soujourn_time
     global t_departure_tick
     global total_packets_departed


     if current_tick >= t_departure_tick:
         packet = packet_queue.dequeue()
         if packet:
            delay = packet.finished_processing(current_tick)
            packet_waiting_time -= service_time
            total_soujourn_time += delay
            total_packets_departed += 1

            #after we service a packet, check to see if more packets are in queue
            #if so update next departure time
            next_packet = packet_queue.front()
            if next_packet != False:
                t_departure_tick += service_time






E_T = 0.0
E_N = 0.0
P_idle = 0.0
P_lost = 0.0
for i in range(0,5):
    t_arrival_tick = calc_arrival_time() #calculate first packet arrival time
    for tick in range(0, total_ticks):
       generate_packet(current_tick=tick)
       service_packet(current_tick=tick)


    average_sojourn_time = (float(total_soujourn_time)/time_to_ticks)/float(total_packets_departed)
    percentage_packet_lost = 100*float(packets_dropped)/total_packets_generated
    average_packets_in_queue = 100*total_packets_enqueued_over_ticks/float(total_ticks)
    percentage_of_idle_time = 100*float(idle_tick_count)/total_ticks
    E_T += average_sojourn_time
    E_N += average_packets_in_queue
    P_idle += percentage_of_idle_time
    P_lost += percentage_packet_lost
E_T /= 5.0
E_N /= 5.0
P_idle /= 5.0
P_lost /= 5.0

print E_N, E_T, P_idle, P_lost

#create_report()