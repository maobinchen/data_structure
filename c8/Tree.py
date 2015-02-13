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
        return self.num_children(self,p) == 0

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

