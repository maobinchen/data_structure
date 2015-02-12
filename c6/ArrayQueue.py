class Empty(Exception):
    pass

class ArrayQueue:
    'FIFO queue implementaion using a Python list as underlying storage.'
    CAPACITY = 2 

    def __init__(self):
        self._data = [None] * ArrayQueue.CAPACITY
        self._size = 0
        self._front = 0

    def __len__(self):
        return self._size

    def is_empty(self):
        return self._size == 0

    def first(self):
        if self.is_empty():
            return Empty('Queue is Empty')
        return self._data[self._front]

    def dequeue(self):
        if self.is_empty():
            return Empty('Queue is Empty')
        answer = self._data[self._front]
        self._data[self._front] = None
        self._front = (1+self._front) % len(self._data)
        self._size -= 1
        return answer

    def enqueue(self,e):
        if self._size == len(self._data):
            self._resize(2*len(self._data))
        avail = (self._front + self._size) % len(self._data)
        self._data[avail] =  e
        self._size += 1

    def _resize(self,cap):
        print 'resizing queue ' + str(cap)
        old = self._data
        self._data = [None] * cap
        walk = self._front
        for k in range(self._size):
            self._data[k] = old[walk]
            walk = (1+walk) % len(old)
        self._front = 0
       
if __name__ == '__main__':
    Q = ArrayQueue()
    Q.enqueue(5)
    Q.enqueue(10)
    Q.enqueue(10)
    print Q.is_empty()
    print Q.dequeue()
    Q.enqueue(9)
    print Q.first() 
    print len(Q)
