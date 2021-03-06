#!/usr/bin/env python
# -*- coding: utf-8 -*-
from math import log
import random
from collections import deque
import numpy

from packet import Packet

class packet_generator:

    def __init__(self, lambda_factor, packet_size, transmission_rate):
        self.lambda_factor = lambda_factor
        self.packet_size = packet_size
        self.packet_lost = 0
        self.transmission_rate = transmission_rate
        self.service_time = packet_size / transmission_rate
        self.next_packet_arrival = self.calc_arrival_time()
        self.next_packet_departure = -1
        self.packets_generated = 0

    def update_packets_lost(self):
        self.packet_lost += 1

    def get_next_packet_arrival_time(self):
        return self.next_packet_arrival

    #calculates the number of ticks until the next packet is sent out
    def calc_arrival_time(self):
     convert_time_to_ticks =  1e-6
     u = random.random() #generate random number between 0...1
     arrival_time = ((-1/self.lambda_factor) * log(1-u)) / convert_time_to_ticks

     #return arrival_time
     return arrival_time


    #create a packet, given the arrival time, packet size(default to 1) and the tick it was created on
    def create_new_packet(self, current_tick, interarrival_time):
        self.packets_generated += 1
        return Packet(current_tick, self.packet_size)

    #tries to generate a new packet
    def try_generate_packet(self, current_tick):
        if current_tick >= self.get_next_packet_arrival_time():
            next_packet_arrival_tick = current_tick + self.calc_arrival_time()
            next_packet_departure_tick = current_tick + self.service_time

            self.next_packet_arrival = next_packet_arrival_tick
            self.next_packet_departure = next_packet_departure_tick

            packet = self.create_new_packet(current_tick, next_packet_arrival_tick)

            self.packets_generated += 1
            return packet
        return False



class packet_server:

    def __init__(self, queue_size=0, queue_limit=False, transmission_rate=0, packet_size=0):
        self.queue = deque()
        #this is a counter that adds up the number of empty cells in the queue each tick
        self.accumulated_packets_waiting_in_queue = 0

        self.is_queue_limited = queue_limit
        self.queue_size_limit = queue_size
        self.departure_tick = -1
        self.idle_ticks = 0
        self.packets_sent = 0
        self.transmission_rate = transmission_rate
        self.packet_size = packet_size

    def get_accumulated_waiting_queue_size(self):
        return self.accumulated_packets_waiting_in_queue
    def get_average_waiting_queue_size(self, total_tick):
        return float(self.accumulated_packets_waiting_in_queue) / total_tick

    def update_accumulated_waiting_queue_size(self,size):
        self.accumulated_packets_waiting_in_queue += size

    def set_queue_limit(self,queue_limit):
        self.queue_size_limit = queue_limit
        self.is_queue_limited = True

    def get_waiting_packets_in_queue(self):
        return len(self.queue)

    #the generator uses this to set the next departure tick
    def set_next_packet_departure_tick(self, departure_tick):
        self.departure_tick = departure_tick

    #adds a packet to the queue so it waits to be processed by the server
    def add_to_queue(self,packet, current_tick):
        #if the queue has a limit check if its filled
        if self.is_queue_limited:
            #if the number of items in the waiting queue is greater than
            #of equal to the limited size, return False to notify that
            #the packet has been dropped and the operation failed
            if self.get_waiting_packets_in_queue() >= self.queue_size_limit:
                print "Packet Lost"
                return False
            else:
                print "Packet Arrived:"+str(packet)
                self.update_accumulated_waiting_queue_size(1)
                if self.get_waiting_packets_in_queue() == 0:
                    packet.start_server_processing(current_tick)
                    next_departure_tick = current_tick + packet_size/transmission_rate
                    self.set_next_packet_departure_tick(next_departure_tick)
                self.queue.append(packet)
                return True
        #if the queue has no limits, just add it to the waiting queue
        else:
            print "Packet Arrived:" + str(packet)
            self.update_accumulated_waiting_queue_size(1)
            if self.get_waiting_packets_in_queue() == 0:
                packet.start_server_processing(current_tick)
                next_departure_tick = current_tick + packet_size / transmission_rate
                self.set_next_packet_departure_tick(next_departure_tick)
            self.queue.append(packet)
            return True


    def try_processing_packet(self, current_tick):
        if current_tick >= self.departure_tick:
            # to process next packet, the function needs to know what tick its currently on
            packets_waiting = self.get_waiting_packets_in_queue()
            if packets_waiting > 0:
                packet = self.queue.popleft()
                packet.finished_processing(current_tick)
                print "Packet Serviced: " + str(packet)
                print "Current Packets in Queue:" + str(self.get_waiting_packets_in_queue())
                print "Current Accumulated Packets in Queue: " + str(self.get_accumulated_waiting_queue_size())
                self.packets_sent += 1
                packets_waiting -= 1

                # update next departure tick
                if packets_waiting == 0:
                    next_departure_tick = -1
                else:
                    #start processing the next packet, update the departure time to match when that packet is sent
                    next_departure_tick = current_tick + packet_size/transmission_rate
                    #update the packet's start time for when its being processed
                    self.queue[0].start_server_processing(current_tick)

                self.set_next_packet_departure_tick(next_departure_tick)


            else:
                #if there's nothing in the queue, there shouldn't be a departure tick
                self.set_next_packet_departure_tick(departure_tick=-1)
        else:
            #if the queue is empty, then the server is idle
            if self.get_waiting_packets_in_queue() == 0 :
                self.idle_ticks += 1


#used to specify the limit on the queue
packet_queue_limit = -1
#a flag used to represent if we're simulating with a finite queue
finite_queue_size = False

#variables used to hold the next time a packet is generated
packet_arrival_time = 12
#variable used to hold the next time a packet is going to be processed by the server
packet_departure_time = -1

num_of_ticks = int(raw_input("Number of Ticks: ")) #TICK
lambda_factor = float(raw_input("Lambda: ")) #λ
packet_size = int(raw_input("Packet Length: ")) #L
transmission_rate = int(raw_input("Transmission Rate: ")) #c


queue_limit = raw_input("Queue Limit [Y/N]?") #K
queue_limit = (queue_limit == 'Y' or queue_limit == 'y')
if queue_limit:
    queue_limit_size = int(raw_input("Queue Length"))


simulation_packet_generator = packet_generator(lambda_factor=lambda_factor,packet_size=packet_size, transmission_rate=transmission_rate)
simulation_packet_server = packet_server(queue_limit=False, packet_size=packet_size, transmission_rate=transmission_rate)
if queue_limit:
    simulation_packet_server.set_queue_limit(queue_limit_size)



for current_tick in range(0, num_of_ticks+1):

    #call the packet generator to try to generate a packet
    packet = simulation_packet_generator.try_generate_packet(current_tick)

    #if you get a packet, add it to the queue
    if packet != False:

        packet_queued = simulation_packet_server.add_to_queue(packet,current_tick)
        if not packet_queued:
            simulation_packet_generator.update_packets_lost()
    simulation_packet_server.try_processing_packet(current_tick)

accumulated_queue_size = simulation_packet_server.get_accumulated_waiting_queue_size()
average_queue_size = simulation_packet_server.get_average_waiting_queue_size(num_of_ticks)
total_packets_lost = simulation_packet_generator.packet_lost
idle_ticks = simulation_packet_server.idle_ticks

print "Total Number of Packets in Waiting Queue:" + str(accumulated_queue_size)
print "Average Number of Packets in Queue Per Tick:" + str(average_queue_size)
print "Packets Lost: " + str(total_packets_lost)
print "Server Idle: " + str(idle_ticks)
#create_report()