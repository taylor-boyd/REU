import numpy as np

class Node:

    def __init__(self, data, node_type):

        self.left = None
        self.right = None
        self.data = data
        self.node_type = node_type

    def insert_left(self, data):
        self.left = data 

    def insert_right(self, data):
        self.right = data

    def getNodeName(self,num):
        if num == 0: # THEN
            return "THEN"
        elif num == 1: # OR
            return "OR"
        elif num == 2: # AND
            return "AND"
        else: # PLACE
            return "PLACE"

    # Print the tree
    def PrintTree(self):
        if self.getNodeName(self.node_type) != "P":
            print(self.getNodeName(self.node_type))
        else:
            print(str(self.data))
        if self.left:
            self.left.PrintTree()
        if self.right:
            self.right.PrintTree()

    def PrintTreeToFile(self, file):
        if self.getNodeName(self.node_type) != "P":
            file.write(self.getNodeName(self.node_type))
        else:
            file.write(str(self.data))
        file.write(" ")
        if self.left:
            self.left.PrintTreeToFile(file)
        if self.right:
            self.right.PrintTreeToFile(file)

    # generate possible combintions of a single tree
    def genCombos(self):
        vec = []
        if self.node_type == 3:
            vec.append([self.data])
            return vec
        if self.left.node_type == 3 and self.right.node_type == 3:
            if self.node_type == 2:
                vec.append([self.left.data, self.right.data])
                vec.append([self.right.data, self.left.data])
            elif self.node_type == 1:
                vec.append([self.left.data])
                vec.append([self.right.data])
            elif self.node_type == 0:
                vec.append([self.left.data, self.right.data])
            print(vec)
            return vec
        if self.node_type == 0: #THEN
            vector_left = self.left.genCombos()
            vector_right = self.right.genCombos()
            for i in vector_left:
                for j in vector_right:
                    vec.append(np.concatenate((i, j)))
            print(vec)
            return vec
        elif self.node_type == 2: #AND
            vector_left = self.left.genCombos()
            print("LEFT: " + str(vector_left))
            vector_right = self.right.genCombos()
            print("RIGHT: " + str(vector_right))
            for i in vector_left:
                for j in vector_right:
                    print(i)
                    print(j)
                    vec.append(np.concatenate((i, j)))
                    vec.append(np.concatenate((j, i)))
            print(vec)
            return vec
        elif self.node_type == 1: #OR
            vector_left = self.left.genCombos()
            print("LEFT OR: " + str(vector_left))
            vector_right = self.right.genCombos()
            print("RIGHT OR: " + str(vector_right))
            for i in vector_left:
                vec.append(i)
            for j in vector_right:
                vec.append(j)
            return vec