# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 15:05:43 2021

@author: Emmet
"""
import re
import collections
import os
from collections import Counter

counter = Counter()

path = r'C:\Users\Emmet\Desktop\Infortmation Storage\Dataset-P1'

for f in os.listdir(path):
    filename = os.path.join(path, f)
    if os.path.isfile(filename):
        with open(filename) as words:
             c = words.read().split()
             list(filter(lambda y: re.sub(r'[^a-zA-Z0-9\n\.]', ' ', y), c))
             tokens = list(filter(lambda x: len(x) > 4 and len(x) < 20 , c))
             counter = counter + Counter(tokens)
             
for word in counter.most_common(200):

 print (word)