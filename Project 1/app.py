import math
import random
import numpy

from packet import Packet
packet_queue = []

num_of_ticks = 100
remove_next_packet = -1

def calc_arrival_time(lambda_factor):
 u= uniform_rv_generator() #generate random number between 0...1
 arrival_time = ((-1/lambda_factor) * math.log(1-u) * 1000000)
 return arrival_time

#this is our packet generator
def generate_new_packet(tick, packet_size = 1):
    return Packet(tick,packet_size)

#def arrival(tick):
 #if t >= packet_arrival_time:
  #packet_queue.append(new_packet)
  #t_arrival= t + calc_arrival_time()
  #t_departure= t+ (packet_size/transmission_rate) #Also need to consider packet loss case when queue is full


#def departure():
 #if t>=t_departure:
  #packet_queue.pop()


def uniform_rv_generator():
    return random.random()



t_arrival = calc_arrival_time(100) #calculate first packet arrival time
add_next_packet = math.floor(uniform_rv_generator() * 3)
for tick in range(0, num_of_ticks+1):
    if add_next_packet == tick:
        add_next_packet = tick + math.floor(uniform_rv_generator() * 30)
        packet = generate_new_packet(tick,packet_size=tick)
        packet_queue.append(packet)
        print packet
    #arrival(tick)
   #departure()

#create_report()