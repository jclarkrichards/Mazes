from random import randint

'''In the Sidewinder algorithm, we visit each node once.
For each node we choose a random direction from a possible 2 directions.
If we choose direction1, then we continue to the next node and add the node
to our <run>.  As soon as we choose direction2 we need to then choose a random
node in our <run> list and then remove the paths in all of the other nodes in that 
<run>.  We also remove the direction1 path on the node when we choose a direction2. 
We have to take care of each row before we can move to another row.  
We can choose any random row though, we don't have to go in order.
'''

def generateMaze(nodes):
    nodes.getEmptyGrid()
    index = randint(0, len(nodes.nodeList)-1)
    node = nodes.nodeList[index]
    node.visited = True
    allNodesVisited = False
    print "start = " + str(index)

    while not allNodesVisited:
        directionList = nodes.getDirections(node)
        #print directionList
        directionIndex = randint(0, len(directionList)-1)
        direction = directionList[directionIndex]
        nodeNext = nodes.getUnlinkedNode(node, direction)
        if not nodeNext.visited:
            nodes.addPath(node, direction)
            node = nodeNext
            node.visited = True
        else:
            node = nodeNext

        allNodesVisited = True
        for i in range(len(nodes.nodeList)):
            if not nodes.nodeList[i].visited:
                allNodesVisited = False
                break

    
            

        
    
