class Empty(Exception):
    pass

class _DoublyLinkedBase:
    class _Node:
        __slots__ = '_element','_prev','_next'
        def __init__(self,element,prev,next):
            self._element = element
            self._prev = prev
            self._next = next

    def __init__(self):
        self._header = self._Node(None,None,None)
        self._trailer = self._Node(None,None,None)
        self._header._next = self._trailer
        self._trailer._prev = self._header
        self._size = 0

    def __len__(self):
        return self._size

    def is_empty(self):
        return self._size == 0

    def _insert_between(self,e,predecessor,successor):
        newest = self._Node(e,predecessor,successor)
        predecessor._next = newest
        successor._prev = newest
        self._size += 1
        return newest

    def _delete_node(self,node):
        predecessor = node._prev
        successor = node._next
        predecessor._next = successor
        successor._prev = predecessor
        self._size -= 1
        element = node._element
        node._element = node._prev = node._next = None
        return element

class LinkedDeque(_DoublyLinkedBase):

    def first(self):
        if self.is_empty():
            raise Empty("Deque is empty")
        return self._header._next._element
    
    def last(self):
        if self.is_empty():
            raise Empty("Deque is empty")
        return self._trailer._prev._element

    def insert_first(self,e):
        self._insert_between(e,self._header,self._header._next)

    def insert_last(self,e):
        self._insert_between(e,self._trailer._prev,self._trailer)

    def delete_first(self):
        if self.is_empty():
            raise Empty("Deque is empty")
        return self._delete_node(self._header._next)
    
    def delete_last(self):
        if self.is_empty():
            raise Empty("Deque is empty")
        return self._delete_node(self._trailer._prev)

    def __iter__(self):
        walk = self._header
        while walk._next._element:
            yield walk._next._element
            walk = walk._next

    def __str__(self):
        items = [i for i in self]
        return '\t'.join(items)

class PositionalList(_DoublyLinkedBase):

    class Position:

        def __init__(self,container,node):
            self._container = container
            self._node = node

        def element(self):
            return self._node._element

        def __eq__(self,other):
            return type(other) is type(self) and other._node is self._node

        def __ne__(self,other):
            return not (self == other)

    def _validate(self,p):
        if not isinstance(p,self.Position):
            raise TypeError('p must be proper Position type')
        if p._container is not self:
            raise ValueError('p does not belong to this container')
        if p._node._next is None:
            raise ValueError('p is no longer valid')
        return p._node

    def _make_position(self,node):
        if node is self._header or node is self._trailer:
            return None
        else:
            return self.Position(self,node)

    def first(self):
        return self._make_position(self._header._next)

    def last(self):
        return self._make_position(self._trailer._prev)

    def before(self,p):
        node = self._validate(p)
        return self._make_position(node._prev)

    def after(self,p):
        node = self._validate(p)
        return self._make_position(node._next)

    def __iter__(self):
        walk = self.first()
        while walk is not None:
            yield walk.element()
            walk = self.after(walk)

    def _insert_between(self,e,predecessor,successor):
        node = _DoublyLinkedBase._insert_between(self,e,predecessor,successor)
        return self._make_position(node)

    def add_first(self,e):
        return self._insert_between(e,self._header,self._header._next)
    
    def add_before(self,p,e):
        original = self._validate(p)
        return self._insert_between(e,original._prev,original)

    def add_after(self,p,e):
        original = self._validate(p)
        return self._insert_between(e,original,original._next)

    def delete(self,p):
        original = self._validate(p)
        return self._delete_node(original)

    def replace(self,p,e):
        original = self._validate(p)
        old_value = original._element
        original._element = e
        return old_value
    
    def __str__(self):
        elements = [str(p) for p in self]
        return ','.join(elements)

if __name__ == '__main__':
    PQ = PositionalList()
    s = PQ.add_first('1')
    PQ.add_after(s,'a')
    PQ.add_before(s,'b')
    print PQ
    PQ.replace(s,'c')
    print PQ
    PQ.delete(s)
    print PQ


    DQ = LinkedDeque()
    DQ.insert_first('a')
    DQ.insert_first('B')
    DQ.insert_first('c')
    DQ.insert_last('d')
    DQ.insert_last('E')
    print DQ
    print len(DQ)
    print DQ.delete_last()
    print DQ.last()
    print DQ.delete_first()
    print DQ.first()
    

    










