def splitby5lines():
	file = open("allChunkedNoTags3.txt")
	count_file = 1
	counter = 0
	filesplit = "test_files/Test_set"
	file1 = open(filesplit+str(count_file)+".txt","w")
	while 1:
		line = file.readline()
		if not line:
			break
		if counter == 1:
			file1.close()
			count_file = count_file + 1
			file1 = open(filesplit+str(count_file)+".txt","w")
			file1.write(line)
			counter = 0
		else:
			file1.write(line)
			counter = counter + 1
	file1.close()
	file.close()
	print count_file
	return

splitby5lines()
