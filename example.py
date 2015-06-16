import pandas as pd 
import sys

filename = sys.argv[1]
action = sys.argv[2]
input1 = sys.argv[3]

class file:

    def __init__ (self):
        self.data = pd.read_csv(filename, delim_whitespace = True)

    def sub(self):
        self.num_of_col = int(input1)
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
        self.data.to_csv("sub_newfile.txt", sep = '\t', index = False)

    def norm(self):
        

first = file()
if action == "s":
    first.sub()