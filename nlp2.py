import sys
import nltk
from nltk.corpus import wordnet as wn

def initialize():
	global brownCorpus,unigramTagger
	print "Loading corpus and tagger. This may take a moment."
	print "Loading corpus...",
	brownCorpus = nltk.corpus.brown.tagged_sents()
	print "done."
	print "Loading tagger...",
	unigramTagger = nltk.UnigramTagger(brownCorpus)
	print "done."
	
def tokenizer(sentence):
	return nltk.word_tokenize(sentence)

def readParseTree(treeStr):
	str = ""
	previousToken=None
	for each in treeStr:
		word = each[0][0]
		tokenLabel=each[1]
		realTag=None
		if tokenLabel=='S':
			#Get the inner tuple
			realTag = each[0][1]
			tokenLabel=realTag
		elif tokenLabel!=previousToken:
			realTag = tokenLabel
		if tokenLabel!=previousToken:
			str=str+realTag+"/"+word+" "
		previousToken = tokenLabel
	return str

def chunker(tokenizedSentence):
	grammar = """
		EXT: {(<MD.*><BE.*>|<HV.*><BE.*>|<DO.*><BE.*>|<BE.*>)<AT>*<JJ.*>*<NN.*>*}
		NPH: {<A(T|P)>*<JJ.*>*(<,><JJ.*>)*<N.*>*<CS.*>*<PP.*>*<VBD>*}
		VOB: {(<MD.*><VB.*>|<HV.*><VB.*>|<BE.*><VB.*>|<DO.*><VB.*>|<VB.*>)<AT>*<JJ.*>*<NN.*>*}
		PRP: {(<RP.*>|<IN.*>)<PP.*>*<AT>*<JJ.*>*(<,><JJ.*>)*<N.*>*|(<RP.*>|<IN.*>)<AT>*<N.*>*|(<RP.*>|<IN.*>)<VBG>|}
	"""
	#Previous rules for rollback
	#PM: {<VB(D|N|G)?>*<IN.*><AT>*<N.*>|<WRB>NP|<WPS>NP}
	#VP: {<MD.*><VB.*>|<HV.*><VB.*>|<BE.*><VB.*>|<DO.*><VB.*>}
	#NP: {<AT>*<JJ.*>*(<,><JJ.*>)*<N.*>*}
	#		PP: {<IN.*><AT>*<N.*>|<IN.*><VBG>|<IN.*><PP.*>*<AT>*<JJ.*>*(<,><JJ.*>)*<N.*>*}
	c = nltk.RegexpParser(grammar)
	#print c.parse(tokenizedSentence).pprint()
	str = readParseTree(c.parse(tokenizedSentence).pos())
	return str

def posTagger(sentence):
	tokenizedSentence = tokenizer(sentence)
	wordsTagged = unigramTagger.tag(tokenizedSentence)
	theList = []
	testTagging = []
	for i in range(len(wordsTagged)):
		word = wordsTagged[i][0]
		tag = wordsTagged[i][1]
		if None==tag:
			tag = nltk.pos_tag(word)[0][1]
			wordsTagged[i]=(word,tag)
		newStr = tag+"/"+word
		theList.append(newStr)
		if tag[:2]=="BE" or tag[:2]=="DO" or tag[:2]=="HV" or tag[:2]=="VB":
			testTagging.append("VB/"+word)
		elif tag[:2]=="AB" or tag[:2]=="AP" or tag[:2]=="DT" or tag[:1]=="N" or tag[:2]=="PN" or tag[:2]=="PP":
			testTagging.append("NN/"+word)
		else:
			testTagging.append(word)
	print wordsTagged
	treeStr = chunker(wordsTagged)
	return treeStr



#Global variables, set in initialize function
brownCorpus = None
unigramTagger = None
initialize()
t=open(sys.argv[1],'r')
lines = t.readlines()
t.close()
f=open(sys.argv[2],'w')
for sentence in lines:
#while True:
#	print
#	sentence=raw_input("Enter a sentence (Type \"Exit\" to quit): ")
	if sentence.lower()=="exit":
		break
	else:
		print sentence
		treeStr = posTagger(sentence)
		print treeStr
		f.write(sentence)
		f.write(treeStr)
		f.write("\n")
f.close()
