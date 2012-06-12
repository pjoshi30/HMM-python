import sys
expected = []

def parseFile():
    #file = open("/preetam/NLP/assignment1/HMM/dataset/dataset/all.txt")
    file = open(sys.argv[1])
    FirstLineflag = True
    arrList = []
    while 1:
        line = file.readline()
        if not line:
            break
        if FirstLineflag:
            arrList = line.strip().split(" ")
            FirstLineflag = False
        else:
            tmp = line.strip().split(" ")
            for clp in tmp:
                arrList.append(clp)
    return arrList

def cleanArrayList(arrList,stateDict):
    clean_list = []
    for var in arrList:
        tmp = var.strip().split("/")
        if len(tmp) == 1:
            continue
	if stateDict.has_key(tmp[1]):
            clean_list.append(var)
    return clean_list

def calculateM(stateDict):
    #Now we have an array list of tokens
    #Iterate over these tokens to get the number of observation symbols
    ObsDict = {}
    arrayList = parseFile()
   # print arrayList
    count = 0
    for var in arrayList:
        #print var
        tmp1 = var.strip().split("/")
	if len(tmp1) == 1:
	    continue
        if stateDict.has_key(tmp1[1]):
            if not ObsDict.has_key(tmp1[0]):
                ObsDict[tmp1[0]] = count
                count = count + 1
    return ObsDict

def calculatePI(N):
    arrayList = parseFile()
    pi = [0.0]*N
    for var in arrayList:
        tmp = var.strip().split("/")
	if len(tmp) == 1:
	    continue
        if(tmp[1] == "WHO"):
            pi[0] = pi[0] + 1
        if(tmp[1] == "WHAT"):
            pi[1] = pi[1] + 1
        if(tmp[1] == "WHY"):
            pi[2] = pi[2] + 1
        if(tmp[1] == "WHEN"):
            pi[3] = pi[3] + 1
        if(tmp[1] == "WHERE"):
            pi[4] = pi[4] + 1
        if(tmp[1] == "."):
            pi[5] = pi[5] + 1
        if(tmp[1] == "?"):
            pi[6] = pi[6] + 1
    count = 0
    for i in range(len(pi)):
        count = count + pi[i]
    for j in range(len(pi)):
        pi[j] = pi[j] / count
    return pi

##def findStateDict():
##    arrayList = parseFile()
##    count = 0
##    stateDict = {}
##    for var in arrayList:
##        tmp = var.strip().split("/")
##        if not stateDict.has_key(tmp[1]):
##            stateDict(tmp[1]) = count
##            count = count + 1
##    return stateDict

def checker(val, i, A, arrayList):
##    print val
    #aList = parseFile()
    #arrayList = cleanArrayList(alist)
    if i == len(arrayList)-1:
        return A
    tmp = arrayList[i+1].split("/")
    if tmp[1] == "WHO":
        A[val][0] = A[val][0] + 1
    if tmp[1] == "WHAT":
        A[val][1] = A[val][1] + 1
    if tmp[1] == "WHY":
        A[val][2] = A[val][2] + 1
    if tmp[1] == "WHEN":
        A[val][3] = A[val][3] + 1
    if tmp[1] == "WHERE":
        A[val][4] = A[val][4] + 1
    if tmp[1] == ".":
        A[val][5] = A[val][5] + 1
    if tmp[1] == "?":
        A[val][6] = A[val][6] + 1
    return A

def calculateA(N,stateDict):
    import numpy as np
    aList = parseFile()
    arrayList = cleanArrayList(aList,stateDict)
    A = np.zeros([N,N],np.float)
    for i in range(len(arrayList)):
        #print i
        tmp = arrayList[i].split("/")
	if len(tmp) == 1:
	    continue
        if tmp[1] == "WHO":
            A = checker(stateDict["WHO"],i, A, arrayList)
        if tmp[1] == "WHAT":
            A = checker(stateDict["WHAT"],i, A, arrayList)
        if tmp[1] == "WHY":
            A = checker(stateDict["WHY"],i, A, arrayList)
        if tmp[1] == "WHEN":
            A = checker(stateDict["WHEN"],i, A, arrayList)
        if tmp[1] == "WHERE":
            A = checker(stateDict["WHERE"],i, A, arrayList)
        if tmp[1] == ".":
            A = checker(stateDict["."],i, A, arrayList)
        if tmp[1] == "?":
            A = checker(stateDict["?"],i, A, arrayList)
##        print "*********************"
##        print i
##        print A
    for j in range(N):
        counter = 0
        for k in range(N):
            counter = counter + A[j][k]
        for p in range(N):
            A[j][p] = A[j][p]/counter
    return A

