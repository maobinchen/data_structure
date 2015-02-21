from DoublyLinkedBase import PositionalList

class PriorityQueueBase:
    class _Item:
        __slots__ = '_key','_value'

        def __init__(self,k,v):
            self._key = k
            self._value = v

        def __lt__(self,other):
            return self._key < other._key

    def is_empty(self):
        return len(self) == 0
class Empty(Exception):
    pass

class UnsortedPriorityQueue(PriorityQueueBase):
    def _find_min(self):
        if self.is_empty():
            raise Empty('Priority queue is empty')
        small = self._data.first()
        walk = self._data.after(small)
        while walk is not None:
            if walk.element() < small.element():
                small = walk
            walk = self._data.after(walk)
        return small

    def __init__(self):
        self._data = PositionalList()

    def __len__(self):
        return len(self._data)

    def add(self,key,value):
        self._data.add_first(self._Item(key,value))

    def min(self):
        p = self._find_min()
        item = p.element()
        return(item._key,item._value)

    def remove_min(self):
        p = self._find_min()
        item = self._data.delete(p)
        return(item._key,item._value)

class SortedPriorityQueue(PriorityQueueBase):
    def __init__(self):
        self._data = PositionalList()

    def __len__(self):
        return len(self._data)

    def add(self,key,value):
        newest = self._Item(key,value)
        walk = self._data.last()
        while walk is not None and newest < walk.element():
            walk = self._data.before(walk)
        if walk is None:
            self._data.add_first(newest)
        else:
            self._data.add_after(walk,newest)

    def min(self):
        if self.is_empty():
            raise Empty('Priority queue is empty')
        p = self._data.first()
        item = p.element()
        return(item._key,item._value)

    def remove_min(self):
        if self.is_empty():
            raise Empty('Priority queue is empty')
        item = self._data.delete(self._data.first())
        return(item._key,item._value)

class HeapPriorityQueue(PriorityQueueBase):
    'A min-oriented priority queue implemented with an array based binary heap'
    def _parent(self,j):
        return (j-1)//2

    def _left(self,j):
        return 2*j+1
    
    def _right(self,j):
        return 2*j+2

    def _has_left(self,j):
        return self._left(j) < len(self._data)

    def _has_right(self,j):
        return self._right(j) < len(self._data)

    def _swap(self,i,j):
        self._data[i], self._data[j] = self._data[j], self._data[i]

    def _upheap(self,j):
        parent = self._parent(j)
        if j>0 and self._data[j] < self._data[parent]:
            self._swap(j,parent)
            self._upheap(parent)

    def _downheap(self,j):
        if self._has_left(j):
            left = self._left(j)
            small_child = left
            if self._has_right(j):
                right = self._right(j)
                if self._data[right] < self._data[left]:
                    small_child = right
            if self._data[small_child] < self._data[j]:
                self._swap(j,small_child)
                self._downheap(small_child)

    def __init__(self,contents=()):
        self._data = [self._Item(k,v) for k,v in contents]
        if len(self._data) > 1:
            self._heapify()

    def __len__(self):
        return len(self._data)

    def _heapify(self):
        start = self._parent(len(self)-1)
        for j in range(start,-1,-1):
            self._downheap(j)

    def add(self,key,value):
        self._data.append(self._Item(key,value))
        self._upheap(len(self._data)-1) 

    def min(self):
        if self.is_empty():
            raise Empty('Priority queue is empty')
        item = self._data[0]
        return (item._key,item._value)

    def remove_min(self):
        if self.is_empty():
            raise Empty('Priority queue is empty')
        self._swap(0,len(self._data)-1)
        item = self._data.pop()
        self._downheap(0)
        return (item._key,item._value)

class AdaptableHeapPriorityQueue(HeapPriorityQueue):
    class Locator(HeapPriorityQueue._Item):
        __slots__ = '_index'
    
        def __init__(self,k,v,j):
    #        super(Locator,self).__init__(k,v)
            HeapPriorityQueue._Item.__init__(self,k,v)
            self._index = j

    def _swap(self,i,j):
   #     super()._swap(i,j)
        HeapPriorityQueue._swap(self,i,j)
        self._data[i]._index = i
        self._data[j]._index = j

    def _bubble(self,j):
        if j>0 and self._data[j] < self._data[self._parent(j)]:
            self._upheap(j)
        else:
            self._downheap(j)

    def add(self,key,value):
        token = self.Locator(key,value,len(self._data))
        self._data.append(token)
        self._upheap(len(self._data)-1)
        return token

    def update(self,loc,newkey,newval):
        j = loc._index
        if not (0<=j<len(self) and self._data[j] is loc):
            raise ValueError('Invalid locator')
        loc._key = newkey
        loc._value = newval
        self._bubble(j)

    def remove(self,loc):
        j = loc._index
        if not (0<=j<len(self) and self._data[j] is loc):
            raise ValueError('Invalid locator')
        if j == len(self) - 1:
            self._data.pop()
        else:
            self._swap(j,len(self) - 1)
            self._data.pop()
            self._bubble(j)
        return (loc._key,loc._value) 

    def __iter__(self):
        for item in self._data:
            yield (item._key,item._value,item._index)

    def __str__(self):
        vs = [str(v) for v in self]
        return ','.join(vs)

if __name__ == '__main__':
    PQ = UnsortedPriorityQueue()
    PQ.add(7,'A')
    PQ.add(9,'B')
    PQ.add(5,'C')
    print PQ.min()
    print len(PQ)
    print PQ.remove_min()
    print len(PQ)

    PQ = SortedPriorityQueue()
    PQ.add(7,'A')
    PQ.add(9,'B')
    PQ.add(5,'C')
    print PQ.min()
    print len(PQ)
    print PQ.remove_min()
    print len(PQ)

    contents = [(1,'A'),(5,'E'),(6,'F'),(4,'D'),(3,'C'),(2,'B')]
    HQ = HeapPriorityQueue(contents)
    print len(HQ)
    print HQ.min()
    print HQ.remove_min()
    print len(HQ)
    print HQ.min()    

    AHQ = AdaptableHeapPriorityQueue()
    locs = []
    for k,v in contents:
        locs.append(AHQ.add(k,v))
    print len(AHQ)
    print AHQ
    AHQ.update(locs[0],8,'H')
    print AHQ
    AHQ.remove(locs[5])
    print AHQ
    
