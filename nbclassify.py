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
score=[0,0,0,0]
list_result={}
res_file=open('nboutput.txt','w')
def ApplyMultinomialNB(C,V,prior,condProb,d):
	global WordsInClass
	for doc in glob.glob(d + '/**/**/**/*.txt'):#, recursive=True
		try:
			new_file1=open(os.path.abspath(doc),"r")
			words=[word for line in new_file1 for word in line.split()]				
			for c in C:
				score[c]=math.log10(Decimal(prior[c]))
				for word in words:
					word_token=word.translate(string.maketrans("",""), string.punctuation).lower()
					if word_token  in condProb:#.keys():
						score[c]+=math.log10(condProb[word_token][c])
		finally:
			new_file1.close()
		ranks=[0,0,0,0]
		
		if score[2]>score[3] and score[0]>score[1]:
			res_file.write('truthful negative '+doc+"\n")
		else:
			if score[3]>score[2] and score[0]>score[1]:
				res_file.write('deceptive negative '+doc+"\n")
			else:
				if score[2]>score[3] and score[1]>score[0]:
					res_file.write('truthful positive '+doc+"\n")		
				else:
					res_file.write('deceptive positive '+doc+"\n")


	return # return class with max score


def main():
	wrong =0
	with open('nbmodel.txt') as f:
	    word_dict,prior,condProb= pickle.load(f)
	if len(sys.argv)>1:
		ApplyMultinomialNB(C,word_dict,prior,condProb,sys.argv[1])#last arg is the doc to classify
	return 

if __name__ == "__main__":
    main()

