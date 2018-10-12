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

def generateMaze(nodelist, runDirection='RIGHT', updownDirection='UP'):
    run = []
    for node in nodelist:
        if (node.neighbors[updownDirection] is not None):
            run.append(node)
            val = randint(0,1)
            if val == 1 or node.neighbors[runDirection] is None:
                val2 = randint(0, len(run)-1)
                for i in range(len(run)):
                    if i != val2:
                        run[i].removePath(updownDirection)
                node.removePath(runDirection)
                run = []
            

            
