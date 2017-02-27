from Node import Node
from Medium import Medium

class Network:
    def __init__(self, number_of_nodes, packet_arrival_rate, LAN_speed, packet_length, time_to_ticks,
                    total_ticks, transmission_delay, persistent):
        self.num_nodes = number_of_nodes
        self.packet_arrival_rate = packet_arrival_rate
        self.LAN_speed= LAN_speed
        self.packet_length = packet_length
        self.total_ticks = total_ticks
        self.time_to_ticks = time_to_ticks
        self.persistent = persistent
        self.transmission_delay = transmission_delay / time_to_ticks
        self.transmission_medium = None
        # list of all the nodes in the network
        self.node_list = []
        self.node_physical_layer = []



        self.frame_transmitted = 0
        self.total_frame_transmission_delay = 0




    def run_simulation(self):

        #initialize/reset all variables of simulation
        self.frame_transmitted = 0
        self.total_frame_transmission_delay = 0
        self.transmission_medium = Medium(N=self.num_nodes)

        # list of each node's state of transmitting a frame
        # -1 -> not transmitting, immediate physical layer is free
        # ID of Node -> transmitting on immediate physical layer
        self.node_list = []
        for i in xrange(0, self.num_nodes):
            node = Node( node_id=i,
                         num_nodes=self.num_nodes,
                         transmission_delay=self.transmission_delay,
                         time_to_ticks=self.time_to_ticks,
                         arrival_rate=self.packet_arrival_rate,
                         persistent=self.persistent,
                         medium = self.transmission_medium)
            node.set_next_frame_generated_tick(current_tick=0)
            self.node_list.append(node)

        for tick in xrange(0,self.total_ticks):
            #iterate through each node and update its state
            for node in self.node_list:
                #run the node during this tick
                node.run_node(current_tick=tick)


        # go through each node and get transmission results
        for node in self.node_list:
            node_stats = node.get_simulation_results()
            self.frame_transmitted += node_stats[0]
            self.total_frame_transmission_delay += node_stats[1]

        throughput = float(self.frame_transmitted * self.packet_length) / float(self.total_ticks * self.time_to_ticks)
        average_delay = float(self.total_frame_transmission_delay) / float(self.frame_transmitted)
        return [throughput, average_delay]






