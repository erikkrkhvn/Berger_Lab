import sys
import os
import shutil

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
        directory = os.getcwd()
        os.mkdir("non_normal_chr")
        correct_list = list()
        correct_list.append('chrX_' + self.filename)
        correct_list.append('chrY_' + self.filename)
        for i in range(1,23):
            correct_list.append('chr' + str(i) + '_' + self.filename)
        for f in os.listdir(directory):
            if (f in correct_list) == False:
                shutil.move((directory + '\\' + f), (directory + '\\' + "non_normal_chr" + '\\' + f))   

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