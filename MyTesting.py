
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

    for key in andDict:
        index1 = index2 = index3 = index4 = 0
        for i in range(0,ex1.size-1):
            for j in andDict[key].children:
                if ex1[i] == j.name:
                    index1 += i
                    print(index1)
                if ex2[i] == j.name:
                    index2 += i
                    print(index2)
        if index1 != index2:
            newNode = Node("AND")
            newLeft = andDict[key]
            newLeft.parent = newNode
            print('\n')
            if (index1 - index2) == 2 or (index2 - index1) == 2:
                for key2 in orDict:
                    for i2 in range(0,ex1.size-1):
                        if ex1[i2] == key2:
                            index3 += i2
                        if ex2[i2] == key2:
                            index4 += i2
                    if index3 != index4:
                        if (index3 - index4) == 2 or (index4 - index3) == 2:
                            newRight = orDict[key2]
                            newRight.parent = newNode   
                            del orDict[key2] 
                            break                    
            else:
                if (index1 - index2) == 4 or (index2 - index1) == 4:
                    newRight = andDict[key+2]
                    newRight.parent = newNode
                    del andDict[key+2]
            andDict[key] = newNode  
    return ex1, ex2

def mergeAnds(ex, andNodes):
    andNodesNew = np.array([])
    for i in andNodes:
        index = np.argwhere(ex==i[0])
        ex = np.delete(ex, index)
        andNodesNew = np.append(andNodesNew, int(i[1]))
    return (ex, andNodesNew)

def reconstruct(andNodes, orNodes, ex1):
    global andDict
    global orDict
    
    tree = Node("THEN")
    # Look for ORs in ANDs using andNodes
    

    return tree
        
def mainAlg(ex1, ex2):
    orNodes = findOrNodes(ex1, ex2)
    ex2 = replaceOrNodes(ex2, orNodes)
    graph = initGraph(ex1, ex2)
    andNodes = findAndNodes(graph)
    ex1, ex2 = andBuilding(ex1, ex2)
    #ex1, tempAnds = mergeAnds(ex1, andNodes)
    #ex2, andNodes = mergeAnds(ex2, andNodes)
    return ex1, ex2, andNodes, orNodes


#%%
# case 1 -- works!!
# ex1 = np.array([1,2,3])
# ex2 = np.array([2,1,4])

# case 1.2 -- works!!
# ex1 = np.array([1,3,4])
# ex2 = np.array([2,4,3])

#case 3 -- works!!
# ex1 = np.array([1,2,3,4,5])
# ex2 = np.array([4,3,2,1,6])

#case 3.2 -- works!!
# ex1 = np.array([1,3,4,5,6])
# ex2 = np.array([2,6,5,4,3])

# case 4 -- works!!
# ex1 = np.array([1,2,3,4,5,6])
# ex2 = np.array([4,3,2,1,6,5])

# case 4.2 -- works!!
# ex1 = np.array([1,2,3,4,5,6])
# ex2 = np.array([2,1,6,5,4,3])

# case 5 -- two or's - not werkin
# ex1 = np.array([1,3])
# ex2 = np.array([2,4])

# case 5 -- two and's -- does not work 
# ex1 = np.array([1,2,3,4])
# ex2 = np.array([2,1,4,3])

#case 2 -- how do we get this to work???
# ex1 = np.array([1,2,3,4])
# ex2 = np.array([3,2,1,5])

# new case
ex1 = np.array([1,2,3,5])
ex2 = np.array([4,2,1,6])

print("ex1: " + str(ex1))
print("ex2: " + str(ex2))

global andDict

# while len(ex1) != 2:
ex1, ex2, andNodes, orNodes = mainAlg(ex1, ex2)

andNodes = andNodes.flatten()
tree = reconstruct(andNodes, orNodes, ex1)
print("\n\nRECONSTRUCTED TREE: \n")
print(RenderTree(tree))

#%%
#ex1, ex2, andNodes, orNodes = mainAlg(ex1, ex2)
print("ex1: " + str(ex1))
print("ex2: " + str(ex2))
print('\n')
print(andNodes)
print('\n')
print(orNodes)
print('\n')
print(andDict)
print('\n')
for i in andDict:
    print(andDict[i].children)
print('\n')
print(RenderTree(andDict[2]))
print(RenderTree(orDict[5]))

#%%
