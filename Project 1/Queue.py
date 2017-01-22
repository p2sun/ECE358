from collections import deque
class Queue:
    def __init__(self, limit = -1):
        self.size = 0
        self.queue = deque()
        self.limit = limit
    def __len__(self):
        return len(self.queue)

    def front(self):
        if self.size > 0:
            return self.queue[0]
        else:
            return False

    def enqueue(self,item):
        #if limit is -1 then its an unlimited queue
        if (self.limit == -1):
            self.size += 1
            self.queue.append(item)
            return True
        #if not the case, then the queue has a limit
        else:
            #only enqueue if the size is less than the limit
            if(len(self.queue) < self.limit):
                #increment the limit
                self.size += 1
                self.queue.append(item)
                return True
            else:
                return False
    def dequeue(self):
        if(self.size > 0):
            #decrement the size counter
            self.size -= 1
            return self.queue.popleft()

        else:
            return False
    def full(self):
        return self.get_size() >= self.limit
    def empty(self):
        return self.size == 0