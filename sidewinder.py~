from random import randint

'''In the binary tree algorithm, we visit each node (in any order) 
and then randomly choose a direction (direction1 or direction2).
Whichever of the 2 directions we choose, we remove the path between
the 2 nodes.  If the node only has 1 of the 2 paths, then we don't do anything.
'''

def generateMaze(nodelist, direction1='UP', direction2='RIGHT'):
    for node in nodelist:
        if (node.neighbors[direction1] is not None and 
            node.neighbors[direction2] is not None):
            val = randint(0,1)
            if val == 0:
                node.removePath(direction1)
            else:
                node.removePath(direction2)
