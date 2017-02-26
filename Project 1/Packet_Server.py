import math
import random

from Packet import Packet
from Queue import Queue


class Packet_Server:
    def __init__(self,queue_size, service_period, time_to_ticks, lambda_factor):
        self.packet_queue = Queue(limit=queue_size)
        #average time required to service a packet
        self.service_time = service_period
        #the number of ticks in a second
        self.time_to_ticks = time_to_ticks
        #lambda
        self.lambda_factor = lambda_factor
        #counts the number of packets currently in the queue
        self.total_packets_enqueued = 0
        #counts the number of packets put into the queue throughout the simulation
        self.total_packets_enqueued_over_ticks = 0
        #counts the number of packets that were generated during the simulation
        self.total_packets_generated = 0
        #counts the total amount of ticks that for all packets to be serviced
        self.total_soujourn_time = 0
        #counts the total number of packets that were sent to the packet queue
        self.total_packets_departed = 0
        #counts the total number of packets dropped during the simulation
        self.packets_dropped = 0
        #the tick for the next packet's arrival
        self.t_arrival_tick = 0
        #the tick for the next packet's departure
        self.t_departure_tick = -1
        #counter for the number of ticks the packet server was idle
        self.idle_tick_count = 0
        #delay between next packet's departure and service time
        self.packet_waiting_time = 0

    def calc_arrival_time(self):
        u = random.uniform(0, 1)  # generate random number between 0...1
        arrival_time = (-1 / float(self.lambda_factor)) * math.log(1.0 - u) * self.time_to_ticks
        # return arrival_time
        return arrival_time

    #
    # METHOD
    # DESCRIPTION - simulates the generation of a packet, given the current tick, it will update the simulation values
    # PARAMETERS - current tick, the current tick of the simulation
    # RETURNS - Nothing
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
            self.t_arrival_tick += self.calc_arrival_time()

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


    #
    # METHOD
    # DESCRIPTION - simulates the servicing of a packet, given the current tick, it will update the simulation values
    # PARAMETERS - current tick, the current tick of the simulation
    # RETURNS - Nothing
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

    #
    # METHOD
    # DESCRIPTION - returns the result of the simulation in an array
    # PARAMETERS - total_ticks, the number of ticks the simulation was run for
    # RETURN - array of 4 values, the average sojourn time, percentage of lost packets, average packets enqueued
    #          and the percentage of simulation idle
    def simulation_results(self, total_ticks):
        average_sojourn_time = (float(self.total_soujourn_time) / self.time_to_ticks) / float(self.total_packets_departed)
        percentage_packet_lost = 100*float(self.packets_dropped) / self.total_packets_generated
        average_packets_enqueued = float(self.total_packets_enqueued_over_ticks) / total_ticks
        percentage_idle = 100 * float(self.idle_tick_count) / total_ticks
        return [average_sojourn_time, percentage_packet_lost, average_packets_enqueued, percentage_idle]

    #
    # METHOD -  run_simulation
    # DESCRIPTION - runs the simulation of a server and packet generator configuration
    # PARAMETERS - total_ticks is the number of ticks the simulation is run for
    #
    def run_simulation(self, total_ticks):
        #clear all the variables used in the simulation
        self.total_packets_enqueued = 0
        self.total_packets_enqueued_over_ticks = 0
        self.total_packets_generated = 0
        self.total_soujourn_time = 0
        self.total_packets_departed = 0
        self.packets_dropped = 0
        self.t_arrival_tick = self.calc_arrival_time()
        self.t_departure_tick = -1
        self.idle_tick_count = 0
        self.packet_waiting_time = 0


        #run the simulation
        for tick in range(0, total_ticks):
           self.generate_packet(current_tick=tick)
           self.service_packet(current_tick=tick)
        return self.simulation_results(total_ticks=total_ticks)