import pandas as pd 
import sys
import matplotlib.pyplot as plt

filename = sys.argv[1]
action = sys.argv[2]

class file:

    def __init__ (self):
        self.data = pd.read_csv(filename, delim_whitespace = True)

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
        self.data.to_csv("sub_newfile.txt", sep = '\t')

    def norm(self):
        self.name_list = list(self.data.columns.values)
        for i in range(3, len(self.data.columns)):
            self.data[self.name_list[i]] = self.data[self.name_list[i]]*float(int(sys.argv[3])/self.data[self.name_list[i]].sum())
        self.data.to_csv("norm_cKrox_100bp.txt", sep = '\t')

    def plot(self):
        for i in range (1,3):
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
        new.to_csv("quan_" + sys.argv[3] + "_file.txt", sep = '\t')

    def intersect(self):
        

first = file()
if action == "s":
    first.sub()
if action == "n":
    first.norm()
if action == "p":
    first.plot()
if action == "qu":
    first.quan('u')
if action == "qd":
    first.quan('d')