#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
import random
import numpy

from packet import Packet
from collections import deque
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


packet_arrival_time = 12
packet_departure_time = -1
packet_waiting_time = 0
total_soujourn_time = 0
total_packets_departed = 0
total_packets_enqueued = 0
total_packets_enqueued_over_ticks = 0

test = True
#constants
time_to_ticks = 1e-6

if test:
    total_ticks = 10000000
    lambda_factor = 350
    packet_size = 2000
    transmission_rate = 8
    queue_limit_size = 10
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
service_time = math.ceil(packet_size/transmission_rate)


packet_queue = Queue(limit=10)




#stats
total_packets_enqueued = 0
idle_tick_count = 0
packets_dropped = 0



t_departure_tick = -1
t_arrival_tick = 0



#calculates the number of ticks until the next packet is sent out
def calc_arrival_time():

    u = random.uniform(0,1) #generate random number between 0...1
    arrival_time = (-1/float(lambda_factor)) * math.log(1-u) / time_to_ticks
    #return arrival_time
    return arrival_time


#create a packet, given the arrival time, packet size(default to 1) and the tick it was created on
def create_new_packet(tick, interarrival_time):
    return Packet(tick,interarrival_time, packet_size)

#
def arrival(current_tick):
    global packet_queue
    global total_packets_enqueued
    global total_packets_enqueued_over_ticks
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

    if current_tick >= t_arrival_tick:
        arrival_time = calc_arrival_time()
        packet = Packet(current_tick)

        #enqueue the packet and calculate when the next packet is sent
        packet.packet_service_start_tick = current_tick + packet_waiting_time
        enqueue_success = packet_queue.enqueue(packet)
        t_arrival_tick = current_tick + arrival_time
        if(enqueue_success):
            total_packets_enqueued += 1
            # delay time for next packet arriving in queue is increased with a new packet waiting in the queue
            packet_waiting_time += service_time
            if packet_queue.size == 1:
                t_departure_tick = current_tick + service_time
        else:
            packets_dropped += 1











def departure(current_tick):
     global packet_waiting_time
     global total_soujourn_time
     global t_departure_tick
     global total_packets_departed



     if current_tick > t_departure_tick:
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







t_arrival_tick = calc_arrival_time() #calculate first packet arrival time
for tick in range(0, total_ticks):
   arrival(current_tick=tick)
   departure(current_tick=tick)


average_sojourn_time = time_to_ticks * total_soujourn_time/float(total_packets_departed)

average_packets_in_queue = 100*total_packets_enqueued_over_ticks/float(total_ticks)
percentage_of_idle_time = 100*float(idle_tick_count)/total_ticks
print "Total Waiting Time: " + str(total_soujourn_time * time_to_ticks)
print "Total Packets in Queue: " + str(total_packets_enqueued)
print "Average Packets in Queue:" + str(average_packets_in_queue)
print "Average Sojourn Time:" + str(average_sojourn_time)

print "Percentage of Packet Loss: " + str(100 * float(packets_dropped) / total_packets_enqueued)
print "Total Idle Time: " + str(percentage_of_idle_time) + '%'

#create_report()