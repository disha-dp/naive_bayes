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
score=[0,0,0,0] #for each document, score array stores the top two categories 
list_result={} #stores the list of result classes and the documents classified 


word_dict = {} #stores words and their count in classes, keys correspond to V (vocabulary)  
N=0	#total number of documents
DocsInClass=[0,0,0,0]	#number of documents each class holds
WordsInClass=[0,0,0,0] 	#number of words each class holds from the training set
prior=[0,0,0,0]	#prior probabilities of classes
condProb={}	#conditional probability for each class of each word in the training set

def readWords(C1,C2):
	folds={'fold2','fold3','fold4'}
	for fold in folds:
		#print(fold)
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
					word_token=word.lower()
					#word_token=re.sub(ur"[^\w\d'\s]+",'',word).lower()
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

	os.chdir("negative_polarity")	#category0 NEG
	os.chdir("truthful_from_Web")	#category 2 which is also in category 0
	readWords(NEG,TRUE)
	
	os.chdir("../")					
	os.chdir("deceptive_from_MTurk")	#category 3 which is also in category 0
	readWords(NEG,DEC)
	

	os.chdir("../../")		
	os.chdir("positive_polarity")	#category 1 POS 
	os.chdir("truthful_from_TripAdvisor")	#category 2 which is also in category 1
	readWords(POS,TRUE)

	os.chdir("../")
	os.chdir("deceptive_from_MTurk")	#category 3 which is also in category 1
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
			if word not in condProb.keys():
				condProb[word]=[0.0,0.0,0.0,0.0]
			condProb[word][c]=(float(Tct)+1)/(WordsInClass[c]+len(word_dict)) 
	os.chdir("../../..")

	with open('nbmodel.txt', 'w') as f:
		pickle.dump([word_dict, prior, condProb], f)
	f.close()
	return 


def main():
	wrong =0
	if len(sys.argv)>1:
		TrainMultinomialNB(sys.argv[1])
	return 

if __name__ == "__main__":
    main()
