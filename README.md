# naive_bayes
A simple implementation of Naive Bayes Hotel Review Classifier:

The various data structures have a description next to their declaration


1. nblearn.py:

TrainMultinomialNB:
Trains the model on the given data

(Picks up the folds list for the folders inside the category directory(negative_polarity/truthful_from_web/fold<2/3/4>) in this case)

(All paths can be modified and custom ones can be plugged in the function ExtractVocab)

Output from nblearn.py is stored in nbmodel.txt which has the computed values for Vocabulary(word_list),prior probabilites, conditional probabilities for each word

2. nbclassify.py:

ApplyMultinomialNB:
Classifies the test document into one of the above categories
Right now, the Category Classes are -0,1,2,3. These can be extended to as many as required

The output is stored in nboutput.txt, which has the names of the category classes and the file paths that were classified on each line
