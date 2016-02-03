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
	#os.chdir(d)

	for doc in glob.glob(d + '/**/**/**/*.txt'):#, recursive=True):
	#for root, dirs, files in os.walk(os.getcwd()):
	#for doc in files:
		#print doc
		#if doc.endswith(('.txt')):
		try:
			#print dirs
			#print root
			#print doc
			#print os.getcwd()
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
		#instead of top 2, use top from pos/neg and top from true/dec
		for num in heapq.nlargest(2,score):
			ranks[score.index(num)]=ranks[score.index(num)]+1
		list_result[doc]= ranks

	for res in list_result:
		print ('writing labels for file: '+res)
		if(list_result[res][2]>list_result[res][3] and list_result[res][0]>list_result[res][1]):# true neg
			res_file.write('truthful negative '+res+"\n")
		if(list_result[res][3]>list_result[res][2] and list_result[res][0]>list_result[res][1]):# dec neg
			res_file.write('deceptive negative '+res+"\n")
		if(list_result[res][2]>list_result[res][3] and list_result[res][1]>list_result[res][0]):# true pos
			res_file.write('truthful positive '+res+"\n")
		if(list_result[res][3]>list_result[res][2] and list_result[res][1]>list_result[res][0]):#dec pos
			res_file.write('deceptive positive '+res+"\n")
			

		
	res_file.close()

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

