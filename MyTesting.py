
#%%
import numpy as np
from anytree import Node, RenderTree

andDict = dict()
orDict = dict()
thenDict = dict()

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

# replaces OR node value from ex2 with pairs (from ex1)
def replaceOrNodes(ex, orNodes, ex1):
    if not len(ex1) <= 2 and not len(ex2) <= 2:
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

# looks for THEN nodes (there will be 2 of the same vals for a key)
def findThenNodes(graph, andNodes, orNodes):
    global thenDict
    thenNodes = np.empty((0,2), int)
    for key in graph:
        keyVals = np.empty((0,3), int)
        for i in graph[key]:
            if i > 0 and key > 0:
                if not np.isin(i, keyVals):
                    keyVals = np.append(keyVals, i)
                elif not np.isin(i, andNodes) and not np.isin(key, andNodes):
                    if not np.isin(i, orNodes) and not np.isin(key, orNodes):
                        node = Node("THEN")
                        if i < key:
                            thenNodes = np.concatenate((thenNodes, [[i, key]]), axis=0)
                            left = Node(i, parent=node)
                            right = Node(key, parent=node)
                        else:
                            thenNodes = np.concatenate((thenNodes, [[key, i]]), axis=0)
                            left = Node(key, parent=node)
                            right = Node(i, parent=node)
                        if i not in thenDict:
                            thenDict[i] = node
    return thenNodes

# looks for larger AND relationships
def andBuilding(ex1, ex2, andNodes, orNodes):
    global andDict
    global orDict
    # if samples are diff lengths, we'll choose smaller one to stay in bounds
    if ex1.size <= ex2.size: 
        ex = ex1
    else: 
        ex = ex2
    for i in range(0,ex.size-1):
        if ex1[i] != ex2[i] and andNodes.size > 2:
            if ex[i] in andDict:
                for j in range(0, len(andNodes)):
                    for k in andNodes[j]:
                        for child in andDict[ex[i]].children:
                            if k == child.name and k != ex[i] and (k - ex[i] == 1 or ex[i] - k == 1):
                                val = k
                                index1 = np.argwhere(ex1==val)
                                index2 = np.argwhere(ex2==val)
                                newNode = Node("AND")
                                newLeft = andDict[ex[i]]
                                newLeft.parent = newNode
                                if index1 != index2:             # both indices do not match so AND is
                                    if j+1 < len(andNodes):      # parent of AND and AND node
                                        key = andNodes[j+1][1]     
                                    else:
                                        key = andNodes[j-1][1]
                                    newRight = andDict[key]
                                    newRight.parent = newNode
                                    del andDict[key]
                                    andDict[ex[i]] = newNode
                                else:                               # one index does not match so AND is
                                    for i2 in range(0,ex1.size):    # parent of AND and OR node
                                        if ex1[i2] != ex2[i2]:
                                            if ex[i2] in orDict:
                                                newRight = orDict[ex[i2]]
                                                newRight.parent = newNode
                                                del orDict[ex[i2]]
                                break

    return ex1, ex2

# OR values are replaced back to original so that indices can be used to
# determine hierarchical OR relationships in next method
def swapBack(ex, orNodes, ex1):
    if not len(ex1) <= 2 and not len(ex2) <= 2: # if length is less than 2, depth is less than 3
        for i in range(0,orNodes.size-1):       # so swapping doesn't matter (there's no higher OR relationships to be found)
            if np.isin(orNodes[i], ex) and np.isin(orNodes[i], ex1):
                if np.isin(orNodes[i+1], ex):
                    if np.isin(orNodes[i+1]+1, orNodes):
                        ex = np.where(ex==orNodes[i+1], int(orNodes[i+2]), ex)
                ex = np.where(ex==orNodes[i], int(orNodes[i+1]), ex)
    return ex

