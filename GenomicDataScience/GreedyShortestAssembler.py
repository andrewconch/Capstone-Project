from collections import defaultdict
import time
import itertools as itt
from operator import itemgetter
import re
def readFastq(filename):
    #function for importing sequences and qualities from FastQ file
    sequences = []
    qualities = []
    with open(filename) as fh:
        while True:
            fh.readline()
            seq = fh.readline().rstrip()
            fh.readline()
            qual = fh.readline().rstrip()
            if len(seq) == 0:
                break
            sequences.append(seq)
            qualities.append(qual)
    return sequences, qualities



def kmerindex(sequences,kmerlength):
    '''building a kmer index based upon kmerlength provided. Iterates through
    #each read and appends dictionary values for given kmer'''
    overlaps=0
    kmer_Dict = defaultdict(list)
    for read in sequences:
        start = 0
        for i in range(start,len(read)-kmerlength+1):
                kmer = read[i:i+kmerlength]
                kmer_Dict[kmer].append(read)
                start +=1
    return kmer_Dict


def overlap(a,b,min_length):
    """ return length of longest suffix of 'a' matching a prefix of 'b' that is
    at least 'min_length' characters long. if no such overlap exists, return 0. """

    start = 0 #start all the way to the left
    if a == b:
        return 0
    while True:
        start = a.find(b[:min_length], start) # look for b's suffix in a
        if start == -1: #no more occurrences to right
            return 0
        if b.startswith(a[start:]): #found occurrence, check for full suffix/prefix match
            return len(a)-start
        start +=1 #move just past previous match
uniquep = defaultdict()
'''uniquep will be used for storage of leftover reads that do not align with any other
reads at the specified kmerlength'''


def pick_maximal_overlap(read, read_set,k,overlapDict):
    '''provides maximal overlap between read of interest and reads containing
    the suffix of the read of interest. Looks up suffix of read of interest in
    kmer_Dict and finds reads (values) under the same key (suffix kmer)'''
    best_olen=0
    read_b = None
    for compar_read in read_set:
        olen = overlap(read,compar_read, 30)
        if olen > best_olen:
            read_b = compar_read
            best_olen = olen
    return read,read_b,best_olen

def main():
    loopcount = 0
    kmerlength = input("Please provide a kmerlength:")
    kmerlength = int(kmerlength)
    seqs, quals = readFastq('ads1_week4_reads.fq')
    #print(len(seqs))
    D = kmerindex(seqs,kmerlength)
    #print(len(D.items()))
    concat = []
    overlapDict = {}
    #print(len(seqs))
    #print(seqs)
    read_a, read_b, global_olen, global_reada, global_readb, global_olen = None, None, None, None, None, None
    for read in seqs:
        read_suffix = read[len(read)-kmerlength:]
        read_set = D[read_suffix].copy()
        read_set.remove(read)
        read_a, read_b, local_olen = pick_maximal_overlap(read,read_set,kmerlength, overlapDict)
        #Used for Troubleshooting during application construction
        #print(read_a, '---------this is read a')
        #print(read_b, '---------this is read b')
        #print(local_olen,'--------this is length of overlap')
        overlapDict[(read_a,read_b)] = local_olen
    lessthan2count = 0
    for k in overlapDict.keys():
        if None in k:
            lessthan2count +=1
    print(lessthan2count)
    print(len(overlapDict.items()),'--------length of overlapDict')

    ''' overlapDict is a dictionary containing two reads listed as a tuple.
    The value for these two reads is the length of their overlap. Only reads with
    overlaps greater than the specified kmerlength will be evaluated as they are selected
    from the read_set (which is based upon the kmer index.)
    The maximum overlap will be selected from ovelapDict for use with
    Greedy Shortest Common Superstring. The maximum remaining overlap is referred to as
    maxolap, and the key (tuple of two reads), referring to the maximum overlap
    is represented by maxkey.

    The maxkey reads will be combined into a singular based upon their overlap. Once the maxkey reads
    have been combined into one corresponding read, they will be removed from the list
    of sequences. The list of sequences will then be appended by the combined read.
    (e.g ABCDE and CDEFGH are joined into ABCDEFGH, ABCDE and CDEFGH are removed from the
    list and replaced with one correspond read ABCDEFGH)

    Additionally, the overlapDict will be updated.  The key:value pairs containing
    either read a or read b will be removed and a new entry into the dictionary
    will be generated. Every instance of read a or read b will be replaced with
    read ab.'''

    nomoreoverlaps = 0
    while nomoreoverlaps != 1:
        nooverlap = []
        tempoverlapDict = overlapDict.copy()
        for k in tempoverlapDict:
            if None in k:
                nooverlap.append(k[0])
                nooverlap.append(k[1])
        maxkey = max(tempoverlapDict.items(), key=itemgetter(1))[0]
        maxolap = max(tempoverlapDict.items(), key=itemgetter(1))[1]
        try:
            tempstr1 = maxkey[0]
            seqs.remove(maxkey[0])
        except:
            print("sequence not found for some reason. pausing")
            nomoreoverlaps = 1
            tempstr2 = maxkey[1]
            seqs.append(tempstr2)
            print(seqs)
            for i in seqs:
                print(len(i))
        try:
            tempstr2 = maxkey[1]
            seqs.remove(maxkey[1])
        except:
            seqs.append(tempstr1)
            nomoreoverlaps = 1
            print(seqs)
            for i in seqs:
                print(len(i))

            #nooverlap = nooverlap+maxkey[1]
            #seqs.remove(maxkey[1])

            #print(len(maxkey[0]))
            continue
        olaplen = overlapDict[maxkey]
        olapString = maxkey[0]+maxkey[1][olaplen:]
        #print(maxkey)
        #print(maxolap)
        tempmax = []
        loopcount = 0
        for k in tempoverlapDict.keys():
            '''cannot iterate over dictionary as it is being modified. instead
            iterate over a temporary dictionary that is generated at the beginning of
            each loop'''
            if any(x in k for x in maxkey):
                newk = [olapString if x == maxkey[0] else x for x in k]
                newk = [olapString if x == maxkey[1] else x for x in newk]
                 #creating new key for overlapDict, replaces read a and read b with new overlap read
                if newk.count(olapString) == 2:
                    del overlapDict[k]
                    #will be once instance in overlapDict that contains both reads a and read b,
                    #this key:value pair is no longer useful and can be discarded
                    continue
                newnewk = (newk[0],newk[1])
                overlapDict[newnewk] = tempoverlapDict[k]
                #new entry for overlapDict contains same overlap value as previous entry for old k
                del overlapDict[k]
                #print(newk.count(olapString), 'number of olapString')
        seqs.append(olapString)
        if nomoreoverlaps == 1:
            break
    seqs = [x for x in seqs if x != None]
    maxstr = max(seqs, key=len)
    #once loop breaks after no remaining overlaps, longest string will contain
    #results from greedy shortest common superstring algorithm.
    print(maxstr)
    print(maxstr.count("A")) #prints number of Adenine
    print(maxstr.count("T")) #prints number of Thymine
start_time = time.time()
main()
print("run time: ", time.time() - start_time)
