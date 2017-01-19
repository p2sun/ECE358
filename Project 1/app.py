import math
import random
import numpy

from packet import Packet

#queue for packets waiting to be processed
packet_queue = []

#list of all packets that have been processed
packet_finished_queue = []

#used to specify the limit on the queue
packet_queue_limit = -1
#a flag used to represent if we're simulating with a finite queue
finite_queue_size = False

#variables used to hold the next time a packet is generated
packet_arrival_time = 12
#variable used to hold the next time a packet is going to be processed by the server
packet_departure_time = -1
#size of a packet
packet_length = 1
#number of memory units processed per unit of time measure
transmission_rate = 1

#number of ticks in the simulation
num_of_ticks = 100
#number of ticks where the server was idle
idle_ticks = 0



class packet_generator:

    def __init__(self, lambda_factor, packet_size, transmission_rate):
        self.lambda_factor = lambda_factor
        self.packet_size = packet_size
        self.packet_lost = 0
        self.transmission_rate = transmission_rate
        self.service_time = packet_size / transmission_rate
        self.next_packet_arrival = self.calc_arrival_time()

    def set_next_packet_arrival_time(self,arrival_tick):
        self.next_packet_arrival = arrival_tick

    def get_next_packet_arrival_time(self):
        return self.next_packet_arrival

    #calculates the number of ticks until the next packet is sent out
    def calc_arrival_time(self):
     u = random.random() #generate random number between 0...1
     arrival_time = ((-1/self.lambda_factor) * math.log(1-u) * 1000000)

     #return arrival_time
     return math.floor(random.random() * 4)


    #create a packet, given the arrival time, packet size(default to 1) and the tick it was created on
    def create_new_packet(self, current_tick, interarrival_time):
        return Packet(current_tick,interarrival_time, self.packet_size)

    #tries to generate a new packet
    def try_generate_packet(self, current_tick):
        if current_tick >= self.get_next_packet_arrival_time():
            next_packet_arrival_tick = current_tick + self.calc_arrival_time()
            self.set_next_packet_arrival_time( next_packet_arrival_tick )
            packet = self.create_new_packet(current_tick, next_packet_arrival_tick)
            return packet
        return False

class packet_server:

    def __init__(self, queue_size=0, queue_limit=False):
        self.idle_ticks = 0
        self.waiting_queue = []
        #this is a counter that adds up the number of empty cells in the queue each tick
        self.total_waiting_queue_size = 0
        self.processed_queue = []
        self.is_queue_limited = queue_limit
        self.queue_size_limit = queue_size
        self.departure_tick = -1
        self.idle_ticks = 0

    def get_average_waiting_queue_size(self, current_tick):
        return self.total_waiting_queue_size / current_tick
    def update_total_waiting_queue_size(self,size):
        self.total_waiting_queue_size += size

    def get_next_departure_tick(self):
        return self.departure_tick

    def get_waiting_queue_size(self):
        return len(self.waiting_queue)

    def set_next_packet_departure_tick(self, departure_tick):
        self.departure_tick = departure_tick

    #adds a packet to the queue so it waits to be processed by the server
    def add_to_queue(self,packet):
        #if the queue has a limit check if its filled
        if self.is_queue_limited:
            #if the number of items in the waiting queue is greater than
            #of equal to the limited size, return False to notify that
            #the packet has been dropped and the operation failed
            if self.get_waiting_queue_size() >= self.queue_size_limit:
                return False
            else:
                self.waiting_queue.append(packet)
                estimated_processing_time = packet.get_packet_size() /
                return True
        #if the queue has no limits, just add it to the waiting queue
        else:
            self.waiting_queue.append(packet)
            return True

    def process_next_packet_in_queue(self, current_tick):
        if self.get_waiting_queue_size() > 0:
            packet = self.waiting_queue.pop()
            packet.finished_processing(current_tick)
            print "Packet Serviced: " + str(packet)
            self.processed_queue.append(packet)

    def try_processing_packet(self, current_tick):
        if current_tick >= self.get_next_departure_tick():
            # to process next packet, the function needs to know what tick its currently on
            self.process_next_packet_in_queue(current_tick)
        else:
            #if the queue is empty, then the server is idle
            if self.get_waiting_queue_size() == 0 :
                self.idle_ticks += 1






simulation_packet_generator = packet_generator(lambda_factor=3,packet_size=1)
simulation_packet_server = packet_server(queue_limit=False)

for current_tick in range(0, num_of_ticks+1):

    packet = simulation_packet_generator.try_generate_packet(current_tick)
    if packet != False:
        simulation_packet_server.add_to_queue(packet)
        simulation_packet_server.try_processing_packet(current_tick)

#create_report()