def calculateB(N, M, obsDict, stateDict):
    arrayList = parseFile()
    import numpy as np
    B = np.zeros([N,M],np.float)
    for var in arrayList:
        tmp = var.split("/")
	if len(tmp) == 1:
	    continue
        if stateDict.has_key(tmp[1]):
            if obsDict.has_key(tmp[0]):
                B[stateDict[tmp[1]]][obsDict[tmp[0]]] = B[stateDict[tmp[1]]][obsDict[tmp[0]]] + 1
    for i in range(N):
        counter = 0
        for j in range(M):
            counter = counter + B[i][j]
        for k in range(M):
            B[i][k] = B[i][k]/counter
    return B

def dataPrep(obsDict,stateDict, line):
   # file = open(filename)
   # FirstLineflag = True
    arrList = []
    test_seq = []
   # while 1:
   #     line = file.readline()
   #     if not line:
   #         break
   #     if FirstLineflag:
   #         arrList = line.strip().split(" ")
   #         FirstLineflag = False
   #     else:
    tmp = line.strip().split(" ")
    for clp in tmp:
    	arrList.append(clp)
    for var in arrList:
    #    temp = var.strip().split("/")
    #    if stateDict.has_key(temp[1]):
    #        expected.append(temp[1])
    	if obsDict.has_key(var):
        	test_seq.append(obsDict[var])
    return test_seq

def invert_dict(dicti):
    inv_map = {}
    for k,v in dicti.items():
        inv_map[v] = k
    return inv_map
    
if __name__=="__main__":
    #print 'Dictionary of Observation Symbols: '
    stateDict = {"WHO":0, "WHAT":1, "WHY":2, "WHEN":3, "WHERE":4, ".":5, "?":6}
    #invert dicitonary to have values mapping to keys
    stateDict_reverse = invert_dict(stateDict)
    obsDict = calculateM(stateDict)
    #invert observation symbol dictionary
    obsDict_invert = invert_dict(obsDict)
    #Calculate N and M
    N = len(stateDict)
    M = len(obsDict)
    #Calculate PI
    pi = calculatePI(N)
    #print 'PI matrix is: '
    #print pi
    #Calculate A
    A = calculateA(N,stateDict)
   #print 'A matrix: '
    #print A
    #Calculate B
    B = calculateB(N, M, obsDict, stateDict)
    #print 'B Matrix: '
    #print B
    print 'Dictionary of Observation Symbols: '
    print obsDict
    #Create the Hidden Markov Model from A, B and PI
    from ghmm import *
    import os, glob
    #path = '/preetam/NLP/assignment1/HMM/submission/test_files/'
    #sigma = IntegerRange(0,len(obsDict))
    #hmm = HMMFromMatrices(sigma, DiscreteDistribution(sigma), A, B, pi )
    #for infile in glob.glob(os.path.join(path,'*.txt')):
	#print infile
    count_line_err = 0
    file_line_err = open("error_lines.txt","w")
    file_inline = open(sys.argv[2])
    while 1:
		line_inline = file_inline.readline()
		if not line_inline:
			break
    		count_line_err = count_line_err + 1
		test_array_list = dataPrep(obsDict,stateDict,line_inline)
    		sigma = IntegerRange(0,len(obsDict))
    		test_seq = EmissionSequence(sigma, test_array_list)
    		hmm = HMMFromMatrices(sigma, DiscreteDistribution(sigma), A, B, pi )
    #print "The hidden markov model is: "
    #print hmm
    #print "Test Sequence is:"
    #print test_seq
    #print "The decoded sequence is"
    		try:
			tuple = hmm.viterbi(test_seq)
		except:
			#ignore that line and log it
			#file_line_err.write(str(count_line_err)+"\n")
			continue
    #print tuple
    		decoded_list = []
    		for var1 in tuple[0]:
			try:
        			decoded_list.append(stateDict_reverse[var1])
			except:
				file_line_err.write(str(count_line_err)+"\n")
				continue
    #print "Tokens are: "
    		input_tokens = []
    		for var2 in test_seq:
        		input_tokens.append(obsDict_invert[var2])
    		file_HMM = open("WHOSeq.txt","a")
    		for var_WHO in decoded_list:
        		file_HMM.write(var_WHO+" ")
		if not len(decoded_list) == 0:
			file_HMM.write("\n")
    		file_HMM.close()

 
    #print input_tokens
    #print "The decoded sequence is"
    #print decoded_list
    #print "Expected output"
    #print expected
