import math
import random
class Frame:

    def __init__(self, frame_generation_tick):
        self.frame_generation_tick = frame_generation_tick
        self.frame_recieved_tick=-1
        self.sent_attempts = 0
        self.frame_service_end_tick = -1




    def finished_transmission(self, current_tick):
        self.frame_service_end_tick = current_tick
        return current_tick - self.frame_generation_tick



    def collision_occured(self):
        self.sent_attempts += 1
        if self.sent_attempts == 10:
            return -1
        else:
            waiting_delay = self.wait_time()
            return waiting_delay

    def wait_time(self):
        i = self.sent_attempts
        #LAN speed is Mbits per second, should be in MBits per tick
        LAN_speed_in_seconds = 1e6
        #number of seconds for one tick
        # 10 us per tick
        seconds_in_ticks = 10e-6
        # 10 us/tick * 1 Mbit / s
        # to convert the Mbits per second to Mbits per tick, multiply it by the seconds to tick conversion3
        LAN_speed_in_ticks = LAN_speed_in_seconds * seconds_in_ticks

        delay = random.uniform(0, 2**i - 1 ) * 512 / LAN_speed_in_ticks
        return delay

    def __str__(self):
        return "Tick When frame Was Generated:"+str(self.frame_generation_tick)\
                +"\nFrame Successfully Transmitted At:" +str(self.frame_service_end_tick)