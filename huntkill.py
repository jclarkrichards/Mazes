from random import randint
from stacks import Stack
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
    #print "start = " + str(node.row) + ", " + str(node.column)
    stack = Stack()
    
    unvisitedNeighbors = nodes.getUnvisitedNeighbors(node)
    #print len(unvisitedNeighbors)
    
    while not allNodesVisited:
        unvisitedNeighbors = nodes.getUnvisitedNeighbors(node)
        #print "Unvisited Neighbors = " + str(len(unvisitedNeighbors))
        if len(unvisitedNeighbors) > 0:
            index = randint(0, len(unvisitedNeighbors)-1)
            nodeNext = unvisitedNeighbors[index]
            direction = nodes.getDirectionFromNodes(node, nodeNext)
            nodes.addPath(node, direction)
            node = nodeNext
            node.visited = True
            #print "node => " + str(node.row) + ", " + str(node.column)
            
        else:
            #print "HUNT AND KILL"
            unvisitedNodes = nodes.getUnvisitedNodes()
            if len(unvisitedNodes) > 0:
                for n in unvisitedNodes:
                    visitedNeighbors = nodes.getVisitedNeighbors(n)
                    if len(visitedNeighbors) > 0:
                        node = n
                        break
                visitedNeighbors = nodes.getVisitedNeighbors(node)
                if len(visitedNeighbors) > 1:
                    i = randint(0, len(visitedNeighbors)-1)
                    temp = visitedNeighbors[i]
                else:
                    temp = visitedNeighbors[0]
                direction = nodes.getDirectionFromNodes(node, temp)
                nodes.addPath(node, direction)
                node.visited = True
                
            else:
                allNodesVisited = True

    

    
            

        
    
