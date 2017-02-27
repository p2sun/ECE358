from Node import Node

class Network:
    def __init__(self, number_of_nodes, packet_arrival_rate, LAN_speed, packet_length, time_to_ticks, total_ticks,persistent):
        self.num_nodes = number_of_nodes
        self.packet_arrival_rate = packet_arrival_rate
        self.LAN_speed= LAN_speed
        self.packet_length = packet_length
        self.total_ticks = total_ticks
        self.time_to_ticks = time_to_ticks
        self.persistent = persistent
        self.transmission_delay = packet_length / (LAN_speed * time_to_ticks)
        # list of all the nodes in the network
        self.node_list = []
        self.node_states = []

        self.node_using_hub = -1
        self.frame_transmitted = 0
        self.total_frame_transmission_delay = 0




    def run_simulation(self):

        #initialize/reset all variables of simulation
        self.node_using_hub = -1
        self.frame_transmitted = 0
        self.total_frame_transmission_delay = 0

        # list of each node's state of transmitting a frame
        # 0 -> not transmitting, immediate physical layer is free
        # 1 -> transmitting on immediate physical layer
        # 2 -> transmitting
        self.node_states = [0 for i in range(0, self.num_nodes)]

        for i in range(0, self.num_nodes):
            node = Node( node_id=i,
                         num_nodes=self.num_nodes,
                         transmission_delay=self.transmission_delay,
                         time_to_ticks=self.time_to_ticks,
                         arrival_rate=self.packet_arrival_rate,
                         persistent=self.persistent)
            node.set_next_frame_generated_tick(current_tick=0)
            self.node_list.append(node)

        for tick in range(0,self.total_ticks):

            #iterate through each node and update its state
            for node in self.node_list:
                #run the node during this tick
                node.run_node(current_tick=tick)
                #get its transmission state and the destination of current frame is being sent to
                transmission_destination = node.get_frame_destination()
                transmission_state = node.get_transmission_state()

                node_id = node.get_node_id()
                node_current_state = self.node_states[node_id]
                destination_current_state = self.node_states[transmission_destination]
                # assume the initial state of the node's state is 0 before transmission begins
                if transmission_state == 1 and node_current_state == 0:
                    self.node_states[node_id] = 1
                # transmitted across the hub now
                if transmission_state == 2 and node_current_state == 1:
                    #if hub is not busy, the hub is now occupied  by the current node
                    if self.node_using_hub == -1:
                        self.node_using_hub = node_id
                        self.node_states[node_id] = 2
                    else:
                        # collision occured

                        # notify current node and node using hub collision occured
                        node_using_hub = self.node_list[self.node_using_hub]
                        node_using_hub_id = node_using_hub.get_node_id()

                        node_using_hub.set_collision_occured()
                        node.set_collision_occured()

                        # update the list of node states, both aren't transmitting now since they're in backoff mode
                        self.node_states[node_id] = 0
                        self.node_states[node_using_hub_id] = 0
                        self.node_using_hub = -1
                if transmission_state == 3 and node_current_state == 2:
                    destination_node = self.node_list[transmission_destination]
                    # check if destination physical layer is busy, if it is collision has occured
                    if destination_current_state == 1:
                        destination_node.set_collision_occured()
                        node.set_collision_occured()
                        self.node_states[node_id] = 0
                        self.node_states[transmission_destination] = 0
                    else:
                        self.node_states[node_id] = 3
                        physical_layer_busy_until = node.get_transmission_end()
                        destination_node.set_medium_busy(busy_until=physical_layer_busy_until)
        # go through each node and get transmission results
        for node in self.node_list:
            node_stats = node.get_simulation_results()
            self.frame_transmitted += node_stats[0]
            self.total_frame_transmission_delay += node_stats[1]

        throughput = float(self.frame_transmitted * self.packet_length) / float(self.total_ticks * self.time_to_ticks)
        average_delay = float(self.total_frame_transmission_delay) / float(self.frame_transmitted)
        return [throughput, average_delay]






