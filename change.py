import sys

filename = sys.argv[1]
action = sys.argv[2]
input1 = sys.argv[3]

#If the second argument is n then you are normalizing the data. The thrid argument will then be the
#constant you are normalizing too. It normilzes the data by adding all of the reads together and then multiplying each
#read by a constant so that when you now add up all reads there will be 10000000 (ten 
#million)

#If the second argument is s then you are subtracting two columns from each other to find the difference.
#thrid argument is the first column, and the fourth argument is the second column.
#This program returns a file with name Difference_(name of col1)_(name of col2).txt
#In this file the first column has number of the base pair interval, next column is the 
#chromosome the interval is on, then the startof the interval, then the end of the 
#interval, and then a column of the difference (col1 - col2).

#If the second argument is q then the operation one the two following arguments is division
#In division, if the denominator is 0 then the value after division is simply the numerator.

#If the second argument is a "c" then you can compact the file in the sense that you can group together 
#groups of basepairs to get less resolution in basepair intervals. For example if you have as compaction 
#factor 300 then the program will add together all of the reads of the intervals between 1 and 300 and all groups of 300
#starting from there

class file:

	def __init__ (self, filename):
		self.filename = filename
		with open(self.filename, "r") as read_file:
			self.first_line = read_file.readline()
			self.second_line = read_file.readline()

	def normalize(self, norm_const):
		parsed = self.first_line.split()
		self.length = len(parsed) - 3
		total = list()
		for j in range (0,self.length):
			total.append(0)
		with open(self.filename, "r") as read_file:
			random = read_file.readline()
			while True:
				line = read_file.readline()
				if line == "":
					break
				split_line = line.split()
				important = split_line[4:4+self.length]
				for i in range(0,self.length):
					total[i] += int(important[i])
		constant = list()
		for k in range(0,self.length):
			constant.append(float(int(norm_const)/float(total[k])))
		with open(self.filename, "r") as read_file:
			random = read_file.readline()
			with open(("norm_"+ self.filename), "w") as write_file:
				write_file.write((random)) 
				while True:
					line = read_file.readline()
					if line == "":
						break
					split = line.split()
					for i in range (0, self.length):
						split[i+4] = str(int(split[i+4])*constant[i])
					write_file.write(("\t".join(split)) + "\n")	

	def compact(self, comp_factor):
		parsed = self.first_line.split()
		self.length = len(parsed) - 3
		secondline_parsed = self.second_line.split()
		base_pair_diff = int(secondline_parsed[3]) - int(secondline_parsed[2]) + 1
		self.num_of_lines = int(comp_factor)/int(base_pair_diff)
		self.new_chrom_mode = 0
		with open(self.filename, "r") as read_file:
			random = read_file.readline()
			with open(("comp_" + comp_factor + "_" + self.filename), "w") as write_file:
				write_file.write((random)) 
				line_num = 0
				while True:
					returned = self.compact_helper(read_file)
					group_total = returned[0]
					boundaries = returned[1]
					if (boundaries[3] != 0) and (boundaries[4] == 0):
						break
					line_string = list()
					line_string.append(str(line_num))
					for i in range(0,3):
						line_string.append(str(boundaries[i]))
					for j in range(0, self.length):
						line_string.append(str(group_total[j]))
					write_file.write(("\t".join(line_string)) + "\n")
					line_num += 1

	def compact_helper(self, read_file):
		returned_info = []
		group_total = list()
		boundaries = list()
		split_line = ["","","",""]
		self.previous_split_line = list()
		a = 0
		for l in range (0,5):
			boundaries.append(0)
		for k in range (0,self.length):
			group_total.append(0)
		if (self.new_chrom_mode != 0):
			new_important = self.new_chrom[4:4+self.length]
			for i in range(0,self.length):
				group_total[i] += int(new_important[i])
			self.new_chrom_mode = 0
			a = 1
		for j in range(0,self.num_of_lines-a):
			line = read_file.readline()
			if line == "":
				boundaries[3] = 1
				break
			split_line = line.split()
			if j == 0:
				if a == 0:
					chromosome_num = split_line[1]
					boundaries[0] = chromosome_num
					boundaries[1] = split_line[2]
					boundaries[4] = 1
				else:
					chromosome_num = split_line[1]
					boundaries[0] = chromosome_num
					boundaries[1] = self.new_chrom[2]
					boundaries[4] = 1
			if chromosome_num == split_line[1]:	
				important = split_line[4:4+self.length]
				previous_split_line = split_line
				for i in range(0,self.length):
					group_total[i] += int(important[i])
			else:
				self.new_chrom = split_line
				self.new_chrom_mode = 1
				split_line = previous_split_line
				break
		boundaries[2] = split_line[3]
		returned_info.append(group_total)
		returned_info.append(boundaries)
		return returned_info

