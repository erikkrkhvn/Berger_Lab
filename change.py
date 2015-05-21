import sys

filename = sys.argv[1]
col1 = sys.argv[2]
col2 = sys.argv[3]
action = sys.argv[4]

#This program returns a file with name Difference_(name of col1)_(name of col2).txt
#In this file the first column has number of the base pair interval, next column is the 
#chromosome the interval is on, then the startof the interval, then the end of the 
#interval, and then a column of the difference (col1 - col2). 
#action designates if the operation on the two columns is division or subtraction
#In division, if the denominator is then the value after division is simply the numerator.

def fileinput(filename, col1, col2):
	with open(filename, "r") as read_file:
		first_line = read_file.readline()
		parsed = first_line.split()
		num1 = int(col1)
		num2 = int(col2)
		name_col1 = parsed[(2+num1)]
		name_col2 = parsed[(2+num2)]
		new_first = list()
		new_first.append("")
		for b in range(0,3):
			new_first.append(parsed[b])
		if action == "s":
			new_first.append(("%s-%s" % (name_col1,name_col2)))
			with open(("Difference_%s_%s.txt" % (name_col1,name_col2)), "w") as write_file:
				write_file.write(("\t".join(new_first)) +"\n") 
				while True:
					next_line = read_file.readline()
					if next_line == "":
						break
					pieces = next_line.split()
					new_value = int(pieces[(3+num1)]) - int(pieces[(3+num2)])
					new_line = list()
					for i in range(0,4):
						new_line.append(pieces[i])
					new_line.append(str(new_value))
					write_file.write(("\t".join(new_line)) + "\n")
		if action == "q":
			new_first.append(("%s/%s" % (name_col1,name_col2)))
			with open(("Division_%s_%s.txt" % (name_col1,name_col2)), "w") as write_file:
				write_file.write(("\t".join(new_first)) +"\n") 
				while True:
					next_line = read_file.readline()
					if next_line == "":
						break
					pieces = next_line.split()
					first_num = int(pieces[(3+num1)])
					second_num = int(pieces[(3+num2)])
					if second_num == 0:
						new_value = first_num
					else:
						new_value = float(first_num/float(second_num))
					new_line = list()
					for i in range(0,4):
						new_line.append(pieces[i])
					new_line.append(str(new_value))
					write_file.write(("\t".join(new_line)) + "\n")

			
fileinput(filename, col1, col2)
