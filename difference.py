#difference
import sys

filename = sys.argv[1]
col1 = sys.argv[2]
col2 = sys.argv[3]

#This program returns a file with name Difference_(name of col1)_(name of col2).txt
#In this file the first column has number of the base pari interval, next column is the 
#chromosome the interval is on, then the startof the interval, then the end of the 
#interval, and then a column of the difference (col1 - col2).

def fileinput(filename, col1, col2):
	with open(filename, "r") as read_file:
		first_line = read_file.readline()
		parsed = first_line.split()
		name_col1 = parsed[(3+int(col1))]
		name_col2 = parsed[(3+int(col2))]
		with open(("Difference_%s_%s.txt" % (name_col1,name_col2)), "w") as write_file:
			write_file.write(("		Chr	Start	End	%s" % ("%s-%s" % (name_col1,name_col2)))+"\n") 
			
fileinput(filename, col1, col2)