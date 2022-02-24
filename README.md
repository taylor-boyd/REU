# Hierarchical Task Learning Through Human Demonstration

### Project Abstract:
&nbsp; In order for robots to carry out a task sequence, it must be translated in such a way that they can understand. One way this can be done is by using a task tree representation. Currently this method does not allow robots and humans to collaborate without interruption as hard coding of the task tree is required. One solution to this is to enable robots to construct task trees themselves. After observing a human demonstrate a repeated series of tasks, the robot would then use the different sequences to build and store a corresponding hierarchical task tree representation. The accuracy of the constructed task tree can be validated through the comparison of the robot's completion of the task and the human's original demonstration as well as the robot's ability to complete the task in more ways than one. Upon validation, this process will allow human-robot interactions to remain continuous and enable those without a computer science background to collaborate with robots as well. 
<br />
&nbsp; Link to research paper (incomplete): https://www.overleaf.com/read/mvzxrhhtknjq

### Dependencies:
&nbsp; NumPy  
&nbsp;&nbsp; download with "pip install numpy"  
<br />
&nbsp; AnyTree  
&nbsp;&nbsp; download with "pip install anytree"
<br />
<br />
&nbsp; Distributed_Collaborative_Task_Tree
<br />
&nbsp;&nbsp; code and instructions at https://github.com/UNR-RoboticsResearchLab/Distributed_Collaborative_Task_Tree
<br />
&nbsp;&nbsp; my code is in the 'taylor_while' branch; this where 'sequence_builder.cc' can be found

### How to run:
&nbsp; MainAlg-Copy1.py
<br />
&nbsp; This file is just an un-documented copy of Main_Documented.py.
<br />

&nbsp; Main_Documented.py
<br />
&nbsp; This is the main program that takes in 2 well-representative task sequences and outputs a corresponding hierarchical task tree. The trees that can be correctly reconstructed must have a root 'THEN' node and a maximum depth of 3; all nodes other than the root can be either 'AND' or 'OR'.
<br />
&nbsp;&nbsp; test.txt has a whole bunch of possible task sequences that have been used to test the accuracy of Main_Documented
<br />
&nbsp; MyTesting.py
<br />
&nbsp; This file is an extension of Main_Documented that doesn't pass all tests. It's an attempt at constructing hierarchical task trees that include 'THEN' nodes outside of the root and trees with a larger depth than 3.
<br />
&nbsp; Main_testscript.py
<br />
&nbsp; This program allows Main_Documented to interface with sequence_builder.cc. The output file from sequence_builder.cc that contains observed task sequences can be inputted to this file so that they can be put into the right format to be entered into Main_Documented.py and the constructed hierarchical task tree can be displayed in the terminal.
<br />
&nbsp;&nbsp; seq.txt is an example of what an output file from sequence_builder.cc would look like; it can be used to make sure Main_testscript works
<br />