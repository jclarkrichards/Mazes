import pygame
from random import randint
from vectors import Vector2D
from numpy import loadtxt
"""The link dictionary shows which nodes are connected to each other.  
This does not change.  If we want to know what nodes we can connect then 
we can just consult this dictionary.
"""

class Node(object):
    def __init__(self, x, y, row, column, dx, dy):
        self.row, self.column = row, column
        self.position = Vector2D(x + column*dx, y + row*dy)
        self.neighbors = {'UP':None, 'DOWN':None, 'LEFT':None, 'RIGHT':None}
        self.color = (255,0,0)
        self.visited = False

    def __eq__(self, node):
        if self.row == node.row and self.column == node.column:
            return True
        return False

    def getNeighborKeys(self):
        '''Return the neighbor keys ('UP', 'DOWN', 'LEFT', or 'RIGHT') that are not None'''
        result = []
        for key in self.neighbors.keys():
            if self.neighbors[key] is not None:
                result.append(key)
        return result

    def redundantNode(self):
        '''A node is redundant if it only has 2 paths, and those 2 paths are opposite
        of each other, i.e. UP and DOWN or LEFT and RIGHT'''
        numneighbors = 0
        directions = []
        for key in self.neighbors.keys():
            if self.neighbors[key] is not None:
                numneighbors += 1
                directions.append(key)

        if numneighbors == 2:
            vlist = []
            for d in directions:
                if d == 'UP' or d == 'DOWN':
                    vlist.append(Vector2D(0,1))
                else:
                    vlist.append(Vector2D(1,0))
            dotpro = vlist[0].dot(vlist[1])
            if dotpro == 0:
                return False
            return True
                
        else:
            return False

    def unvisitedNeighbors(self):
        '''Return a list of unvisited neighbors'''
        results = []
        for key in self.neighbors.keys():
            if self.neighbors[key] is not None:
                if self.neighbors[key].visited == False:
                    results.append(self.neighbors[key])
        return results

    def getDirections(self):
        directionList = []
        for key in self.neighbors.keys():
            if self.neighbors[key] is not None:
                directionList.append(key)
        return directionList

    def removePath(self, direction):
        if self.neighbors[direction] is not None:
            oppositeDirection = self.getOppositeDirection(direction)
            self.neighbors[direction].neighbors[oppositeDirection] = None
            self.neighbors[direction] = None

    def getOppositeDirection(self, direction):
        if direction == 'UP':
            return 'DOWN'
        if direction == 'DOWN':
            return 'UP'
        if direction == 'LEFT':
            return 'RIGHT'
        if direction == 'RIGHT':
            return 'LEFT'

    def isDeadend(self):
        temp = 0
        for key in self.neighbors.keys():
            if self.neighbors[key] is not None:
                temp += 1
        if temp == 1: return True
        return False

    def render(self, screen):
        for n in self.neighbors.keys():
            if self.neighbors[n] is not None:
                pygame.draw.line(screen, (255,255,255), self.position.toTuple(), self.neighbors[n].position.toTuple(), 2)

        pygame.draw.circle(screen, self.color, self.position.toTuple(), 6)


