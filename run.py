import pygame
from pygame.locals import *
#from constants import *
from nodes import NodeGroup
import binaryTree
import sidewinder
import aldous_broder
import wilson
import huntkill
import backtracker

class GameController(object):
    def __init__(self):
        pygame.init()
        dx, dy = 25, 25
        rows, columns = 20, 20
        self.nodes = NodeGroup(dx, dy, rows, columns, dx, dy)
        self.nodes.usePacmanTemplate()
        rows, columns = self.nodes.rows, self.nodes.columns
        #print len(self.nodes.nodeList)
        #print "+++++++++++++++++"
        #huntkill.generateMaze(self.nodes)
        backtracker.generateMaze(self.nodes)
        #wilson.generateMaze(self.nodes)
        #aldous_broder.generateMaze(self.nodes)
        #binaryTree.generateMaze(self.nodes.nodeList)
        #sidewinder.generateMaze(self.nodes.nodeList)
        #print "DEADENDS = " + str(self.nodes.deadends())
        
        self.nodes.braid()
        #self.nodes.removeRedundantNodes()
        

        SCREENSIZE = (dx * (columns+1), dy * (rows+1))
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.setBackGround(SCREENSIZE)
        
    def setBackGround(self, screensize):
        self.background = pygame.surface.Surface(screensize).convert()
        self.background.fill((0,0,0))

    def update(self):
        self.checkEvents()
        self.render()

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.nodes.render(self.screen)
        pygame.display.update()


if __name__ == "__main__":
    game = GameController()

    while True:
        game.update()
