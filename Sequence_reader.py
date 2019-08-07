#%%
import numpy as np

file = input('task sequence file name: ')
f = open(file, "r")
sequence = np.empty((0,5), int)
lines = f.readlines()
for i in lines:
    line = i
    for j in range(0, len(line)):
        if line[j] == '[':
            k = j+1
            while line[k] != ']':
                sequence = np.append(sequence, line[k])
                k += 1
f.close()

#%%
