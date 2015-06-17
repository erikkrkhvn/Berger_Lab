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
        self.data.to_csv("norm_newfile.txt", sep = '\t')

    def plot(self):
        self.data.plot(x = 'Start', kind = 'bar', subplots = True, by = ['Chr'])
        plt.show()

first = file()
if action == "s":
    first.sub()
if action == "n":
    first.norm()
if action == "p":
    first.plot()