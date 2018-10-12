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
    nodeEnd = nodes.nodeList[index]
    nodeEnd.visited = True
    allNodesVisited = False
    #print "start = " + str(index)
    stack = Stack()

    while not allNodesVisited:
        unvisitedNodes = nodes.getUnvisitedNodes()
        index = randint(0, len(unvisitedNodes)-1)
        nodeStart = unvisitedNodes[index]
        endFound = False
        stack.push(nodeStart)
        while not endFound:
            directionList = nodes.getDirections(stack.peek())
            directionIndex = randint(0, len(directionList)-1)
            direction = directionList[directionIndex]
            nodeNext = nodes.getUnlinkedNode(stack.peek(), direction)
            if not nodeNext.visited:
                if stack.contains(nodeNext):
                    while stack.peek() is not nodeNext:
                        stack.pop()
                else:
                    stack.push(nodeNext)
            else:
                #Carve out the path that is defined by the stack
                stack.push(nodeNext)
                endFound = True
                while not stack.isEmpty():
                    node1 = stack.pop()
                    node2 = stack.peek()
                    node1.visited = True
                    if node2 is not None:
                        #print node1, node2
                        direction = nodes.getDirectionFromNodes(node1, node2)
                        nodes.addPath(node1, direction)
                    else:
                        stack.clear()
                    
        unvisitedNodes = nodes.getUnvisitedNodes()
        if len(unvisitedNodes) == 0:
            allNodesVisited = True

    
            

        
    
