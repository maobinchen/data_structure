from ArrayStack import ArrayStack

def is_matched(expr):
    'return true is all delimiters are properly match; false otherwise'
    left = '([{'
    right = ')]}'
    S = ArrayStack()
    for c in expr:
        if c in left:
            S.push(c)
        elif c in right:
            if S.is_empty():
                return False
            if right.index(c) != left.index(S.pop()):
                return False
    return S.is_empty()

if __name__ == '__main__':
    exprs = ['(I{am[not]fat}big)','(not[match}']
    for expr in exprs:
        if is_matched(expr):
            print expr+' is matched'
        else:
            print expr+' is not matched'

