from Bio import SeqIO
import re
ORFnumber = 1
AllORFsinFile = {}
ORFlengths = {}
ORFpositions= {}
ORFgene = {}
def orffinder(dna):
    "Iterates through one frame at a time to determine if the sequence contains stop codons within each frame."
    stop_codons = ['tga', 'tag', 'taa']
    ORFsingene = {}
    ORFnumber = 1
    for i in range (frame-1, len(dna), 3):
            ORFsequence = []
            codon = dna [i:i+3].lower()
            if codon != 'atg':
                continue
            if codon == 'atg':

                framestart = i
            #determines the starting position of an open reading frame
            for q in range (framestart, len(dna), 3):

                codon = dna [q:q+3].lower()
                newcodon = str(codon)
                if newcodon in stop_codons:
                    ORFsequence.append(newcodon)
                    ORFsequence = "".join(ORFsequence)
                    startstop = "%i start %i stop" %(framestart+1, q+4)
                    ORFpositions[seq_record.id +" "+ str(ORFnumber)] = startstop
                    ORFsingene[seq_record.id +" "+ str(ORFnumber)] = ORFsequence
                    for i in ORFsingene:
                        AllORFsinFile[i] = ORFsingene[i]

                    ORFnumber = ORFnumber + 1
                    #iterates through codons after start sequence and finds stop sequence.
                    #determines start and stop position of ORF and number of ORFs in gene
                    break
                else:
                    ORFsequence.append(newcodon)
                    continue
                    #if no stop codon, add codon to sequence and continue
sequencelendict = {}
records = list(SeqIO.parse("dna2.fasta", "fasta"))
print("Found %i sequences" % len(records))
for seq_record in SeqIO.parse("dna2.fasta", "fasta"):
  record = seq_record.id
  seqlen = len(seq_record)
  sequencelendict[record] = seqlen


x = sorted(sequencelendict.values())
lowest = x[0]
highest = x.pop()

shortest = [number for number, record in sequencelendict.items() if record == lowest]
longest = [number for number, record in sequencelendict.items() if record == highest]
print("The shortest sequence belongs to:", shortest[0], "with length of %s." % sequencelendict.get(shortest[0]))
print("The longest sequence belongs to:", longest[0], "with length of %s." % sequencelendict.get(longest[0]))

for seq_record in SeqIO.parse("dna2.fasta", "fasta"):
    dna = seq_record.seq
frame = input("Please provide a frame input between 1 and 3 to find open reading frames on:")
try:
    frame = int(frame)
except:
    print("Value provided was not an integer between 1 and 3.")
if int(frame) >= 1 and int(frame) <=3:
    pass
else:
    print("Provided frame did not meet required critera. Please try again.")
    exit()
del dna
for seq_record in SeqIO.parse("dna2.fasta", "fasta"):
    nucleo = seq_record.seq
    orffinder(nucleo)
for i in AllORFsinFile:
    ORFlengths[i] = len(AllORFsinFile[i])
for i in ORFlengths:
    x = (sorted(ORFlengths.values()))
longestORFlength = x.pop()
genewithlongestORF = [number for number, record in ORFlengths.items() if record == longestORFlength]
print(genewithlongestORF)
for i in ORFpositions:
    if i == genewithlongestORF[0]:
        print(ORFpositions[i])


identifier = input("\nProvide a sequence identifier.\nThis will provide the longest ORF available for that sequence identifier within frame %i :" %(frame))
identifier = re.sub('[\W\_]','', identifier)
print(identifier)
#I want to adapt this function later on to determine the longest ORF across all reading frames
#will have to create new dictionary containing only ORF information for this identifier
newORFlengths= {}
for i in ORFlengths.keys():
    new = re.sub('[\W\_]','', i)
    newORFlengths[new]= ORFlengths[i]
print(newORFlengths.items())
res = [val for key, val in newORFlengths.items() if identifier in key]
longestinID= sorted(res)
longestORFinID=longestinID.pop()
longestORFinID=int(longestORFinID)
print(longestORFinID)
longORFinIDnumber= [number for number, record in newORFlengths.items() if record == longestORFinID]
print("The longest ORF in frame %s of %s is %i." %(frame, identifier, longestORFinID))
