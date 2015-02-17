from LinkedStack import LinkedQueue
class Tree:
    
    class Position:
        
        def element(self):
            raise NotImplementedError('must be implemented by subclasses')

        def __eq__(self, other):
            raise NotImplementedError('must be implemented by subclasses')

        def __ne__(self, other):
            return not (self == other)

    def root(self):
        raise NotImplementedError('must be implemented by subclasses')

    def parent(self):
        raise NotImplementedError('must be implemented by subclasses')

    def num_children(self,p):
        raise NotImplementedError('must be implemented by subclasses')

    def children(self,p):
        raise NotImplementedError('must be implemented by subclasses')

    def __len__(self):
        raise NotImplementedError('must be implemented by subclasses')

    def is_root(self,p):
        return self.root() == p

    def is_leaf(self,p):
        return self.num_children(p) == 0

    def is_empty(self):
        return len(self) == 0

    def depth(self,p):
        if self.is_root(p):
            return 0
        else:
            return 1 + self.depth(self.parent(p))

    def _height2(self,p):
        if self.is_leaf(p):
            return 0
        else:
            return 1 + max(self._height2(c) for c in self.children(p))

    def height(self,p=None):
        if p is None:
            p = self.root()
        return self._height2(p)

class BinaryTree(Tree):
    
    def left(self,p):
        raise NotImplementedError('must be implemented by subclasses')

    def right(self,p):
        raise NotImplementedError('must be implemented by subclasses')

    def sibling(self,p):
        parent = self.parent(p)
        if parent is None:
            return None
        else:
            if p == self.left(parent):
                return self.right(parent)
            else:
                return self.left(parent)

    def children(self,p):
        if self.left(p) is not None:
            yield self.left(p)
        if self.right(p) is not None:
            yield self.right(p)
        
class LinkedBinaryTree(BinaryTree):
    class _Node:
        __slots__ = '_element','_parent','_left','_right'
        def __init__(self,element,parent=None,left=None,right=None):
            self._element = element
            self._parent = parent
            self._left = left
            self._right = right

    class Position(BinaryTree.Position):
        def __init__(self,container,node):
            self._container = container
            self._node = node
        
        def element(self):
            return self._node._element

        def __eq__(self,other):
            return type(other) is type(self) and other._node is self._node

    def _validate(self,p):
        if not isinstance(p,self.Position):
            raise TypeError('p must be proper Position type')
        if p._container is not self:
            raise ValueError('p does not belong to this container') 
        if p._node._parent is p._node: #convention for deprecated nodes
            raise ValueError('p is no longer valid')
        return p._node

    def _make_position(self,node):
        return self.Position(self,node) if node is not None else None

    def __init__(self):
        self._root = None
        self._size = 0

    def __len__(self):
        return self._size

    def root(self):
        return self._make_position(self._root)

    def parent(self,p):
        node = self._validate(p)
        return self._make_position(node._parent)

    def left(self,p):
        node = self._validate(p)
        return self._make_position(node._left)

    def right(self,p):
        node = self._validate(p)
        return self._make_position(node._right)

    def num_children(self,p):
        node = self._validate(p)
        count = 0
        if node._left is not None:
            count += 1
        if node._right is not None:
            count += 1
        return count

    def _add_root(self,e):
        if self._root is not None: raise ValueError('Root exists')
        self._root = self._Node(e)
        self._size = 1
        return self._make_position(self._root)

    def _add_left(self,p,e):
        node = self._validate(p)
        if node._left is not None: raise ValueError('left child exists')
        node._left = self._Node(e,node)
        self._size  += 1
        return self._make_position(node._left) 
    
    def _add_right(self,p,e):
        node = self._validate(p)
        if node._right is not None: raise ValueError('right child exists')
        node._right = self._Node(e,node)
        self._size  += 1
        return self._make_position(node._right)

    def _replace(self,p,e):
        node = self._validate(p)
        old = node._element
        node._element = e
        return old

    def _delete(self,p):
        node = self._validate(p)
        if self.num_children(p) == 2: return ValueError('p has two children')
        child = node._left if node._left else node._right
        if child is not None:
            child._parent = node._parent
        if node is self._root:
            self._root = child
        else:
            parent = node._parent
            if node is parent._left:
                parent._left = child
            else:
                parent._right = child
        self._size -= 1
        node._parent = node
        return node._element

    def _attach(self,p,t1,t2):
        node = self._validate(p)
        if not self.is_leaf(p): raise ValueError('position must be leaf')
        if not type(self) is type(t1) is type(t2):
            raise TypeError('Tree types must match')
        self._size += len(t1) + len(t2)
        if not t1.is_empty():
            t1._root._parent = node
            node._left = t1._root
            t1._root = None
            t1._size = None
        if not t2.is_empty():
            t2._root._parent = node
            node._right = t2._root
            t2._root = None
            t2._size = None

    def preorder(self):
        if not self.is_empty():
            for p in self._subtree_preorder(self.root()):
                yield p

    def _subtree_preorder(self,p):
        yield p
        for c in self.children(p):
            for other in self._subtree_preorder(c):
                yield other

    def postorder(self):
        if not self.is_empty():
            for p in self._subtree_postorder(self.root()):
                yield p
    
    def _subtree_postorder(self,p):
        for c in self.children(p):
            for other in self._subtree_postorder(c):
                yield other
        yield p

    def inorder(self):
        if not self.is_empty():
            for p in self._subtree_inorder(self.root()):
                yield p

    def _subtree_inorder(self,p):
        if self.left(p) is not None:
            for other in self._subtree_inorder(self.left(p)):
                yield other
        yield p
        if self.right(p) is not None:
            for other in self._subtree_inorder(self.right(p)):
                yield other

    def breadthfirst(self):
        if not self.is_empty():
            fringe = LinkedQueue()
            fringe.enqueue(self.root())
            while not fringe.is_empty():
                p=fringe.dequeue()
                yield(p)
                for c in self.children(p):
                    fringe.enqueue(c)

            

    def positions(self):
#        return self.preorder()
#        return self.postorder()
#        return self.inorder()
        return self.breadthfirst()

    def __str__(self):
        elements = [p.element() for p in self.positions()]
        return ','.join(elements)
                
if __name__ == '__main__':
    T = LinkedBinaryTree()
    r = T._add_root('A')
    b = T._add_left(r,'B')
    c = T._add_right(r,'C')
    d = T._add_left(b,'D')
    e = T._add_right(d,'E')
    print len(T)
    print T.depth(e)
    print T.height(r)
    print T
    T1 = LinkedBinaryTree()
    r1 = T1._add_root('F')
    T1._add_left(r1,'G')
    T1._add_right(r1,'H')
    T2 = LinkedBinaryTree()
    r2 = T2._add_root('I')
    T2._add_left(r2,'J')
    T2._add_right(r2,'K')
    T._attach(e,T1,T2)
    print len(T)
    print T
        

        

        