class difference(file):

	def __init__ (self, file):
		self.filename = file.filename
		self.first_line = file.first_line
		parsed = self.first_line.split()
		self.num_of_col = int(input1) #number of columns you will using as input
		self.col_list = list()
		self.name_list = list()
		for i in range(0,self.num_of_col):
			self.col_list.append(int(sys.argv[i+4]))
		for j in range(0,self.num_of_col):
			self.name_list.append(parsed[2+self.col_list[j]])
		self.new_first = list()
		self.new_first.append("")
		for b in range(0,3):
			self.new_first.append(parsed[b])
		
	def subtraction(self):
		for k in range(0,(self.num_of_col/2)+1,2):
			self.new_first.append(("%s-%s" % (self.name_list[k], self.name_list[k+1])))
		self.type = "sub"

	def division(self):
		for k in range(0,(self.num_of_col/2)+1,2):
			self.new_first.append(("%s/%s" % (self.name_list[k], self.name_list[k+1])))
		self.type = "div"

	def while_loop(self):
		with open(self.filename, "r") as read_file:
			first_line = read_file.readline()
			if self.type == "sub":
				title = ("Difference_" + self.filename)
				with open(title, "w") as write_file:
					write_file.write(("\t".join(self.new_first)) +"\n") 
					while True:
						next_line = read_file.readline()
						if next_line == "":
							break
						pieces = next_line.split()
						nums = list()
						new_vals = list()
						for j in range(0,self.num_of_col):
							nums.append(float(pieces[3+self.col_list[j]]))
						for k in range(0,(self.num_of_col/2)+1,2):
							new_vals.append(nums[k]-nums[k+1])
						new_line = list()
						for i in range(0,4):
							new_line.append(pieces[i])
						for l in range(0,(self.num_of_col/2)):
							new_line.append(str(new_vals[l]))
						write_file.write(("\t".join(new_line)) + "\n")		
			elif self.type =="div":
				title = ("Division_" + self.filename)
				with open(title, "w") as write_file:
					write_file.write(("\t".join(self.new_first)) +"\n")
					while True:
						next_line = read_file.readline()
						if next_line == "":
							break
						pieces = next_line.split()
						nums = list()
						new_vals = list()
						for j in range(0,self.num_of_col):
							nums.append(int(pieces[3+self.col_list[j]]))
						for k in range(0,(self.num_of_col/2)+1,2):
							if nums[k+1] == 0:
								new_vals.append(nums[k])
							else:
								new_vals.append(float(first_num/float(second_num)))
						new_line = list()
						for i in range(0,4):
							new_line.append(pieces[i])
						for l in range(0,(self.num_of_col/2)):
							new_line.append(str(new_vals[l]))
						write_file.write(("\t".join(new_line)) + "\n")

first = file(filename)			
if action == "s":
	second = difference(first)
	second.subtraction()
	second.while_loop()
elif action == "q":
	second = difference(first)
	second.division()
	second.while_loop()
elif action == "n":
	first.normalize(input1)
elif action == "c":
	if (int(input1)%10) != 0:
		print "Please enter a multiple of 100 as compacting factor"
		quit()
	else:
		first.compact(input1)