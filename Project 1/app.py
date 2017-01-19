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




#calculates the number of ticks until the next packet is sent out
def calc_arrival_time(lambda_factor):
 u= random.random() #generate random number between 0...1
 arrival_time = ((-1/lambda_factor) * math.log(1-u) * 1000000)
 #return arrival_time
 return math.floor(random.random() * 4)


#create a packet, given the arrival time, packet size(default to 1) and the tick it was created on
def create_new_packet(tick, interarrival_time, packet_size = packet_length):
    return Packet(tick,interarrival_time, packet_size)

#
def packet_generator(tick,next_packet_arrive_tick, next_packet_departure_tick):
    if tick >= next_packet_arrive_tick:
        arrival_time = calc_arrival_time(1)
        packet = create_new_packet(tick, arrival_time)
        packet_queue.append(packet)

        next_packet_arrive_tick = tick + arrival_time
        #calculate when next packet is serviced
        next_packet_departure_tick = tick + (packet.get_packet_size() / transmission_rate)
        print "Packet Arrived: " + str(packet)

    return next_packet_arrive_tick, next_packet_departure_tick

def packet_server(tick, next_packet_departure_time):
 if tick >= next_packet_departure_time and len(packet_queue) > 0:
     packet = packet_queue.pop()
     packet.finished_processing(tick)
     print "Packet Serviced: " + str(packet)
     packet_finished_queue.append(packet)






t_arrival = calc_arrival_time(1) #calculate first packet arrival time
for tick in range(0, num_of_ticks+1):
   packet_arrival_time, packet_departure_time = packet_generator(tick,packet_arrival_time, packet_departure_time)
   packet_server(tick,packet_departure_time)

#create_report()