import sys

filename = sys.argv[1]
action = sys.argv[2]
input1 = sys.argv[3]

#This program returns a file with name Difference_(name of col1)_(name of col2).txt
#In this file the first column has number of the base pair interval, next column is the 
#chromosome the interval is on, then the startof the interval, then the end of the 
#interval, and then a column of the difference (col1 - col2). 
#action designates if the operation on the two columns is division or subtraction
#In division, if the denominator is then the value after division is simply the numerator.

#This files' purpose is to normalize the data from ChIP-sep reads
#It normilzes the data by adding all of the reads together and then multiplying each
#read by a constant so that when you now add up all reads there will be 10000000 (ten 
#million)

class file:

	def __init__ (self, filename):
		self.filename = filename

	def difference(self, col1, col2):
		with open(self.filename, "r") as read_file:
			first_line = read_file.readline()
			parsed = first_line.split()
			num1 = int(col1)
			num2 = int(col2)
			name_col1 = parsed[(2+num1)]
			name_col2 = parsed[(2+num2)]
			self.new_first = list()
			self.new_first.append("")
			for b in range(0,3):
				self.new_first.append(parsed[b])
			self.new_first.append(("%s-%s" % (name_col1,name_col2)))
			with open(("Difference_%s_%s.txt" % (name_col1,name_col2)), "w") as write_file:
				write_file.write(("\t".join(self.new_first)) +"\n") 
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

	def division(self, col1, col2):
		with open(self.filename, "r") as read_file:
			first_line = read_file.readline()
			parsed = first_line.split()
			num1 = int(col1)
			num2 = int(col2)
			name_col1 = parsed[(2+num1)]
			name_col2 = parsed[(2+num2)]
			self.new_first = list()
			self.new_first.append("")
			for b in range(0,3):
				self.new_first.append(parsed[b])
			self.new_first.append(("%s/%s" % (name_col1,name_col2)))
			with open(("Division_%s_%s.txt" % (name_col1,name_col2)), "w") as write_file:
				write_file.write(("\t".join(self.new_first)) +"\n") 
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
	def normalize(self, norm_const):
		norm = 1



new_file = file(filename)			
if action == "s":
	new_file.difference(input1, sys.argv[4])
elif action == "q":
	new_file.division(input1, sys.argv[4])
elif action == "n":
	new_file.normalize(input1)
