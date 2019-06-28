
#%%
import numpy as np
from anytree import Node, RenderTree

andDict = dict()
orDict = dict()

############ HELPER FUNCTIONS ############

# find all OR nodes (aka any node in ex1 that is not in ex2 and visa versa)
def findOrNodes(ex1, ex2):
    global orDict

    orNodes = np.empty((0,5), int)
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

def replaceOrNodes(ex, orNodes, ex1):
    for i in range(0,orNodes.size-1):
        if (orNodes[i+1] - orNodes[i]) == 1:
            if (np.isin(orNodes[i], ex) and not np.isin(orNodes[i+1], ex)) or (np.isin(orNodes[i+1], ex) 
            and not np.isin(orNodes[i], ex)): # precaution for OR cases
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
    # checks for special case (AND-AND/AND-AND/AND, OR case 4)
    if not any(andDict):
        for key in graph:
            keyVals = np.empty((0,3), int)
            for i in graph[key]:
                if i > 0 and key > 0:
                    if not np.isin(i, keyVals):
                        keyVals = np.append(keyVals, i)
                    else:
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
                if j < len(ex1) and j < len(ex2): #added this in case of diff length examples
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
                            break
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
            break
    if delKey1 != 10:
        del andDict[delKey1]
    elif delKey2 != 10:
        del orDict[delKey2]

    return ex1, ex2

def orBuilding(ex1, ex2, orNodes):
    global andDict
    global orDict
    
    delKey = delKey2 = 10
    keys = [0] * 4
    if len(ex1) != len(ex2):
        orDict.clear()
        for i in range(0, orNodes.size-1):
            if np.isin(orNodes[i], ex1) and np.isin(orNodes[i+1], ex1):
                newNode = Node("OR")
                node = Node("AND", parent=newNode)
                left = Node(orNodes[i+1], parent=node)
                right = Node(orNodes[i], parent=node)
                orDict[orNodes[i]] = newNode
                delKey = i
        if delKey != 10:
            keys[0] = orNodes[delKey]
            keys[1] = orNodes[delKey+1]
            orNodes = np.delete(orNodes, delKey+1)
            orNodes = np.delete(orNodes, delKey)
        for i in range(0, orNodes.size-1):
            if orNodes[i+1] - orNodes[i] == 1:
                node = Node("OR")
                left = Node(orNodes[i], parent=node)
                right = Node(orNodes[i+1], parent=node)
                orDict[orNodes[i]] = node
                delKey2 = i
        if delKey2 != 10:
            keys[2] = orNodes[delKey2]
            keys[3] = orNodes[delKey2+1]
            orNodes = np.delete(orNodes, delKey2+1)
            orNodes = np.delete(orNodes, delKey2)
        for i in orNodes:
            if not i-1 in orDict:
                if not np.isin(i-1, keys) and not np.isin(i-1, andNodes):
                    node = Node("OR", parent=orDict[keys[0]])
                    left = Node(i-1, parent=node)
                    right = Node(i, parent=node)
            else:
                node = Node("OR", parent=orDict[keys[0]])
                left = Node(i, parent=node)
                right = Node(i+1, parent=node)

    else:
        for key in orDict:
            orPairs = orDict[key].children
            if orPairs[1].name - orPairs[0].name != 1:
                newNode = Node("OR")
                node1 = Node("OR", parent=newNode)
                left = Node(orPairs[0].name, parent=node1)
                right = Node((orPairs[0].name)+1, parent=node1)
                node2 = Node("OR", parent=newNode)
                left2 = Node(orPairs[1].name, parent=node2)
                if (orPairs[1].name)+1 <= 6:
                    right2 = Node((orPairs[1].name)+1, parent=node2)
                else:
                    right2 = Node((orPairs[1].name)-1, parent=node2)
                orDict[orPairs[0].name] = newNode
        if len(orDict.keys()) == 3 or len(andDict.keys()) == 1:
            newNode = Node("OR")
            for i in range(0, orNodes.size-1):
                if np.isin(orNodes[i], ex1) and np.isin(orNodes[i+1], ex1):
                    node = Node("AND", parent=newNode)
                    left = Node(orNodes[i], parent=node)
                    right = Node(orNodes[i+1], parent=node)
                    delKey = i
                elif np.isin(orNodes[i], ex2) and np.isin(orNodes[i+1], ex2):
                    node = Node("AND", parent=newNode)
                    left = Node(orNodes[i], parent=node)
                    right = Node(orNodes[i+1], parent=node)
                    delKey2 = i
            if delKey != 10:
                orDict[orNodes[delKey]] = newNode
            if delKey2 != 10:
                if orNodes[delKey2] in orDict:
                    del orDict[orNodes[delKey2]]
                else:
                    del orDict[orNodes[delKey2+1]]

    return orNodes

