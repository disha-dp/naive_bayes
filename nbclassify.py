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
C=[0,1,2,3]#"negative","positive","true","dec"]	
score=[0,0,0,0]
list_result={}


def ApplyMultinomialNB(C,V,prior,condProb,d):
	global WordsInClass
	os.chdir(d)
	for doc in glob.glob("*.txt"):	#read all text files
		try:
			new_file1=open(doc,"r")
			words=[word for line in new_file1 for word in line.split()]				
			for c in C:
				score[c]=math.log10(Decimal(prior[c]))	# compute log of prior probability
				for word in words:
					word_token=word.translate(string.maketrans("",""), string.punctuation).lower()	#remove all punc and move to lower case
					if word_token  in condProb.keys():
						score[c]+=math.log10(condProb[word_token][c]) #compute log of cond prob of word
		finally:
			new_file1.close()
		ranks=[0,0,0,0]

		for num in heapq.nlargest(2,score):
			ranks[score.index(num)]=ranks[score.index(num)]+1	#add the top 2 categories
		list_result[doc]= ranks
		res_file=open("../nboutput.txt","w")	#open op file for writing
		#0- NEG, 1- POS, 2- TRUE, 3- DEC
		for res in list_result:	#write results to file
			if(list_result[res][2]==1):
				if(list_result[res][1]==1):
					res_file.write('truthful positive '+os.getcwd()+res+"\n")
				else:
					if(list_result[res][0]==1):
						res_file.write('truthful negative '+os.getcwd()+res+"\n")
			else:
				if(list_result[res][3]==1):
					if(list_result[res][1]==1):
						res_file.write('deceptive positive '+os.getcwd()+res+"\n")
					else:
						if(list_result[res][0]==1):
							res_file.write('deceptive negative '+os.getcwd()+res+"\n")
	return 


def main():
	wrong =0
	with open('nbmodel.txt') as f:	# read from the file that nbtrain wrote data in 
	    word_dict,prior,condProb= pickle.load(f)
	if len(sys.argv)>1:
		ApplyMultinomialNB(C,word_dict,prior,condProb,sys.argv[1])#last arg is the doc to classify
	return 

if __name__ == "__main__":
    main()
