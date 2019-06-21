
#%%
import numpy as np
from anytree import Node, RenderTree

andDict = dict()
orDict = dict()

############ HELPER FUNCTIONS ############

# find all OR nodes (aka any node in ex1 that is not in ex2 and visa versa)
def findOrNodes(ex1, ex2):
    global orDict
    orNodes = np.empty((0,3), int)
    for i in ex1:
        if not np.isin(i, ex2):
            orNodes = np.append(orNodes,i)
    for i in ex2:
        if not np.isin(i, ex1):
            orNodes = np.append(orNodes,i)
    orNodes.sort()
    for i in range(0, orNodes.size-1,2):
        node = Node("OR")
        left = Node(orNodes[i], parent=node)
        right = Node(orNodes[i+1], parent=node)
        orDict[orNodes[i]] = node
    return orNodes

def replaceOrNodes(ex, orNodes):
    for i in range(0,orNodes.size-1):
        ex = np.where(ex==orNodes[i+1], int(orNodes[i]), ex)
    return ex

def initGraph(ex1, ex2):
    # initialize graph with first elements coming from 0 start node
    graph = dict()
    graph[0] = np.array([ex1[0],ex2[0]])
    # add each outgoing node from its previous root node
    for i in range(0,ex1.size-1):
        if ex1[i] in graph:
            graph[ex1[i]] = np.append(graph[ex1[i]], ex1[i+1])
        else:
            graph[ex1[i]] = np.array([ex1[i+1]])
    for i in range(0,ex2.size-1):
        if ex2[i] in graph:
            graph[ex2[i]] = np.append(graph[ex2[i]], ex2[i+1])
        else:
            graph[ex2[i]] = np.array([ex2[i+1]])
    return graph

def findAndNodes(graph):
    global andDict
    andNodes = np.empty((0,2), int)
    # find pairs in graph where they exist in each others dest.
    for key in graph:
        for i in graph[key]:
            if int(i) in graph and key in graph[int(i)]:
                if key not in andNodes:
                    node = Node("AND")
                    if i < key:
                        andNodes = np.concatenate((andNodes, [[i, key]]), axis=0)  
                        left = Node(i, parent=node)
                        right = Node(key, parent=node)
                    else:
                        andNodes = np.concatenate((andNodes, [[key, i]]), axis=0)
                        left = Node(key, parent=node)
                        right = Node(i, parent=node)        
                    if i not in andDict:
                        andDict[i] = node
    return andNodes

def andBuilding(ex1, ex2):
    global andDict
    global orDict

    delKey1 = delKey2 = 10
    for key in andDict:
        index1 = index2 = index3 = index4 = 0
        for i in andDict[key].children: 
            for j in range(0,ex1.size):
                if ex1[j] == i.name:
                    index1 += j
                if ex2[j] == i.name:
                    index2 += j
        if index1 != index2:
            newNode = Node("AND")
            newLeft = andDict[key]
            newLeft.parent = newNode
            if (index1 - index2) == 2 or (index2 - index1) == 2:
                for key2 in orDict:
                    for i2 in range(0,ex1.size):
                        if ex1[i2] == key2:
                            index3 += i2
                        if ex2[i2] == key2:
                            index4 += i2
                    if index3 != index4:
                        if (index3 - index4) == 2 or (index4 - index3) == 2:
                            newRight = orDict[key2]
                            newRight.parent = newNode
                            delKey2 = key2        
            else:
                if (index1 - index2) == 4 or (index2 - index1) == 4:
                    nextKey = key+2
                    nextKey2 = key+1
                    if nextKey in andDict:
                        newRight = andDict[nextKey]
                        newRight.parent = newNode
                        delKey1 = nextKey
                    if nextKey2 in andDict:
                        newRight = andDict[nextKey2]
                        newRight.parent = newNode
                        delKey1 = nextKey2
            andDict[key] = newNode
    if delKey1 != 10:
        del andDict[delKey1]
    elif delKey2 != 10:
        del orDict[delKey2]

    return ex1, ex2

def reconstruct(andNodes, orNodes, ex1):
    global andDict
    global orDict
    
    tree = Node("THEN")

    print(andDict)
    print(orDict)

    delKey1 = delKey2 = 10
    #while len(andDict.keys()) != 0 and len(orDict.keys()) != 0:     #just added this
        for key in andDict:
            for key2 in orDict:
                if key > key2 and not np.isin(key, orNodes):
                    node = orDict[key2]
                    node.parent = tree
                else:
                    if key > key2:
                        node = orDict[key2]
                        node.parent = tree
                    elif np.isin(key, orNodes):
                        parentNode = Node("AND")
                        node1 = orDict[key]
                        node1.parent = parentNode
                        delKey1 = key
                        for i in andNodes:
                            if not np.isin(i, orNodes):
                                if (key - i) == 1 or (i - key) == 1:
                                    node2 = Node("AND", parent=parentNode)
                                    left = Node(i, parent=node2)
                                    j = i-1
                                    k = i+1
                                    if not np.isin(j, orNodes):
                                        right = Node(j, parent=node2)
                                    if not np.isin(k, orNodes):
                                        right = Node(k, parent=node2)
                                    parentNode.parent = tree
                    else:
                        node = andDict[key]
                        node.parent = tree

    #if delKey1 != 10:
     #   del orDict[delKey1]
    #if delKey2 != 10:


    return tree
        
def mainAlg(ex1, ex2):
    orNodes = findOrNodes(ex1, ex2)
    ex2 = replaceOrNodes(ex2, orNodes)
    graph = initGraph(ex1, ex2)
    andNodes = findAndNodes(graph)
    ex1, ex2 = andBuilding(ex1, ex2)
    return ex1, ex2, andNodes, orNodes


#%%

### AND-AND/AND-AND/OR, OR cases ###

# case 1 -- works!!
# ex1 = np.array([1,2,3,5])
# ex2 = np.array([4,2,1,6])

# case 2 -- works!!
# ex1 = np.array([1,3,2,5])
# ex2 = np.array([2,4,1,6])

# case 3 -- gotta work on it
# ex1 = np.array([1,3,4,5])
# ex2 = np.array([2,6,4,3])

# case 4 -- works!!
ex1 = np.array([1,3,5,4])
ex2 = np.array([2,4,6,3])

### AND-AND/AND-AND/AND, OR cases ###

# case 1 -- works!!
# ex1 = np.array([1,2,3,4,5])
# ex2 = np.array([4,3,2,1,6])

# case 2 -- works!!
# ex1 = np.array([1,3,2,4,5])
# ex2 = np.array([4,2,3,1,6])

# case 3 -- gotta work on it
# ex1 = np.array([1,3,4,5,6])
# ex2 = np.array([2,6,5,4,3])

# case 4 -- gotta work on it
# ex1 = np.array([1,3,5,4,6])
# ex2 = np.array([2,4,6,3,5])

### AND-AND/AND-AND/AND, AND cases ###

# case 1 -- works!!
# ex1 = np.array([1,2,3,4,5,6])
# ex2 = np.array([4,3,2,1,6,5])

# case 2 -- gotta work on it
# ex1 = np.array([1,2,3,4,5,6])
# ex2 = np.array([2,1,6,5,4,3])

print("ex1: " + str(ex1))
print("ex2: " + str(ex2))

global andDict

ex1, ex2, andNodes, orNodes = mainAlg(ex1, ex2)

andNodes = andNodes.flatten()
tree = reconstruct(andNodes, orNodes, ex1)
print("\n\nRECONSTRUCTED TREE: \n")
print(RenderTree(tree))


#%%
