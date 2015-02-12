class Empty(Exception):
    pass

class LinkedStack:
    class _Node:
        __slots__ = '_element','_next'
        def __init__(self,element,next):
            self._element = element
            self._next = next

    def __init__(self):
        self._head = None
        self._size = 0

    def __len__(self):
        return self._size

    def is_empty(self):
        return self._size == 0

    def push(self,e):
        self._head = self._Node(e,self._head)
        self._size += 1

    def top(self):
        if self.is_empty():
            raise Empty('Stack is empty')
        return self._head._element

    def pop(self):
        if self.is_empty():
            raise Empty('Stack is empty')
        answer = self._head._element
        self._head = self._head._next
        self._size -= 1
        return answer

class LinkedQueue:
    class _Node:
        __slots__ = '_element','_next'
        def __init__(self,element,next):
            self._element = element
            self._next = next

    def __init__(self):
        self._head = None
        self._tail = None
        self._size = 0

    def __len__(self):
        return self._size

    def is_empty(self):
        return self._size == 0
    
    def first(self):
        if self.is_empty():
            raise Empty('Queue is empty')
        return self._head._element

    def dequeue(self):
        if self.is_empty():
            raise Empty('Queue is empty')
        answer = self._head._element
        self._head = self._head._next 
        self._size -= 1
        if self.is_empty():
            self._tail = None
        return answer

    def enqueue(self, e):
        newest = self._Node(e,None)
        if self.is_empty():
            self._head = newest
        else:
            self._tail._next = newest
        self._tail = newest
        self._size += 1
    

if __name__ == '__main__':
    L = LinkedStack()
    L.push('a')
    L.push('b')
    L.push(6)
    print len(L)
    print L.top()
    print L.pop()
    print L.pop()
    print L.pop()
#    print L.pop()

    Q = LinkedQueue()
    Q.enqueue('a')
    Q.enqueue('B')
    Q.enqueue('c')
    print Q.first()
    print len(Q)
    print Q.dequeue()
    print Q.dequeue()
    print Q.dequeue()
    print Q.dequeue()
    
    

