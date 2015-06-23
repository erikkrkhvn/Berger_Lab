import pandas as pd 
import sys
import matplotlib.pyplot as plt
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
            new = self.data[self.data[name_list[i]] > self.data[name_list[i]].quantile(perc)].dropna()
        if way == 'd':
            new = self.data[self.data[name_list[i]] < self.data[name_list[i]].quantile(perc)].dropna()
        for j in range(3, len(name_list)):
            if j != i:
                new = new.drop(name_list[j], axis = 1)
        new.to_csv("quan_" + sys.argv[3] + "_" + self.filename, sep = '\t')

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

    def inter(self):
        new = pd.unique(self.data['Chr'].ravel())
        print ('directory' + '\\' + 'f')

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
if action =='i':
    first = file(input1)
    first.inter()
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