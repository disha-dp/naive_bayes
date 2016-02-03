import math
import sys
import os,glob
import array
import string
from collections import Counter
from decimal import Decimal
import heapq
import pickle
NEG=0
POS=1
TRUE=2
DEC=3
#C is superset of category classes
C=[0,1,2,3]#"negative","positive","true","dec"]	
#create class list from the input 
word_dict = {}
N=0
DocsInClass=[0,0,0,0]
WordsInClass=[0,0,0,0] 
prior=[0,0,0,0]
condProb={}
score=[0,0,0,0]
list_result={}

def readWords(C1,C2):
	folds={'fold2','fold3','fold4'}
	for fold in folds:
		os.chdir(fold)
		for doc in glob.glob("*.txt"):
			DocsInClass[C1]=DocsInClass[C1]+1
			DocsInClass[C2]=DocsInClass[C2]+1
			global N
			N =N+1 #keep incrementing doc count
			try:
				new_file=open(doc,"r")
				words=[word for line in new_file for word in line.split()]				
				WordsInClass[C1]=WordsInClass[C1]+len(words)
				WordsInClass[C2]=WordsInClass[C2]+len(words)
				for word in words:
					word_token=word.translate(string.maketrans("",""), string.punctuation).lower()
					if word_token not in word_dict.keys():
						word_dict[word_token]=[0,0,0,0]		#add (word:1 in class to which it belongs)
					word_dict[word_token][C1]=word_dict[word_token][C1]+1
					word_dict[word_token][C2]=word_dict[word_token][C2]+1
			finally:
				new_file.close()
		os.chdir('../')
	return

def ExtractVocab(dir):
	os.chdir(dir)

	os.chdir("negative_polarity")
	os.chdir("truthful_from_Web")
	readWords(NEG,TRUE)
	
	os.chdir("../")
	os.chdir("deceptive_from_MTurk")
	readWords(NEG,DEC)
	

	os.chdir("../../")
	os.chdir("positive_polarity")
	os.chdir("truthful_from_TripAdvisor")
	readWords(POS,TRUE)

	os.chdir("../")
	os.chdir("deceptive_from_MTurk")
	readWords(POS,DEC)
	
	return

def printMap(diction):
	for word in diction:
		print word
		print diction[word]


def TrainMultinomialNB(dir):
	global condProb
	ExtractVocab(dir)
	for c in C: #say we are talking about class negative
		Nc=DocsInClass[c]	#c should translate to an index in DocsInClass
		prior[c]=Decimal(Nc)/N
		textc=WordsInClass[c] #ConcatenateTextOfAllDocsInClass(D,c)
		for word in word_dict:
			Tct=word_dict[word][c]	#count the number of times the word belonged to that class
								#CountTokesOfTerm(textc,t`)
			if word not in condProb:#.keys():
				condProb[word]=[0.0,0.0,0.0,0.0]
			condProb[word][c]=(float(Tct)+1)/(WordsInClass[c]+len(word_dict)) 
	os.chdir("../../..")

	with open('nbmodel.txt', 'w') as f:
		pickle.dump([word_dict, prior, condProb], f)
	f.close()
	return #word_dict,prior,condProb
 
def main():
	counting=0
	for root, dirs, files in os.walk(os.getcwd()):
	    for fil in files:
	    	if fil.endswith(('.txt')):
			    print fil
	if len(sys.argv)>1:
		TrainMultinomialNB(sys.argv[1])
	return 

if __name__ == "__main__":
    main()

