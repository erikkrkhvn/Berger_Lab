import sys
import os
import shutil

filename = sys.argv[1]
action = sys.argv[2]

class splitfile:

    def __init__ (self,filename):
        self.filename = filename
        self.firstline = ''
        if action == 'c':
            with open(self.filename, "r") as read_file:
                self.first_line = read_file.readline()
                self.second_line = read_file.readline()

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

    def recombine_bedgraph(self):
        count = True
        with open(self.filename,'r') as inFile:
            with open(('rec_' + self.filename),'w') as outFile:
                outFile.write('track type=bedGraph name="XXX" description="XXX" color=31,39,202 visibility=full yLineOnOff=on autoScale=on yLineMark="0.0" alwaysZero=on graphType=bar maxHeightPixels=128:75:11 windowingFunction=maximum smoothingWindow=off' + '\n')
                for line in inFile:
                    if count:
                        self.firstline = line
                        count = False
                    else:
                        l = line.split()
                        newline = l[1:4]
                        for i in range(6,len(l)):
                            newline.append(str(l[i]))
                        outFile.write(("\t".join(newline)) + "\n")
        count = True
        l1 = self.firstline.split()
        for i in range(4,len(l1)):
            with open('rec_' + self.filename,'r') as inFile:
                with open((l1[i] + '_' + self.filename),'w') as outFile:
                    for line in inFile:
                        if count:
                            outFile.write('track type=bedGraph name="' + l1[i] + '" description="XXX" color=31,39,202 visibility=full yLineOnOff=on autoScale=on yLineMark="0.0" alwaysZero=on graphType=bar maxHeightPixels=128:75:11 windowingFunction=maximum smoothingWindow=off' + '\n')
                            count = False
                        else:
                            l = line.split()
                            newline = l[0:3]
                            newline.append(str(l[i-3]))
                            outFile.write(("\t".join(newline)) + "\n")
            count = True
        os.remove('rec_' + self.filename)

    def compact(self, comp_factor):
        parsed = self.first_line.split()
        self.length = len(parsed) - 3
        secondline_parsed = self.second_line.split()
        base_pair_diff = int(secondline_parsed[3]) - int(secondline_parsed[2]) + 1
        self.num_of_lines = int(int(comp_factor)/int(base_pair_diff))
        print ('num_of_lines ' + str(self.num_of_lines))
        self.new_chrom_mode = 0
        with open(self.filename, "r") as read_file:
            random = read_file.readline()
            with open(("comp_" + comp_factor + "_" + self.filename), "w") as write_file:
                write_file.write((random)) 
                line_num = 0
                while True:
                    returned = self.compact_helper(read_file)
                    group_total = returned[0]
                    boundaries = returned[1]
                    if (boundaries[3] != 0) and (boundaries[4] == 0):
                        break
                    line_string = list()
                    line_string.append(str(line_num))
                    for i in range(0,3):
                        line_string.append(str(boundaries[i]))
                    for j in range(0, self.length):
                        line_string.append(str(group_total[j]))
                    write_file.write(("\t".join(line_string)) + "\n")
                    line_num += 1

    def compact_helper(self, read_file):
        returned_info = []
        group_total = list()
        boundaries = list()
        split_line = ["","","",""]
        self.previous_split_line = list()
        a = 0
        for l in range (0,5):
            boundaries.append(0)
        for k in range (0,self.length):
            group_total.append(0)
        if (self.new_chrom_mode != 0):
            new_important = self.new_chrom[4:4+self.length]
            for i in range(0,self.length):
                group_total[i] += float(new_important[i])
            self.new_chrom_mode = 0
            a = 1
        for j in range(0,self.num_of_lines-a):
            line = read_file.readline()
            if line == "":
                boundaries[3] = 1
                break
            split_line = line.split()
            if j == 0:
                if a == 0:
                    chromosome_num = split_line[1]
                    boundaries[0] = chromosome_num
                    boundaries[1] = split_line[2]
                    boundaries[4] = 1
                else:
                    chromosome_num = split_line[1]
                    boundaries[0] = chromosome_num
                    boundaries[1] = self.new_chrom[2]
                    boundaries[4] = 1
            if chromosome_num == split_line[1]: 
                important = split_line[4:4+self.length]
                previous_split_line = split_line
                for i in range(0,self.length):
                    group_total[i] += float(important[i])
            else:
                self.new_chrom = split_line
                self.new_chrom_mode = 1
                split_line = previous_split_line
                break
        boundaries[2] = split_line[3]
        returned_info.append(group_total)
        returned_info.append(boundaries)
        return returned_info

    def one(self, col):
        with open(self.filename,'r') as inFile:
            with open(('one_' + self.filename),'w') as outFile:
                for line in inFile:
                    l = line.split()
                    newline = l[col]
                    outFile.write(newline + "\n")

    def heatmap_fdr(self):
        with open(self.filename,'r') as inFile:
            with open(('ffdr10_' + self.filename),'w') as outFile:
                for line in inFile:
                    l = line.split('\t')
                    if ("Annotation Cluster") in l[0]:
                        outFile.write(("\t".join(l)))
                        continue
                    if l[0] == "Category":
                        outFile.write(("\t".join(l)))
                        continue
                    if l[0] == '\n':
                        outFile.write(("\t".join(l)))
                        continue
                    if float(l[12]) < 10.0:
                        outFile.write(("\t".join(l)))
                        continue
        with open(('ffdr10_' + self.filename),'r') as inFile:
            with open(('fdr10_' + self.filename),'w') as outFile:
                totalline = ""
                delete = False
                for line in inFile:
                    l = line.split('\t')
                    if ("Annotation Cluster") in l[0]:
                        totalline = ("\t".join(l))
                        continue
                    if l[0] == "Category":
                        totalline += ("\t".join(l))
                        delete = True
                        continue
                    if l[0] == '\n':
                        if delete:
                            delete = False
                            totalline = ''
                            continue
                        else:
                            outFile.write((totalline) + '\n') 
                            totalline = ''
                            continue
                    if float(l[12]) < 10.0:
                        totalline += ("\t".join(l))
                        delete = False
                        continue               
        os.remove('ffdr10_' + self.filename)

    def new_line(self):
        with open(self.filename, 'r') as inFile:
            with open('corr' + self.filename, 'w') as outFile:
                for line in inFile:
                    new = line.replace('^M','\n')
                    outFile.write(new)
        with open('corr' + self.filename, 'r') as inFile:
            with open('n_' + self.filename, 'w') as outFile:
                line = inFile.readline()
                while line != "":
                    line = line.replace('\n','')
                    new = line + '\t' + '.' + '\t' + '0' + '\t' + '+' + '\n'
                    outFile.write(new)
                    line = inFile.readline()
        os.remove('corr' + self.filename)


new_file = splitfile(filename)
if action == 'c':
    if (int(sys.argv[3])%10) != 0:
        print ("Please enter a multiple of 100 as compacting factor")
        quit()
    else:
        new_file.compact(sys.argv[3])
if action == 'rb':
    new_file.recombine_bedgraph()
if action == 'r':
    new_file.remove()
if action == 'o':
    new_file.one(int(sys.argv[3]))
if action == 'h':
    new_file.heatmap_fdr()
if action == 'n':
    new_file.new_line()