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
        for j in range(0,self.num_of_col):
            self.name_list.append(parsed[2+self.col_list[j]])
        for k in range(0,(self.num_of_col/2)+1,2):
            a = self.name_list[k]
            b = self.name_list[k+1]
            new_name = a+"-"+b
            self.data[new_name] = self.data.apply(subtraction(), axis = 1)

    def subtraction(row, col1, col2):
        return int(row['Third'] - row['First'])

data['sub'] = data.apply(sub,axis = 1)
data = data.drop(['Third', 'First'], axis = 1)

data.to_csv('new_file.txt', sep = '\t', index = False)

first = file()
if action == "s":
    second = sub(first)