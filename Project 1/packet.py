class Frame:

    def __init__(self, packet_generation_tick):
        self.packet_generation_tick = packet_generation_tick
        self.packet_service_start_tick=-1
        self.packet_service_end_tick = -1


    def finished_processing(self, packet_end_tick):
        self.packet_service_end_tick = packet_end_tick
        return packet_end_tick - self.packet_generation_tick

    def start_processing(self, packet_start_tick):
        self.packet_service_start_tick = packet_start_tick

    def __str__(self):
        return "Tick When Packet Was Generated:"+str(self.packet_generation_tick)\
                +"\nPacket Service Started:" +str(self.packet_service_start_tick) \
                +"\nPacket Service Ended:"+str(self.packet_service_end_tick)+'\n'