# looks for larger OR relationships
def orBuilding(ex1, ex2, orNodes, andNodes):
    global andDict
    global orDict
    
    keys = [0] * 4
    # different lengths indicates OR-OR/OR-OR/AND relationship
    if len(ex1) != len(ex2):
        orDict.clear()
        for i in range(0, orNodes.size-1):         # if OR node pair is in one ex only, it's the AND node child
            if ((np.isin(orNodes[i], ex1) and np.isin(orNodes[i+1], ex1)) or 
                        (np.isin(orNodes[i], ex2) and np.isin(orNodes[i+1], ex2))):
                newNode = Node("OR")
                node = Node("AND", parent=newNode)
                left = Node(orNodes[i+1], parent=node)
                right = Node(orNodes[i], parent=node)
                orDict[orNodes[i]] = newNode
                keys[0] = orNodes[i]
                keys[1] = orNodes[i+1]
        for i in range(0, orNodes.size-1):          # this is for OR nodes outside of branch being built
            if orNodes[i+1] - orNodes[i] == 1 and not np.isin(orNodes[i], keys):
                node = Node("OR")
                left = Node(orNodes[i], parent=node)
                right = Node(orNodes[i+1], parent=node)
                orDict[orNodes[i]] = node
                keys[2] = orNodes[i]
                keys[3] = orNodes[i+1]
        for i in orNodes:                          
            if not i in orDict and not np.isin(i, keys):
                node = Node("OR", parent=orDict[keys[0]])
                if not np.isin(i-1, keys) and not np.isin(i-1, andNodes) and i-1 > 0:
                    left = Node(i-1, parent=node)
                    right = Node(i, parent=node)
                else:
                    left = Node(i, parent=node)
                    right = Node(i+1, parent=node)
    else:                               # looks for OR-OR/OR-OR/OR relationship or
        for key in orDict:              # OR-OR/AND-OR/AND relationship
            orPairs = orDict[key].children
            if orPairs[1].name - orPairs[0].name != 1:  # OR-OR/OR-OR/OR
                newNode = Node("OR")
                node1 = Node("OR", parent=newNode)
                left = Node(orPairs[0].name, parent=node1)
                right = Node((orPairs[0].name)+1, parent=node1)
                node2 = Node("OR", parent=newNode)
                left2 = Node(orPairs[1].name, parent=node2)
                if (orPairs[1].name)-1 != (orPairs[0].name)+1:
                    right2 = Node((orPairs[1].name)-1, parent=node2)
                else:
                    right2 = Node((orPairs[1].name)+1, parent=node2)
                orDict[orPairs[0].name] = newNode
        if len(orDict.keys()) == 3 or len(andDict.keys()) == 1:     # OR-OR/AND-OR/AND
            newNode = Node("OR")
            for i in range(0, orNodes.size-1):
                if np.isin(orNodes[i], ex1) and np.isin(orNodes[i+1], ex1):
                    node = Node("AND", parent=newNode)
                    left = Node(orNodes[i], parent=node)
                    right = Node(orNodes[i+1], parent=node)
                    orDict[orNodes[i]] = newNode
                elif np.isin(orNodes[i], ex2) and np.isin(orNodes[i+1], ex2):
                    node = Node("AND", parent=newNode)
                    left = Node(orNodes[i], parent=node)
                    right = Node(orNodes[i+1], parent=node)
                    if orNodes[i] in orDict:
                        del orDict[orNodes[i]]
                    else:
                        del orDict[orNodes[i+1]]
    return orNodes

# constructs final task tree and looks for any missed relationships
def reconstruct(andNodes, orNodes, ex1):
    global andDict
    global orDict
    global thenDict
    
    tree = Node("THEN")
    
    if andNodes.size <= orNodes.size:
        short = andNodes
    else:
        short = orNodes
    for i in range(0, short.size-1, 2):
        # adds OR nodes to tree
        if andNodes[i] > orNodes[i] and not np.isin(orNodes[i], andNodes):
            if orNodes[i] in orDict:
                node = orDict[orNodes[i]]
                del orDict[orNodes[i]]
            elif orNodes[i+1] in orDict:
                node = orDict[orNodes[i+1]]
                del orDict[orNodes[i+1]]
            node.parent = tree
        # looks for and adds AND-AND/AND-AND/OR or AND-AND/OR-AND/OR branch to tree
        if (np.isin(andNodes[i], orNodes) or np.isin(orNodes[i], andNodes)) and any(orDict):
            parentNode = Node("AND")
            if andNodes[i] in orDict:
                node1 = orDict[andNodes[i]]
                del orDict[andNodes[i]]
            else:
                node1 = orDict[orNodes[i]]
                del orDict[orNodes[i]]
            node1.parent = parentNode
            for key in andNodes:                        # AND-AND/AND-AND/OR
                if key in andDict and key not in orDict:
                    del andDict[key]
                    node2 = Node("AND", parent=parentNode)
                    for key2 in andNodes:
                        if not np.isin(key2, orNodes):
                            left = Node(key2, parent=node2)
                            if not np.isin(key2+1, orNodes) and np.isin(key2+1, andNodes):
                                right = Node(key2+1, parent=node2)
                            else:
                                right = Node(key2-1, parent=node2)
                            break
                    break
            if any(andDict) and len(parentNode.children) < 2:                                   # AND-AND/OR-AND/OR
                for key in orNodes:
                    if key in orDict and key in andNodes:
                        node2 = orDict[key]
                        del andDict[key]
                        del orDict[key]
                        node2.parent = parentNode
                        break
            parentNode.parent = tree
        # adds AND nodes to tree
        elif andNodes[i+1] not in orDict and any(andDict):
            node = andDict[andNodes[i+1]]
            node.parent = tree

    # adds THEN nodes
    for key in thenDict:
        if any(orDict):
            for key2 in orNodes:
                if key2 in orDict and key > key2:
                    node = orDict[key2]
                    node.parent = tree
                    del orDict[key2]
        if any(andDict):
            for key3 in andNodes:
                if key3 in andDict and key > key3:
                    node = andDict[key3]
                    node.parent = tree
                    del andDict[key3]
        node = thenDict[key]
        node.parent = tree

    # adds remaining nodes
    for i in andNodes:
        for j in orNodes:
            if i in andDict and i < j:
                node = andDict[i]
                node.parent = tree
            elif j in orDict:
                node = orDict[j]
                node.parent = tree
    for key in orDict:
        node = orDict[key]
        node.parent = tree
    for key in andDict:
        node = andDict[key]
        node.parent = tree

    return tree
        
