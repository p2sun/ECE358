import string
class Packet:

    def __init__(self, packet_generation_tick, packet_size):
        self.packet_generation_tick = packet_generation_tick
        self.packet_processing_start_tick = 0
        self.packet_processing_end_tick = 0
        self.packet_size = packet_size

    def get_packet_size(self):
        return self.packet_size
    def start_server_processing(self,current_tick):
        self.packet_processing_start_tick = current_tick
    def finished_processing(self, packet_end_tick):
        self.packet_processing_end_tick = packet_end_tick

    def get_start_time(self):
        return self.packet_generation_tick


    def get_timelapsed(self, current_tick):
        return current_tick - self.packet_generation_tick

    def __str__(self):
        return "Tick When Packet Was Generated:"+str(self.get_start_time())+"\nTick When Packet Processing Began:" \
                +str(self.packet_processing_start_tick) + "\nTick When Packet Processing end:" \
               + str(self.packet_processing_end_tick) + "\nPacket Size:"+str(self.get_packet_size()) +"\n"
