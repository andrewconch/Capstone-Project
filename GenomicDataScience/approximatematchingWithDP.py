def readgenome(filename):
    genome = ''
    with open (filename, 'r') as f:
        for line in f:
            if not line[0] == '>':
                genome+= line.rstrip()
    return genome

excerpt = readgenome('chr1.GRCh38.excerpt.fasta')


import numpy as np

def editDistance(x,y):

    D = []
    for i in range(len(x)+1):
        D.append([0]* (len(y)+1))
        #creates array populated with 0's
    for i in range(len(x)+1):
        D[i][0] = i

        #first position of each row is populated with i
    for i in range(len(y)+1):
        D[0][i] = 0
        #first row is populated with all 0's
    list_as_array = np.array(D)
    print(list_as_array)
    #visualize array

    for i in range(1,len(x)+1):
        for j in range(1,len(y)+1):
            distHor = D[i][j-1] + 1
            distVert = D[i-1][j] + 1
            if x[i-1] == y[j-1]:
                distDiag = D[i-1][j-1]
            else:
                distDiag = D[i-1][j-1] + 1
            D[i][j] = min(distHor,distVert,distDiag)
            #detemines the
    list_as_array = np.array(D)
    print(list_as_array)
    print(min(D[-1]))
    #this is an approximate matching algorithm, so to determine the edit distance
    #using approximate matching, we will take the minimal value in the bottom row.
x = 'GCTGATCGATCGTACG'


editDistance(x,excerpt)
