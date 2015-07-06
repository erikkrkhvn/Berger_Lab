import pandas as pd 
import sys
import matplotlib.pyplot as plt
import numpy as np
import os
from os import path
import shutil

input1 = sys.argv[1]
action = sys.argv[2]
total = list()
constant = list()

class file:

    def __init__ (self, filename):
        self.filename = filename
        # if action == "qlu" or action == "qld":
        #     self.data = np.load(filename, mmap_mode='r')
        # else:
        self.data = pd.read_csv(filename, delim_whitespace = True)
        self.total = list()

    def sub(self):
        self.num_of_col = int(sys.argv[3])
        self.col_list = list()
        self.name_list = list()
        for i in range(0,self.num_of_col):
            self.col_list.append(int(sys.argv[i+4]))
        orgi_name_list = list(self.data.columns.values)
        for j in range(0,self.num_of_col):
            self.name_list.append(orgi_name_list[2+self.col_list[j]])
        for k in range(0,int((self.num_of_col/2))+1,2):
            a = self.name_list[k]
            b = self.name_list[k+1]
            new_name = a+"-"+b
            self.data[new_name] = self.data.apply(lambda x: x[a] - x[b], axis = 1)
            self.data = self.data.drop([a,b], axis = 1)
        self.data.to_csv("sub_" + self.filename, sep = '\t')

    def norm(self):
        self.name_list = list(self.data.columns.values)
        for i in range(3, len(self.data.columns)):
            self.data[self.name_list[i]] = self.data[self.name_list[i]]*float(int(sys.argv[3])/self.data[self.name_list[i]].sum())
        self.data.to_csv("norm_" + self.filename, sep = '\t')

    def plot(self):
        chomo_list = pd.unique(self.data['Chr'].ravel())
        for i in range (1,len(chomo_list) + 1):
            a = 'chr' + str(i)
            chromo = self.data.drop(['End'], axis = 1)
            chromo = chromo.loc[self.data['Chr'] == (a)]
            chromo.plot(x = 'Start', kind = 'bar', subplots = True)
        plt.show()
    
    def quan(self, way):
        name_list = list(self.data.columns.values)
        i = int(sys.argv[4]) + 2
        perc = float(int(sys.argv[3])/100)
        if way == 'u':
            if sys.argv[5] == 'o':
                self.data = self.data[self.data[name_list[i]] > 0]
            new = self.data[self.data[name_list[i]] > self.data[name_list[i]].quantile(perc)].dropna()
        if way == 'd':
            if sys.argv[5] == 'o':
                self.data = self.data[self.data[name_list[i]] < 0]
            new = self.data[self.data[name_list[i]] < self.data[name_list[i]].quantile(perc)].dropna()
        for j in range(3, len(name_list)):
            if j != i:
                new = new.drop(name_list[j], axis = 1)
        new.to_csv("quan_" + sys.argv[3] + "_" + self.filename, sep = '\t')

    # def quan_big(self, way):
    #     i = int(sys.argv[4]) + 2
    #     perc = float(int(sys.argv[3])/100)
    #     print (self.data)
    #     if way == 'u':
    #         cut = np.percentile(self.data[self.data[i] > 0] , perc)
    #     elif way == 'd':
    #         cut = np.percentile(self.data[self.data[i] < 0][:i] , perc)
    #     print (cut)
    #     if way == 'u':
    #         new = self.data[self.data[i] >= cut]
    #     elif way == 'd':
    #         new = self.data[self.data[i] <= cut][[0,1,2,i]]
    #     print (new)
    #     np.savetxt("quan_" + sys.argv[3] + "_" + self.filename, new, delimiter = '\t')

    def normf(self):
        self.name_list = list(self.data.columns.values)
        for i in range(3, len(self.data.columns)):
            self.data[self.name_list[i]] = self.data[self.name_list[i]]*constant[i-3]
        self.data.to_csv("norm_" + self.filename, sep = '\t')

    def normf_helper(self):
        self.name_list = list(self.data.columns.values)
        if total == list():
            for i in range(3, len(self.data.columns)):
                total.append(self.data[self.name_list[i]].sum())
        else:
            for i in range(0, len(self.data.columns) - 3):
                total[i] = total[i] + self.data[self.name_list[i+3]].sum()


class filemani:

    def __init__ (self, filename):
        self.filename = filename

    def rename(self):
        toberemoved = sys.argv[3]
        tobeadded = sys.argv[4]
        length = len(toberemoved)
        if self.filename.startswith(toberemoved):
            os.rename(self.filename, (tobeadded + self.filename[length:]))

        


if action == "s":
    first = file(input1)
    first.sub()
if action == "n":
    first = file(input1)
    first.norm()
if action == "p":
    first = file(input1)
    first.plot()
if action == "qu":
    first = file(input1)
    first.quan('u')
if action == "qd":
    first = file(input1)
    first.quan('d')
if action == "sf":
    for f in os.listdir(input1):
        if path.isfile(f):
            new = file(f)
            new.sub()
    directory = os.getcwd()
    os.mkdir("subtracted")
    for f in os.listdir(directory):
            if 'sub_' in f:
                shutil.move((directory + '\\' + f), (directory + '\\' + "subtracted" + '\\' + f))

if action == "nf":
    for f in os.listdir(input1):
        if path.isfile(f):
            new = file(f)
            new.normf_helper()
    print (total)
    for i in range(0, len(total)):
        constant.append(float(int(sys.argv[3])/total[i]))
    print (constant)
    directory = os.getcwd()
    os.mkdir("normalized")
    for f in os.listdir(input1):
        if path.isfile(f):
            new = file(f)
            new.normf()
    for f in os.listdir(directory):
            if 'norm_' in f:
                shutil.move((directory + '\\' + f), (directory + '\\' + "normalized" + '\\' + f))
if action == "r":
    for f in os.listdir(input1):
        if path.isfile(f):
            new = filemani(f)
            new.rename()
if action == "c":
    first = False
    with open('combined_file.txt', 'w') as outfile:
        filelist = (os.listdir(input1))
        chrlist = list()
        for i in range(1,23):
            ele = [s for s in filelist if ("_chr" + str(i) + "_") in s]
            chrlist.append(ele)
        chrlist.append([s for s in filelist if ("chrX") in s])
        chrlist.append([s for s in filelist if ("chrY") in s])
        print(chrlist)
        for f in range(0,24):
            if path.isfile(chrlist[f][0]):
                with open(chrlist[f][0], "r") as infile:
                    for line in infile:
                        if first:
                            first = False
                        else:
                            outfile.write(line)          
                if first == False:
                    first = True
if action == "qlu":
    first = file(input1)
    first.quan_big('u')
if action == "qld":
    first = file(input1)
    first.quan_big('d')