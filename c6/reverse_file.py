from ArrayStack import ArrayStack

def reverse_file(filename):
    S = ArrayStack()
    original = open(filename)
    for line in original:
        S.push(line.rstrip('\n'))
    original.close()

    newfile = 'rev_'+filename
    output = open(newfile,'w')
    while not S.is_empty():
        output.write(S.pop()  + '\n')
    output.close()
