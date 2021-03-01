# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 18:55:28 2021

@author: Emmet
"""
import math
import numpy
from operator import itemgetter 
import re
import os
import random
from collections import Counter
import collections
# Counter to take in the frequency of words for a given document 
wordFreqCounterPerDocument = Counter()
# Counter for counting frequency of words read 
wordFreq = Counter()
# Counter that has frequecny of words across all documents 
wordFreqCounter = Counter()
# Counter  for number of total words in each document 
wordFileCounter = Counter()
# Counter to hold the top ten euchildean distances between the test document and the list of other documents 
top10 = Counter()
# Counter that holds the results for tfdif and ties them to specific documents
results = Counter()
resultsCos = Counter()
# holds idf values for documents
idf = Counter()
# holds tf values for documents 
tf = Counter()
# holds tf-idf values for documents 
tfidf = Counter()
totalWords = 0
#stopWords = stopwords.words('english')
#Path is tied to my directory
path = r'C:\Users\Emmet\Desktop\Infortmation Storage\Dataset-P1'
# after inputting the path of directory, loop around and read all the text to add them to the Counters 

for f in os.listdir(path):
    filename = os.path.join(path, f)
    if os.path.isfile(filename):
        with open(filename) as words:
            c = words.read().split()
            list(filter(lambda y: re.sub(r'[^a-zA-Z0-9\n\.]', ' ', y), c))
            wordFileCounter[filename] = len(c)
            wordFreqCounter = wordFreqCounter + Counter(c)  
            wordFreq = Counter(c)
            totalWords += len(wordFreqCounter)
    wordFreqCounterPerDocument[filename] = Counter(c)



# Method to preform TF-IDF calculations taking in a given document  
def tfidfMethod(document):     
### GETTING IDF 

 for word, val in wordFreqCounter.items():
    idf[word] = math.log((len(wordFileCounter))/(int(val)) , 2) + 1 
### GETTING TF

 docNo = wordFileCounter[document]
 for word,  num in wordFreqCounterPerDocument[document].items():
     tf[word] = num / float(docNo)

   
### CALCULATING TF-IDF       
 for word,  num in wordFreqCounterPerDocument[document].items():    
     tfidf[document] = tf[word] * idf[word]

 return tfidf[document]


# Method for cosine similarty that takes in the test file and another from the list
def cosine(D1,D2):
       number1 = wordFreqCounterPerDocument[D1].values()
       number2 = wordFreqCounterPerDocument[D2].values()
       
       dot = sum(n1 * n2 for n1, n2 in zip(number1, number2) )
       m1 = math.sqrt(sum(number ** 2 for nunmber in number1))
       m2 = math.sqrt(sum(number ** 2 for number in number2))
       if m1 * m2 == 0:     
           return 0
       else:
           vector = dot / (m1 * m2)
          
           return vector 
       
# Ties the Tf-idf value to its given file
for document in wordFileCounter.keys(): 
    
    results[document] = tfidfMethod(document)      

# Using a random file to act as our testing file to compare all other files
testDoc = random.choice(list(wordFileCounter.keys()))

print (" The random document choosen is : ",testDoc ,"\n")

pointRandom = tfidfMethod(testDoc)

for document in wordFileCounter.keys():
    resultsCos[document] = cosine(testDoc, document)
    

# Getting euchildean distance between test document and all other documents
for val, num in results.items():
    top10[val] = numpy.linalg.norm(pointRandom-num)

# Sorting results to display the 10 most relveant documents against the test document 
res = collections.OrderedDict(sorted(top10.items(), key = itemgetter(1))[:10])
print ("Using TF-IDF, the 10 most similar files are : \n")

for results in res:
   print ("): ",results)


# just a note, the list for cosine values is not displaying accuratley, likely due to the either it being sorted wrongly or the cosine formula being incorrect. I ran out of time so I was not able to fix
resC = collections.OrderedDict(sorted(resultsCos.items(), key = itemgetter(1), reverse = True) [:10])
print ("\n Using Cosine, the 10 most similar files are : \n")    
for results in resC:
   print ("): ",results)

