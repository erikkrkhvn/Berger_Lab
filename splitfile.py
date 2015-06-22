import sys

def split():
    chip = sys.argv[1]
    startFlag = True
    pChrom = ''

    with open(chip,'r') as inFile:
        for line in inFile:
            l = line.split()
            currChrom = l[0]

            if startFlag:
                out = ('{}_{}').format(l[0], chip)
                o = open(out,'w')
                pChrom = l[0]            
                startFlag = False
           
            if currChrom != pChrom:
                o.close()
                out = ('{}_{}').format(l[0], chip)
                o = open(out,'w')
                pChrom = currChrom
            o.write(line)
        o.close()


def remove():
    name = sys.argv[1]
    count = True
    with open(name,'r') as inFile:
        with open(('new_' + name),'w') as outFile:
            for line in inFile:
                if count:
                    s=1
                    count = False
                else:
                    l = line.split()
                    newline = l[1:]
                    outFile.write(("\t".join(newline))+ "\n")

split()