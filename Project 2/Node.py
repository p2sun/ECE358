import math
import random

from Frame import Frame
from Queue import Queue


class Node:
    def __init__(self, node_id, num_nodes, transmission_delay, time_to_ticks, arrival_rate, persistent, medium):
        self.node_id = node_id
        self.num_nodes = num_nodes
        self.frame_queue = Queue()
        # average time required to transmit a frame
        self.transmission_delay = transmission_delay
        # the number of ticks in a second
        self.time_to_ticks = time_to_ticks
        # lambda
        self.lambda_factor = arrival_rate
        self.persistent = persistent
        self.medium = medium

        self.total_frames_successfully_sent = 0
        self.total_frames_transmission_delay = 0


        self.next_frame_generated = -1

        self.wait_ends_tick = 0
        # State of computer is Idle , Sensing, Wait, Transmit, Backoff
        self.state = "Idle"
        # The tick when the sensing of the medium ends
        self.sensing_ends_tick = -1
        # The current frame being transmitted
        self.frame_transmitted = None
        # Boolean value for when a collision occurs outside the immediate medium
        self.collision_occured = False
        # The tick when backoff state ends
        self.backoff_ends_tick = -1
        # Counter for the number of frame errors
        self.frame_errors = 0
        # Constant value for when the length of sensing which is 1 tick
        self.sensing_tick_duration = 1
        # When the current frame's transmission ends
        self.transmission_ends_tick = 0
        self.medium_in_use = False
        self.physical_layer_used_by = -1

        self.transmission_begins = -1
        # Tick when the  transmission state ends
        self.transmission_ends_tick = -1

        # Tick when the immediate medium is busy until
        self.physical_layer_busy_until = -1
        # Tick when the hub is busy until
        self.hub_busy_until = -1
        # The ID of the Node that the frame is being sent to
        self.transmission_destination = -1
        # Transmission state, 0 when not transmitting, 1 when transmitting on immediate medium
        # 2 when transmitting on hub, 3 when transmitting on destination medium
        self.transmission_state = 0

    def get_transmission_end(self):
        return self.transmission_ends_tick

    def set_next_frame_generated_tick(self, current_tick):
        u = random.uniform(0, 1)  # generate random number between 0...1
        tick_duration = (-1 / float(self.lambda_factor)) * math.log(1.0 - u) * self.time_to_ticks
        # return arrival_time
        self.next_frame_generated = current_tick + tick_duration

    def set_random_frame_destination(self):
        destination = random.randint(0,self.num_nodes-1)
        self.transmission_destination = destination

    def get_frame_destination(self):
        return self.transmission_destination

    def get_transmission_state(self):
        return self.transmission_state

    def get_node_id(self):
        return self.node_id
    #
    # METHOD
    # DESCRIPTION - simulates the generation of a frame, given the current tick, it will update the simulation values
    # PARAMETERS - current tick, the current tick of the simulation
    # RETURNS - Nothing
    def generate_frame(self, current_tick):

        #check if its time to create a frame
        if current_tick >= self.next_frame_generated:
            # update our arrival tick counter, this is the tick when the next frame is created
            self.set_next_frame_generated_tick(current_tick)
            # new frame object created with current_tick as the tick it was created at
            frame = Frame(current_tick)
            # enqueue the frame
            self.frame_queue.enqueue(frame)



    def get_wait_duration(self):
        if self.persistent:
            return 0
        else:
            return 1

    def collision_happened(self, current_tick):
        wait_time = self.frame_transmitted.collision_occured()
        self.transmission_state = 0
        if wait_time < 0:
            # if the wait time is less than 0, then we've exceeded 10 tries, frame error occured
            self.frame_errors += 1
            # go back to idle state
            self.state = "Idle"

        else:
            # go back to backoff state
            self.state = "Backoff"
            self.backoff_ends_tick = current_tick + wait_time

    def sense_medium_busy(self, current_tick):
        return self.medium.sense_medium(self.node_id, current_tick=current_tick)


    def update_state(self, current_tick):
        self.medium.check_medium(current_tick=current_tick)
        if self.state == "Idle":
            # Check if there are frames waiting to be transmitted
            next_frame = self.frame_queue.dequeue()
            if next_frame != False:
                self.frame_transmitted = next_frame
                self.state = "Sensing"
                self.sensing_ends_tick = current_tick + self.sensing_tick_duration


        if self.state == "Sensing":
            if current_tick == self.sensing_ends_tick:
                medium_busy = self.sense_medium_busy(current_tick)
                if medium_busy:
                    self.state = "Wait"
                    self.wait_ends_tick = current_tick + self.get_wait_duration()
                else:
                    # we can start transmission starting the next tick
                    self.state = "Transmit"
                    # set when the end ticks for each stage of transmission
                    # end tick for immediate physical layer
                    self.transmission_state = 1
                    self.transmission_begins = current_tick + 1
                    self.transmission_ends_tick = current_tick + self.transmission_delay + 1
                    # end tick for hub
                    self.physical_layer_busy_until = current_tick + self.transmission_delay * 1/3 + 1
                    # end tick for destination physical layer
                    self.hub_busy_until = current_tick + self.transmission_delay * 2/3 + 1
                    # set a random destination of transmission
                    self.set_random_frame_destination()

        elif self.state == "Wait":
            if current_tick == self.wait_ends_tick:
                medium_busy = self.sense_medium_busy(current_tick=current_tick)
                if medium_busy:
                    self.wait_ends_tick = current_tick + self.get_wait_duration()
                else:
                    self.state = "Sensing"
                    self.sensing_ends_tick = current_tick + self.sensing_tick_duration
        elif self.state == "Transmit":
            # if medium is busy, when we try to transmit a frame or when a collision has already occured
            # we go to the backoff state
            if self.transmission_state == 1:
                if current_tick == self.transmission_begins:
                    transmit_success = self.medium.transmit_frame_on_layer(current_tick=current_tick, node_id=self.node_id,
                                                    busy_until=self.physical_layer_busy_until)
                    if transmit_success == False:
                        self.collision_happened(current_tick)


                if current_tick > self.transmission_begins and current_tick < self.physical_layer_busy_until:
                    if self.medium.check_collision(self.node_id):
                        self.collision_happened(current_tick)


                if current_tick == self.physical_layer_busy_until:
                    if self.medium.state_changed(self.node_id):
                        self.transmission_state = 2
                    else:
                        self.collision_happened(current_tick)

            if self.transmission_state == 2:
                if current_tick == self.hub_busy_until:
                    self.transmission_state = 3
            if self.transmission_state == 3:
                if current_tick == self.hub_busy_until + 1:
                    transmit_success = self.medium.transmit_frame_on_layer(current_tick=current_tick,
                                                                           node_id=self.transmission_destination,
                                                                           busy_until=self.transmission_ends_tick)
                    if transmit_success == False:
                        self.collision_happened(current_tick)

                if current_tick > self.hub_busy_until + 1 and current_tick < self.transmission_ends_tick:
                    if self.medium.check_collision(self.transmission_destination):
                        self.collision_happened(current_tick)

                if current_tick == self.transmission_ends_tick:
                    if self.medium.state_changed(self.node_id):
                        # if transmission is finished, update the total transmission delay
                        # and total number of successful frames transmitted
                        self.transmission_state = 0
                        delay = self.frame_transmitted.finished_transmission(current_tick)
                        self.total_frames_transmission_delay += delay
                        self.total_frames_successfully_sent += 1
                        self.transmission_state = 4
                        self.state = "Idle"
                    else:
                        self.collision_happened(current_tick)

        elif self.state == "Backoff":
            # stay in the backoff state, until the backoff delay is finished
            # then go back to the sensing state
            if current_tick == self.backoff_ends_tick:
                self.state = "Sensing"
                self.sensing_ends_tick = current_tick + self.sensing_tick_duration

    #
    # METHOD
    # DESCRIPTION - returns the result of the simulation in an array
    # PARAMETERS - total_ticks, the number of ticks the simulation was run for
    # RETURN - array of two values, the amount of frames the computer recieved, the total sum of the transmission delay
    #           of these frames
    def get_simulation_results(self):
        total_frames_transmitted = self.total_frames_successfully_sent
        total_frames_transmission_delay = self.total_frames_transmission_delay
        return [total_frames_transmitted, total_frames_transmission_delay]

    #
    # METHOD -  run_simulation
    # DESCRIPTION - runs the simulation of a server and frame generator configuration
    # PARAMETERS - total_ticks is the number of ticks the simulation is run for
    #
    def run_node(self, current_tick):
        #clear all the variables used in the simulation
        self.generate_frame(current_tick)
        self.update_state(current_tick)



