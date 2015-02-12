from DoublyLinkedBase import PositionalList
import random

def insertion_sort(L):
    if len(L) > 1:
        marker = L.first()
        while marker != L.last():
            pivot = L.after(marker)
            value = pivot.element()
            if value > marker.element():
                marker = pivot
            else:
                walk = marker
                while walk != L.first() and L.before(walk).element() > value:
                    walk = L.before(walk)
                L.delete(pivot)
                L.add_before(walk,value)

if __name__ == '__main__':
    PQ = PositionalList()
    s = PQ.add_first(1)
    PQ.add_after(s,5)
    PQ.add_before(s,3)
    PQ.add_first(9)
    PQ.add_first(11)
    print PQ
    insertion_sort(PQ)
    print PQ
    N = 100
    L = PositionalList()
    for i in range(N) : L.add_first(random.randint(1,1000))
    print L
    insertion_sort(L)
    print L
