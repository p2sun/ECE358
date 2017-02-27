class Medium:
    def __init__(self, N):
        self.N = N
        self.physical_layer_busy = [[False, -1] for i in xrange(0,N) ]
        self.transmit_done = [False for i in xrange(0,N)]

    def sense_medium(self,node_id, current_tick):
        node = self.physical_layer_busy[node_id]
        if node[0] and current_tick <= node[1]:
            return True
        else:
            return False

    def transmit_frame_on_layer(self, current_tick, node_id, busy_until):
        if self.sense_medium(node_id, current_tick):
            self.physical_layer_busy[node_id] = [False, -1]
            return False
        else:
            self.physical_layer_busy[node_id] = [True, busy_until]
            return True

    def state_changed(self, node_id):
        if self.transmit_done[node_id] == True:
            self.transmit_done[node_id] = False
            return True
        else:
            return False

    def check_collision(self, node_id):
        if self.physical_layer_busy[node_id][1] == -1:
            return True
        else:
            return False

    def check_medium(self, current_tick):
        for i in xrange(0,self.N):
            if self.physical_layer_busy[i][0] and current_tick > self.physical_layer_busy[i][1]:
                self.physical_layer_busy[i] = [False, -1]
                self.transmit_done[i] = True

