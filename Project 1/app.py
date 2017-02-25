#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
import random
import sys, getopt

from collections import deque

def calc_arrival_time(lambda_factor, time_to_ticks):
    u = random.uniform(0,1)  #generate random number between 0...1
    arrival_time = (-1/float(lambda_factor)) * math.log(1.0-u) * time_to_ticks
    #return arrival_time
    return arrival_time

class Queue:
    def __init__(self, limit = -1):
        self.size = 0
        self.queue = deque()
        self.limit = limit
    def __len__(self):
        return len(self.queue)

    def front(self):
        if self.size > 0:
            return self.queue[0]
        else:
            return False

    def enqueue(self,item):
        #if limit is -1 then its an unlimited queue
        if (self.limit == -1):
            self.size += 1
            self.queue.append(item)
            return True
        #if not the case, then the queue has a limit
        else:
            #only enqueue if the size is less than the limit
            if(len(self.queue) < self.limit):
                #increment the limit
                self.size += 1
                self.queue.append(item)
                return True
            else:
                return False
    def dequeue(self):
        if(self.size > 0):
            #decrement the size counter
            self.size -= 1
            return self.queue.popleft()

        else:
            return False
    def full(self):
        return self.get_size() >= self.limit
    def empty(self):
        return self.size == 0

class Packet:

    def __init__(self, packet_generation_tick):
        self.packet_generation_tick = packet_generation_tick
        self.packet_service_start_tick=-1
        self.packet_service_end_tick = -1


    def finished_processing(self, packet_end_tick):
        self.packet_service_end_tick = packet_end_tick
        return packet_end_tick - self.packet_generation_tick

    def start_processing(self, packet_start_tick):
        self.packet_service_start_tick = packet_start_tick

    def __str__(self):
        return "Tick When Packet Was Generated:"+str(self.packet_generation_tick)\
                +"\nPacket Service Started:" +str(self.packet_service_start_tick) \
                +"\nPacket Service Ended:"+str(self.packet_service_end_tick)+'\n'





class Packet_Server:
    def __init__(self,queue_size, first_packet_arrival_tick, service_period, time_to_ticks, lambda_factor):
        self.packet_queue = Queue(limit=queue_size)
        self.service_time = service_period
        self.time_to_ticks = time_to_ticks
        self.lambda_factor = lambda_factor
        self.total_packets_enqueued = 0
        self.total_packets_enqueued_over_ticks = 0
        self.total_packets_generated = 0
        self.total_soujourn_time = 0
        self.total_packets_departed = 0
        self.packets_dropped = 0
        self.t_arrival_tick = first_packet_arrival_tick
        self.t_departure_tick = -1
        self.idle_tick_count = 0
        self.packet_waiting_time = 0

    def generate_packet(self, current_tick):

        #get current number of packets in the queue and add it to our running counter
        current_packets_in_queue = self.packet_queue.size
        self.total_packets_enqueued_over_ticks += current_packets_in_queue


        # check if queue is empty, if it is, the queue is idle
        if len(self.packet_queue) == 0 and current_tick > self.t_departure_tick:
            self.idle_tick_count += 1
        #check if its time to create a packet
        if current_tick >= self.t_arrival_tick:
            #update our arrival tick counter, this is the tick when the next packet is created
            self.t_arrival_tick += calc_arrival_time(time_to_ticks=self.time_to_ticks, lambda_factor=self.lambda_factor)

            #new packet object created with current_tick as the tick it was created at
            packet = Packet(current_tick)

            #enqueue the packet and calculate when the next packet is sent
            #packet_waiting_time is a variable holding the wait time in ticks until a new packet can be serviced
            packet.packet_service_start_tick = current_tick + self.packet_waiting_time
            #try to enqueue the packet, if the packet is full then the packet is dropped
            enqueue_success = self.packet_queue.enqueue(packet)
            self.total_packets_generated += 1
            if(enqueue_success):
                self.total_packets_enqueued += 1
                # delay time for next packet arriving in queue is increased with a new packet waiting in the queue
                self.packet_waiting_time += self.service_time
                if self.packet_queue.size == 1:
                    self.t_departure_tick = current_tick + self.service_time
            else:
                self.packets_dropped += 1

    def service_packet(self,current_tick):


         if current_tick >= self.t_departure_tick:
             packet = self.packet_queue.dequeue()
             if packet:
                delay = packet.finished_processing(current_tick)
                self.total_soujourn_time += delay
                self.total_packets_departed += 1

                #after we service a packet, check to see if more packets are in queue
                #if so update next departure time
                next_packet = self.packet_queue.front()
                if next_packet != False:
                    self.t_departure_tick += self.service_time

         if self.packet_queue.front() != False:
             self.packet_waiting_time -= 1

    def simulation_results(self):
        average_sojourn_time = (float(self.total_soujourn_time) / self.time_to_ticks) / float(self.total_packets_departed)
        percentage_packet_lost = 100*float(self.packets_dropped) / self.total_packets_generated
        total_packets_enqueue = self.total_packets_enqueued_over_ticks
        idle_ticks = self.idle_tick_count
        return [average_sojourn_time, percentage_packet_lost, total_packets_enqueue, idle_ticks]
E_T = 0.0
E_N = 0.0
P_idle = 0.0
P_lost = 0.0

def main(argv):
    # Initialize and get variables for simulation
    global E_T, E_N, P_idle, P_lost


    time_to_ticks = 1e6
    total_ticks = int(1e7)  # TICK
    lambda_factor = 700  # λ
    packet_size = 2000  # L
    transmission_rate = 1e6  # c
    queue_limit_size = 25



    service_time = (packet_size / transmission_rate) * time_to_ticks

    for i in range(0,5):

        t_arrival_tick = calc_arrival_time(lambda_factor=lambda_factor, time_to_ticks=time_to_ticks) #calculate first packet arrival time
        packet_server = Packet_Server(queue_size = queue_limit_size,
                                      first_packet_arrival_tick=t_arrival_tick,
                                      service_period= service_time,
                                      time_to_ticks = time_to_ticks,
                                      lambda_factor = lambda_factor)
        for tick in range(0, total_ticks):
           packet_server.generate_packet(current_tick=tick)
           packet_server.service_packet(current_tick=tick)


        results = packet_server.simulation_results()

        average_sojourn_time = results[0]
        percentage_packet_lost = results[1]
        average_packets_in_queue = float(results[2]) / total_ticks
        percentage_of_idle_time =  100 * float(results[3]) / total_ticks


        E_T += average_sojourn_time
        E_N += average_packets_in_queue
        P_idle += percentage_of_idle_time
        P_lost += percentage_packet_lost

    E_T /= 5.0
    E_N /= 5.0
    P_idle /= 5.0
    P_lost /= 5.0

    print E_N, E_T, P_idle, P_lost

if __name__ == "__main__":
    main(sys.argv[1:])



