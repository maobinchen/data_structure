from Tree import LinkedBinaryTree

class EulerTour:
    def __init__(self,tree):
        self._tree = tree
    
    def tree(self):
        return self._tree

    def execute(self):
        if len(self._tree) > 0:
            return self._tour(self._tree.root(),0,[])

    def _tour(self,p,d,path):
        self._hook_previsit(p,d,path)
        results = []
        path.append(0)
        for c in self._tree.children(p):
            results.append(self._tour(c,d+1,path))
            path[-1] += 1
        path.pop()
        answer = self._hook_postvisit(p,d,path,results)
        return answer

    def _hook_previsit(self,p,d,path):
        pass
    
    def _hook_postvisit(self,p,d,path,results):
        pass

class PreorderPrintIndentedTour(EulerTour):
    def _hook_previsit(self,p,d,path):
        print(2*d*' ' + str(p.element()))

class PreorderPrintIndentedLabeledTour(EulerTour):
    def _hook_previsit(self,p,d,path):
        label = '.'.join(str(j+1) for j in path)
        print(2*d*' ' + label+' '+str(p.element()))

if __name__ == '__main__':
    T = LinkedBinaryTree()
    r = T._add_root('A')
    b = T._add_left(r,'B')
    c = T._add_right(r,'C')
    d = T._add_left(b,'D')
    e = T._add_right(d,'E')
    T1 = LinkedBinaryTree()
    r1 = T1._add_root('F')
    T1._add_left(r1,'G')
    T1._add_right(r1,'H')
    T2 = LinkedBinaryTree()
    r2 = T2._add_root('I')
    T2._add_left(r2,'J')
    T2._add_right(r2,'K')
    T._attach(e,T1,T2)
    print T
    euler = PreorderPrintIndentedTour(T)
    euler.execute() 
    euler = PreorderPrintIndentedLabeledTour(T)
    euler.execute() 
