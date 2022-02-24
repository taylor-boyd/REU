# Program for taking sequence_builder.cc output and inputting to main_documented.py

# Output files look like this:
# 
# task sequence key:
# 1 = yellow
# 2 = blue 
# [13456]
# [26543]
#
# and the name of the file is given by the user

import numpy as np
from anytree import Node, RenderTree
from Main_Documented import *

# user enters output file name 
file_name = input("Enter sequence_builder.cc output file name: ")

# looks through file for sequences
sequences = []
with open(file_name) as f:
    for line in f:
        if '[' in line:
            temp = line.strip()
            sequences.append(temp.strip('[]'))
f.close()

# constructing first sequence 
seq1 = []
temp = sequences[0]
for x in temp:
    seq1.append(int(x))
ex1 = np.array(seq1)

# constructing second sequence
seq2 = []
temp = sequences[1]
for x in temp:
    seq2.append(int(x))
ex2 = np.array(seq2)

# print sequences to terminal so user can see
print("ex1: " + str(ex1))
print("ex2: " + str(ex2))

# put sequences into algorithm which findes 'AND', 'OR' relationships, etc.
while len(ex1) != 2:
    ex1, ex2, andNodes, orNodes = mainAlg(ex1, ex2)

# create hierarchical task tree  
andNodes = andNodes.flatten()               # 'flattens' array, collapses it into one dimension
tree = reconstruct(andNodes, orNodes, ex1) 

# print out results
print("\n\nRECONSTRUCTED TREE: \n")
print(RenderTree(tree))                     # anytree feature (Node is too)