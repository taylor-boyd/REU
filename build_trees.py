import node
import random

## Node type encoding ##
# 0 = THEN
# 1 = OR
# 2 = AND
# 3# = PLACE_#

global PLACE_NODE 
PLACE_NODE = 0

# helper function that prints possible tree combinations
def printCombos(combos, file):
	for i in combos:
		for j in i:
			file.write(str(j))
			file.write(" ")
		file.write(",")
	file.write("\n")

# helper function that gets node name aka whether it is THEN, AND, OR
def getNodeName(num):
    if num == 0:
        return "THEN"
    elif num == 1:
        return "OR"
    else:
        return "AND"

# generates tree
def genTree(max_depth, cur_depth):

    PLACE_NODE = 0

    # generate a random number between 0 and 100,000 (inclusive)
    x = random.randint(0,100000)

    # node type is based off random number generated
    node_type = x % 3
    cur_depth += 1

    if node_type != 3 and cur_depth <= max_depth:
        newNode = node.Node(node_type, node_type) # (data, node_type)
        print("Depth " + str(cur_depth) + ": " + getNodeName(node_type))
        newNode.insert_left(genTree(max_depth, cur_depth))
        newNode.insert_right(genTree(max_depth, cur_depth))
        return newNode
    elif cur_depth == (max_depth + 1):
        l = random.randint(0, 8)
        r = random.randint(0, 8)
        print(l)
        #print("Left: " + str(l))
        #print("Right: " + str(r))

# user enters output file name and tree restrictions
#file_name = input("Enter output file name: ")
#max_depth = input("Enter max depth of randomly generated trees: ")
#max_depth = int(max_depth)

# testing purposes
file_name = "trees2.txt"
max_depth = 3

# open file to write possible tree combos to
file = open(file_name, "w")

# generate random number between 0 and 100,000 (inclusive)
random.seed()
x = random.randint(0, 100000)

# beginning node type (0-3) is based off random number generated
node_type = x % 3
print("Beginning node: " + str(node_type))
cur_depth = 1

if node_type != 3 and cur_depth <= max_depth:
    print("ROOT NODE:      " + getNodeName(node_type) + " ")
    tree = node.Node(node_type, node_type)
    tree.insert_left(genTree(max_depth, cur_depth)) # (data, node_type)
    tree.insert_right(genTree(max_depth, cur_depth))
    
#tree.PrintTree() # function inside of node.py
#tree.PrintTreeToFile(file) # another function inside of node.py
#file.write("\n")
#x = tree.genCombos()
#printCombos(x, file)

#x = tree.genCombos()

#print("GENRATED Combos: \n")
#print(x)
file.close()