def mainAlg(ex1, ex2):
    orNodes = findOrNodes(ex1, ex2)
    ex2 = replaceOrNodes(ex2, orNodes, ex1)
    graph = initGraph(ex1, ex2)
    andNodes = findAndNodes(graph)
    thenNodes = findThenNodes(graph, andNodes, orNodes)
    ex1, ex2 = andBuilding(ex1, ex2, andNodes, orNodes)
    ex2 = swapBack(ex2, orNodes, ex1)
    orNodes = orBuilding(ex1, ex2, orNodes, andNodes)
    return ex1, ex2, andNodes, orNodes


#%%

### Depth of 3 on both sides ###

# case 1 -- works!!
ex1 = np.array([1,2,3,4,5])
ex2 = np.array([4,3,2,1,7])

# case 2 -- works!!
# ex1 = np.array([1,3,2,5,7])
# ex2 = np.array([2,4,1,8,6])

# case 3 -- works!!
# ex1 = np.array([1,5,6])
# ex2 = np.array([4,8,7])

# case 4 -- works!!
# ex1 = np.array([1,5,7,8])
# ex2 = np.array([4,3,8,7,6])

# case 5 -- works!!
# ex1 = np.array([1,5])
# ex2 = np.array([4,8])

# case 6 -- works!!
# ex1 = np.array([1,2,3,4,5,6,7,8])
# ex2 = np.array([4,3,2,1,8,7,6,5])

### THEN and AND ###

# case 1 -- works!!
# ex1 = np.array([1,2,3,4])
# ex2 = np.array([1,2,4,3])

# case 2 -- works!!
# ex1 = np.array([1,2,3,4])
# ex2 = np.array([2,1,3,4])

### THEN and OR ###

# case 1 -- works!!
# ex1 = np.array([1,2,3])
# ex2 = np.array([1,2,4])

# case 2 -- works!!
# ex1 = np.array([1,3,4])
# ex2 = np.array([2,3,4])

### THEN branch ###

# case 1 -- works!!
# ex1 = np.array([1,2,3,4,5,6])
# ex2 = np.array([4,3,2,1,5,6])

# case 2 -- works!!
# ex1 = np.array([1,2,3])
# ex2 = np.array([1,2,6])

### THEN at depth 3 ###

# case 1 -- treats THEN as AND
# ex1 = np.array([1,2,3,5])
# ex2 = np.array([4,1,2,6])

# AND-AND/AND-AND/AND, OR
# ex1 = np.array([1,3,6,4,5])
# ex2 = np.array([2,3,5,4,6])

### reconstruct testing ###

# case 1 -- works!!
# ex1 = np.array([1,3,2,5])
# ex2 = np.array([2,4,1,6])

# case 2 -- works!!
# ex1 = np.array([1,3,5,4])
# ex2 = np.array([2,4,6,3])

# case 1 -- works!!
# ex1 = np.array([1,3,5,6])
# ex2 = np.array([4,2,6,5])

# case 2 -- works!!
# ex1 = np.array([1,3,5])
# ex2 = np.array([2,6,4])

print("ex1: " + str(ex1))
print("ex2: " + str(ex2))

global andDict

ex1, ex2, andNodes, orNodes = mainAlg(ex1, ex2)

andNodes = andNodes.flatten()
tree = reconstruct(andNodes, orNodes, ex1)
print("\n\nRECONSTRUCTED TREE: \n")
print(RenderTree(tree))


#%%
