#   this is a simple pygame script to help visualize a given network structure
#   simply for demo purposes, does not actually contribute to the model


import pygame
import sys
import random

print('\n\n\n')

#get user inputs to define the structure of the network
structure = input("please enter the structre of your network with just\nthe sizes and spaces between (ex. '1 3 5 2'): ")
structure = structure.split(' ')
for i in range(len(structure)):
    structure[i] = int(structure[i])


screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)


#   various used constants    
info = pygame.display.Info()
width, height = info.current_w, info.current_h
WINDOW_SIZE = (width, height)#   will automatically make pygame detect screen size
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

NODE_COLOR = RED
EDGE_COLOR = BLUE



def shift_color(color, max_change=10):
    return tuple(
        max(0, min(255, c + random.randint(-max_change, max_change)))
        for c in color
    )



#   function to draw full network given 'networkCoords'
def drawNetwork(networkCoords, nodeRadius, color):
    
    
    for layer in networkCoords:
        for node in layer:
            #color = shift_color(color, max_change=50)
            pygame.draw.circle(screen, color, node, nodeRadius)
            
            
            
#   draw edges between nodes
def drawEdges(networkCoords, edgeThickness, color):
    
    
    for layerInd in range(len(networkCoords) - 1):
        for nodeInd in range(structure[layerInd]):
            #   captured one start node, now draw lines from this node to each of the
            #   next layer nodes
            for nextNodeInd in range(structure[layerInd + 1]):
                #color = shift_color(color, max_change=50)
                pygame.draw.line(screen, color, networkCoords[layerInd][nodeInd], networkCoords[layerInd + 1][nextNodeInd], edgeThickness)



    
    
    
#   initialize pygame screen and clock
pygame.init()
clock = pygame.time.Clock()


#   calculate node radii based on WINDOW_SIZE and the user give structure
possibleWidth = WINDOW_SIZE[0]/len(structure)/3
possibleHeight = WINDOW_SIZE[1]/max(structure)/3



#   depending on which measurement is the limiting size, assign node radius
nodeRadius = min(possibleWidth, possibleHeight) / 3



#   how much of the screen one layer takes up
layerWidth = WINDOW_SIZE[0]/(len(structure))



#   thickness of edges in number of pixels
edgeThickness = 1



#   fill an array with points of the nodes
networkCoords = []
for layerInd in range(len(structure)):
    appendLayer = []
    for nodeInd in range(structure[layerInd]):
        x = layerInd * layerWidth + (layerWidth / 2)
        y = (WINDOW_SIZE[1] / (structure[layerInd] + 1)) * (nodeInd + 1)
        appendLayer.append((x, y))
    networkCoords.append(appendLayer)



#   main loop
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            pygame.quit()
            sys.exit()
            
    #   put drawings here
        
    screen.fill(WHITE)
    
    NODE_COLOR = shift_color(NODE_COLOR, max_change = 5)
    EDGE_COLOR = shift_color(EDGE_COLOR, max_change = 5)
    
    drawEdges(networkCoords, edgeThickness, NODE_COLOR)
    drawNetwork(networkCoords, nodeRadius, EDGE_COLOR)
    
    clock.tick(120)
    pygame.display.flip()