class NodeGroup(object):
    def __init__(self, x=0, y=0, rows=0, columns=0, dx=16, dy=16):
        self.rows, self.columns = rows, columns
        self.dx, self.dy = dx, dy
        self.x, self.y = x, y
        self.nodeList = []
        self.linkList = []
        self.usingPacmanTemplate = False
        self.createNodeList(self.nodeList)
        #self.makeNodePaths(self.nodeList)
        self.createNodeList(self.linkList)
        #self.makeNodePaths(self.linkList)
        self.linkPaths()

    def linkPaths(self):
        self.makeNodePaths(self.nodeList)
        self.makeNodePaths(self.linkList)

    def createNodeList(self, tempList):
        for row in range(self.rows):
            for column in range(self.columns):
                tempList.append(Node(self.x, self.y, row, column, self.dx, self.dy))

    def makeNodePaths(self, tempList):
        for node in tempList:
            node.neighbors['UP'] = self.getNode(node.row-1, node.column)
            node.neighbors['DOWN'] = self.getNode(node.row+1, node.column)
            node.neighbors['LEFT'] = self.getNode(node.row, node.column-1)
            node.neighbors['RIGHT'] = self.getNode(node.row, node.column+1)
            
    def createNodeListPacmanStyle(self, tempList):
        grid = loadtxt("template.txt", dtype=str)
        self.rows, self.columns = grid.shape
        for row in range(self.rows):
            for column in range(self.columns):
                if grid[row][column] != 'x':
                    tempList.append(Node(self.x, self.y, row, column, self.dx, self.dy))
        
    def usePacmanTemplate(self):
        self.nodeList = []
        self.linkList = []
        self.usingPacmanTemplate = True
        self.createNodeListPacmanStyle(self.nodeList)
        self.createNodeListPacmanStyle(self.linkList)
        #self.makeNodePaths(self.nodeList)
        #self.makeNodePaths(self.linkList)
        self.linkPaths()

    def addPath(self, node, direction):
        if direction == 'UP':
            otherNode = self.getNode(node.row-1, node.column)
            node.neighbors['UP'] = otherNode
            otherNode.neighbors['DOWN'] = node
        elif direction == 'DOWN':
            otherNode = self.getNode(node.row+1, node.column)
            node.neighbors['DOWN'] = otherNode
            otherNode.neighbors['UP'] = node            
        elif direction == 'LEFT':
            otherNode = self.getNode(node.row, node.column-1)
            node.neighbors['LEFT'] = otherNode
            otherNode.neighbors['RIGHT'] = node
        else:
            otherNode = self.getNode(node.row, node.column+1)
            node.neighbors['RIGHT'] = otherNode
            otherNode.neighbors['LEFT'] = node
            
    def getNode(self, row, column):
        for node in self.nodeList:
            if node.row == row and node.column == column:
                return node
        return None

    def getNodeFromLink(self, row, column):
        for node in self.linkList:
            if node.row == row and node.column == column:
                return node
        return None

    def getEmptyGrid(self):
        '''If we want a grid without the initial connections'''
        self.nodeList = []
        if self.usingPacmanTemplate:
            self.createNodeListPacmanStyle(self.nodeList)
        else:
            self.createNodeList(self.nodeList)

    def getPossibleDirections(self, node):
        '''Consult the links dictionary to get the possible directions for a node 
        at index'''
        return node.getDirections()

    def getUnlinkedNode(self, node, direction):
        if direction == 'UP':
            return self.getNode(node.row-1, node.column)
        elif direction == 'DOWN':
            return self.getNode(node.row+1, node.column)
        elif direction == 'LEFT':
            return self.getNode(node.row, node.column-1)
        else:
            return self.getNode(node.row, node.column+1)

    def getDirections(self, node):
        lnode = self.getNodeFromLink(node.row, node.column)
        return lnode.getDirections()

    def getUnvisitedNodes(self):
        '''Return all of the unvisited nodes in the maze'''
        unvisitedNodes = []
        for node in self.nodeList:
            if not node.visited:
                unvisitedNodes.append(node)
        return unvisitedNodes

    def getUnvisitedNeighbors(self, node):
        '''Return the unvisited neighbor nodes of the input node'''
        #print "---------------------"
        #print node
        #print str(node.row) + ", " + str(node.column)
        linknode = self.getNodeFromLink(node.row, node.column)
        #print linknode
        results = []
        for key in linknode.neighbors.keys():
            if linknode.neighbors[key] is not None:
                thisnode = self.getNode(linknode.neighbors[key].row, linknode.neighbors[key].column)
                if not thisnode.visited:
                    results.append(thisnode)
        return results

    def getVisitedNeighbors(self, node):
        '''Similar to the method above, except we return all of the visited neighbors'''
        linknode = self.getNodeFromLink(node.row, node.column)
        results = []
        for key in linknode.neighbors.keys():
            if linknode.neighbors[key] is not None:
                thisnode = self.getNode(linknode.neighbors[key].row, linknode.neighbors[key].column)
                if thisnode.visited:
                    results.append(thisnode)
        return results        

    def getDirectionFromNodes(self, node1, node2):
        '''What direction is node2 from node1?'''
        pos = node2.position - node1.position
        dirvec = pos.norm()
        if dirvec.x == 0:
            if dirvec.y == 1:
                return 'DOWN'
            elif dirvec.y == -1:
                return 'UP'
        else:
            if dirvec.y == 0:
                if dirvec.x == 1:
                    return 'RIGHT'
                elif dirvec.x == -1:
                    return 'LEFT'

    def deadends(self):
        '''Return the number of deadends in the nodeList'''
        num = 0
        for node in self.nodeList:
            if node.isDeadend(): num += 1

        return num

    def getUnlinkedDirections(self, node):
        '''Return the list of directions that this node is not linked to'''
        directions = []
        temp = []
        lnode = self.getNodeFromLink(node.row, node.column)
        for key in lnode.neighbors.keys():
            if lnode.neighbors[key] is not None:
                temp.append(key)
        
        for d in temp:
            if node.neighbors[d] is None:
                directions.append(d)

        return directions

    def braid(self):
        '''Removes dead ends by linking the deadends with neighbors'''
        for node in self.nodeList:
            if node.isDeadend():
                directions = self.getUnlinkedDirections(node)
                index = randint(0, len(directions)-1)
                self.addPath(node, directions[index])

    def removeRedundantNodes(self):
        '''Remove nodes that do not have any perpendicular paths'''
        newNodelist = []
        for node in self.nodeList:
            if node.redundantNode():
                print "Redundant node at " + str(node.row) + ", " + str(node.column)
                keys = node.getNeighborKeys()
                node.neighbors[keys[0]].neighbors[keys[1]] = node.neighbors[keys[1]]
                node.neighbors[keys[1]].neighbors[keys[0]] = node.neighbors[keys[0]]
            else:
                newNodelist.append(node)
            self.nodeList = newNodelist

    def render(self, screen):
        for node in self.nodeList:
            node.render(screen)

        
