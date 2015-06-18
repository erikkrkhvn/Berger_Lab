def Counter(Query, Database):
	a = len(Database)
	D_start = []
	D_end = []
	for i in range(0, a):
		D_start.append(Database[i][0])
		D_end.append(Database[i][1])
	D_start.sort()
	D_end.sort()
	c = 0
	x = ICount(D_start, D_end, Query) 
	return x

def ICount(D_start, D_end, interval):
	a_end = interval[1]
	first = Binary_Search1(D_start, a_end, 0, len(D_end)-1, 0)
	a_start = interval[0]
	last = Binary_Search2(D_end, a_start, 0, len(D_start)-1, 0)
	c = first - last
	return [c, first, last]

def Binary_Search1(D_start, a_end, imin, imax, mid2):
	mid1 = (imin + imax)/2 + ((imin + imax) % 2 > 0)
	if mid1 == mid2:
		return mid1
	elif D_start[mid1] < a_end or D_start[mid1] == a_end:
		mid2 = mid1
		return Binary_Search1(D_start, a_end, mid1, imax, mid2)
	else:
		mid2 = mid1
		return Binary_Search1(D_start, a_end, imin, mid1, mid2)

def Binary_Search2(D_end, a_start, imin, imax, mid4):
	mid3 = (imin + imax)/2
	if mid3 == mid4:
		return mid3
	elif D_end[mid3] > a_start or D_end[mid3] == a_start:
		mid4 = mid3
		return Binary_Search1(D_end, a_start, imin , mid3, mid4)
	else:
		mid4 = mid3
		return Binary_Search1(D_end, a_start, mid3, imax, mid4)

def file_input():
	filename = raw_input("Which database would you like to use?: ")
	question = raw_input("Have you cleaned up the file (only chromose name and begin and end points)?(Y/N): ")
	if question == "Y":
		print "Great, we can move on"
	else:
		print "Please prepare the file before using this program. After doing that restart the program."
	infile = raw_input("Is/are the queries in a BED file, otherwise you will have to type them in manually?:(Y/N) ")
	if infile == "N":
		query_chromosome = raw_input("Which chromosome is your query located on?(chr??): ")
		intervalname = raw_input("Which interval are you investigating? Give a name: ")
		interval1 = raw_input("What is the start position of the interval?: ")
		interval2 = raw_input("What is the end position of the interval?: ")
		Query = [int(interval1), int(interval2)]
		Database = []
		with open(filename, "r") as read_file:
			while True:
				a = read_file.readline()
				if a == "":
					break
				b = a.split()
				if b[0] == query_chromosome:
					r = int(b[1])
					t = int(b[2])
					Database.append([r,t])
					print b
				else:
					continue
		a = Counter(Query, Database)
		c = a[0]
		u = "The interval %s had %s intersections with the given database." % (intervalname, c)
		with open("counts.txt", "w") as write_file:
			write_file.write(u + "\n")
		return ""
	else:
		queryfile = raw_input("What is BED file's name?: ")
		intersection = raw_input("Would you like to know with what the query intersects?:(Y/N) ")
		if intersection == "N":
			with open(queryfile, "r") as read_query:
				with open("counts.txt", "w") as write2_file:
					while True:
						k = read_query.readline()
						if k == "":
							break
						l = k.split()
						with open(filename, "r") as read_database:
							Database2 = []
							while True:
								a = read_database.readline()
								if a == "":
									break
								b = a.split()
								if b[0] == l[0]:
									r = int(b[1])
									t = int(b[2])
									Database2.append([r,t])
								else:
									continue
						Query2 = [int(l[1]), int(l[2])]
						z = Counter(Query2, Database2)
						x = z[0]
						y = "%s		%s 	%s 	%s 	" % (l[3], l[1], l[2], x) #Gives name, begin and end position and number of encounters
						write2_file.write(y + "\n")
		else:
			with open(queryfile, "r") as read_query_intersect:
				with open("counts1.txt", "w") as write3_file:
					while True:
						q = read_query_intersect.readline()
						if q == "":
							break
						l = q.split()
						with open(filename, "r") as read_database:
							Database3 = []
							while True:
								a = read_database.readline()
								if a == "":
									break
								b = a.split()
								if b[0] == l[0]:
									r = int(b[1])
									t = int(b[2])
									Database3.append([r,t])
								else:
									continue
						Query3 = [int(l[1]), int(l[2])]
						z = Counter(Query3, Database3)
						x = z[0]
						y = "%s		%s 	%s 	%s 	" % (l[3], l[1], l[2], x) #Gives name, begin and end position and number of encounters
						d = y + "\n"
						for i in range(z[2] + 1, z[1]):
							g = Database3[i]
							h = "%s		%s 	%s" % (l[0], g[0], g[1])
							d += h + "\n"
						write3_file.write(d + "\n")
	return ""

file_input()