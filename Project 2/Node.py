import math
import random

from Frame import Frame
from Queue import Queue


class Node:
    def __init__(self,queue_size, delay, time_to_ticks, arrival_rate, transmission_delay):
        self.frame_queue = Queue(limit=queue_size)
        # average time required to service a frame
        self.transmission_delay = delay
        # the number of ticks in a second
        self.time_to_ticks = time_to_ticks
        # lambda
        self.lambda_factor = arrival_rate
        self.total_frames_successfully_sent = 0
        self.total_frames_transmission_delay = 0

        self.next_frame_generated = 0
        self.wait_ends_tick = 0
        # State of computer is Idle , Sensing, Wait, Transmit, Backoff
        self.state = "Idle"
        self.sensing_ends_tick = 0
        self.frame_transmitted = None
        self.collision_occured = False
        self.backoff_ends_tick = 0
        self.frame_errors = 0
        self.sensing_tick_duration = 1
        self.transmission_ends_tick = 0
        self.transmission_delay = transmission_delay

    def random_poisson_generator(self):
        u = random.uniform(0, 1)  # generate random number between 0...1
        tick_duration = (-1 / float(self.lambda_factor)) * math.log(1.0 - u) * self.time_to_ticks
        # return arrival_time
        return tick_duration
    #
    # METHOD
    # DESCRIPTION - simulates the generation of a frame, given the current tick, it will update the simulation values
    # PARAMETERS - current tick, the current tick of the simulation
    # RETURNS - Nothing
    def generate_frame(self, current_tick):
        #check if its time to create a frame
        if current_tick >= self.next_frame_generated:
            # update our arrival tick counter, this is the tick when the next frame is created
            # self.t_arrival_tick += self.calc_arrival_time()

            # new frame object created with current_tick as the tick it was created at
            frame = Frame(current_tick)
            # enqueue the frame
            self.frame_queue.enqueue(frame)
            self.next_frame_generated = current_tick + self.random_poisson_generator()

    def collision_occured(self, backoff_time):
        self.collision_occured = True

    def get_wait_duration(self):
        return 1

    def sense_medium_busy(self):
        return True

    def update_state(self, current_tick):
        if self.state == "Idle":
            # Check if there are frames waiting to be transmitted
            frames_waiting = self.frame_queue.size > 0
            if frames_waiting:
                self.frame_transmitted = self.frame_queue.dequeue()
                self.state = "Sensing"
                self.sensing_ends_tick = current_tick + self.sensing_tick_duration


        if self.state == "Sensing":
            if current_tick == self.sensing_ends_tick:
                medium_busy = self.sense_medium_busy()
                if medium_busy:
                    self.state = "Wait"
                    self.wait_ends_tick = current_tick + self.get_wait_duration()
                else:
                    self.state = "Transmit"
                    self.transmission_ends_tick = current_tick + self.transmission_delay
                    self.physical_layer_busy_until = current_tick + self.transmission_delay * 1/3
                    self.hub_busy_until = current_tick + self.transmission_delay * 2/3

        elif self.state == "Wait":
            if current_tick == self.wait_ends_tick:
                medium_busy = self.sense_medium_busy()
                if medium_busy:
                    self.wait_ends_tick = current_tick + self.get_wait_duration()
                else:
                    self.state = "Sensing"
                    self.sensing_ends_tick = current_tick + self.sensing_tick_duration
        elif self.state == "Transmit":
            # if medium is busy, when we try to transmit a frame or when a collision has already occured
            # we go to the backoff state
            if self.sense_medium_busy() or self.collision_occured:
                wait_time = self.frame_transmitted.collision_occured()
                if wait_time < 0:
                    # if the wait time is less than 0, then we've exceeded 10 tries, frame error occured
                    self.frame_errors += 1
                    # go back to idle state
                    self.state = "Idle"
                else:
                    # go back to backoff state
                    self.state = "Backoff"
                    self.backoff_ends_tick = current_tick + wait_time
            else:
                # if transmission is finished, update the total transmission delay
                # and total number of successful frames transmitted
                if self.transmission_ends_tick == current_tick:
                    delay = self.frame_transmitted.finished_transmission(current_tick)
                    self.total_frames_transmission_delay += delay
                    self.total_frames_successfully_sent += 1
                    self.state = "Idle"

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
    def simulation_results(self):
        total_frames_transmitted = self.total_frames_successfully_sent
        total_frames_transmission_delay = self.total_frames_transmission_delay
        return [total_frames_transmitted, total_frames_transmission_delay]

    #
    # METHOD -  run_simulation
    # DESCRIPTION - runs the simulation of a server and frame generator configuration
    # PARAMETERS - total_ticks is the number of ticks the simulation is run for
    #
    def run_simulation(self, current_tick):
        #clear all the variables used in the simulation
        self.generate_frame(current_tick)
        self.update_state(current_tick)