def reconstruct(andNodes, orNodes, ex1):
    global andDict
    global orDict
    
    tree = Node("THEN")

    delKey1 = delKey2 = 10
    for key in andDict:
        for key2 in orDict:
            if key > key2 and not np.isin(key, orNodes):
                node = orDict[key2]
                node.parent = tree
                delkey1 = key2
            else:
                if key > key2:
                    node = orDict[key2]
                    node.parent = tree
                    delKey1 = key2
                elif np.isin(key, orNodes):
                    parentNode = Node("AND")
                    node1 = orDict[key]
                    node1.parent = parentNode
                    delKey1 = delKey2 = key
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
                    break
                else:
                    node = andDict[key]
                    node.parent = tree
                    delKey2 = key
    if delKey1 != 10:
        del orDict[delKey1]
    if delKey2 != 10:
        del andDict[delKey2]
    for key in orDict:
        node = orDict[key]
        node.parent = tree
    for key in andDict:
        node = andDict[key]
        node.parent = tree

    return tree
        
def mainAlg(ex1, ex2):
    orNodes = findOrNodes(ex1, ex2)
    #ex2 = replaceOrNodes(ex2, orNodes, ex1)
    graph = initGraph(ex1, ex2)
    andNodes = findAndNodes(graph)
    ex1, ex2 = andBuilding(ex1, ex2)
    orNodes = orBuilding(ex1, ex2, orNodes)
    return ex1, ex2, andNodes, orNodes


#%%

### AND-AND/AND-AND/OR, OR cases ###

# case 1 -- works!!
# ex1 = np.array([1,2,3,5])
# ex2 = np.array([4,2,1,6])

# case 2 -- works!!
# ex1 = np.array([1,3,2,5])
# ex2 = np.array([2,4,1,6])

# case 3 -- works!!
# ex1 = np.array([1,3,4,5])
# ex2 = np.array([2,6,4,3])

# case 4 -- works!!
# ex1 = np.array([1,3,5,4])
# ex2 = np.array([2,4,6,3])

### AND-AND/AND-AND/AND, OR cases ###

# case 1 -- works!!
# ex1 = np.array([1,2,3,4,5])
# ex2 = np.array([4,3,2,1,6])

# case 2 -- works!!
# ex1 = np.array([1,3,2,4,5])
# ex2 = np.array([4,2,3,1,6])

# case 3 -- works!!
# ex1 = np.array([1,3,4,5,6])
# ex2 = np.array([2,6,5,4,3])

# case 4 -- works!!
# ex1 = np.array([1,3,5,4,6])
# ex2 = np.array([2,4,6,3,5])

### AND-AND/AND-AND/AND, AND cases ###

# case 1 -- works!!
# ex1 = np.array([1,2,3,4,5,6])
# ex2 = np.array([4,3,2,1,6,5])

# case 2 -- works!!
# ex1 = np.array([1,2,3,4,5,6])
# ex2 = np.array([2,1,6,5,4,3])

### OR-OR/OR-OR/OR, OR cases ###

# case 1 -- works!!
# ex1 = np.array([1,5])
# ex2 = np.array([3,6])

# case 2 -- works!!
ex1 = np.array([1,2,3])
ex2 = np.array([2,1,6])

### OR-OR/OR-OR/AND, OR cases ###

# case 1 -- works!!
# ex1 = np.array([1,2,5])
# ex2 = np.array([3,6])

# case 2 -- works!!
# ex1 = np.array([1,2,5,6])
# ex2 = np.array([2,1,3])

### OR-OR/AND-OR/AND, OR cases ###

# case 1 -- works!!
# ex1 = np.array([1,2,5])
# ex2 = np.array([3,4,6])

# case 2 -- works!!
# ex1 = np.array([1,2,3,4])
# ex2 = np.array([2,1,6,5])

print("ex1: " + str(ex1))
print("ex2: " + str(ex2))

global andDict

ex1, ex2, andNodes, orNodes = mainAlg(ex1, ex2)

andNodes = andNodes.flatten()
tree = reconstruct(andNodes, orNodes, ex1)
print("\n\nRECONSTRUCTED TREE: \n")
print(RenderTree(tree))


#%%
