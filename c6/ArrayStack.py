class Empty(Exception):
    pass

class ArrayStack:
    'LIFO Stack implementaion using a Python list as underlying storage'

    def __init__(self):
        self._data = []

    def __len__(self):
        return len(self._data)

    def is_empty(self):
        return len(self) == 0

    def push(self,e):
        self._data.append(e)

    def top(self):
        if self.is_empty():
            raise Empty('Stack is empty')
        return self._data[-1]

    def pop(self):
        if self.is_empty():
            raise Empty('Stack is empty')
        return self._data.pop()

if __name__ == '__main__':
    A = ArrayStack()
#    A.pop()
#    A.top()
    A.push(1)
    A.push(2)
    print len(A)
    print A.top()
    print A.pop()
    print A.top()
    
    

    
