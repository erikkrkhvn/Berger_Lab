import sys
import os

class splitfile:

    def __init__ (self,filename):
        self.filename = filename
        self.firstline = ''

    def split(self):
        chip = self.filename
        startFlag = True
        pChrom = ''

        with open('new123_' + chip,'r') as inFile:
            for line in inFile:
                l = line.split()
                currChrom = l[0]

                if startFlag:
                    out = ('{}_{}').format(l[0], chip)
                    o = open(out,'w')
                    o.write(self.firstline)
                    pChrom = l[0]            
                    startFlag = False
               
                if currChrom != pChrom:
                    o.close()
                    out = ('{}_{}').format(l[0], chip)
                    o = open(out,'w')
                    o.write(self.firstline)
                    pChrom = currChrom
                o.write(line)
            o.close()
        os.remove('new123_' + chip)
        

    def remove(self):
        count = True
        with open(self.filename,'r') as inFile:
            with open(('new123_' + self.filename),'w') as outFile:
                for line in inFile:
                    if count:
                        self.firstline = line
                        count = False
                    else:
                        l = line.split()
                        newline = l[1:]
                        outFile.write(("\t".join(newline))+ "\n")

new_file = splitfile(sys.argv[1])
new_file.remove()
new_file.split()