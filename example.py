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
        
        data[a]

    def subtraction(row):
        return int(row['Third'] - row['First'])

data['sub'] = data.apply(sub,axis = 1)
data = data.drop(['Third', 'First'], axis = 1)

data.to_csv('new_file.txt', sep = '\t', index = False)

first = file()
if action == "s":
    second = sub(first)