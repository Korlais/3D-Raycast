import pygame, math, random, sys, datetime;	pygame.init();	pygame.font.init()
from playerClass import Player;		from textMapGen import mapGen
import obstacleClass as obClass;	from obstacleClass import Obstacle
def centerPos(x=None, y=None, r=1):
	#returns (x, y) translated to be relative to (cX, cy) rather than pygame's (0, 0)
	cX, cY = WIDTH/2, HEIGHT/2
	
	if (y == None):		return x + (cX*r)
	elif (x == None): 	return y + (cY*r)
	else: 				return x + (cX*r), y + (cY*r)



#Initialization
WIDTH, HEIGHT, GRIDSIZE, FPS = 1000, 1000, 50, 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Luca's 3D Maze")

surf2D = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)		#Renders the 2D scene
surf3D = pygame.Surface((WIDTH, HEIGHT))						#Renders the 3D scene
surfGUI = pygame.Surface((WIDTH/2, 75), pygame.SRCALPHA)

clock = pygame.time.Clock()
font = pygame.font.Font("C:\Windows\Fonts\IMPACT.TTF", 33)



#Variable Initialization	-------------------------------------------------------------------------------------------------
player = Player(0, 0, 10, 0, turnSpeed=0.12)
walls = [];		rays = [];		raysHit = []


ceiling = pygame.image.load("Assets\\ceiling.png")
floor = pygame.image.load("Assets\\floor.png")
wall = pygame.image.load("Assets\\wall.png")
mapFile = "Assets\\map.txt"

FOV = 1;	numRays = 100
FOVchange = FOV/numRays
resolution = WIDTH/numRays + 1
#----------------------------------------------------------------------------------------------------------------------------
#Creates and displays a randomly generated map via mapGenerator.py	---------------------------------------------------------
mapGen(mapFile, int(WIDTH/GRIDSIZE), 20)
def makeMap():
	walls.clear()
	posX, posY = centerPos(x=0, r=-1), centerPos(y=0, r=-1)
	theMap = open(mapFile)

	for line in theMap:
		for char in range(len(line)): #checks every character in each line
			
			if line[char] == "X":	# X's generate walls
				obst = Obstacle(posX, posY, GRIDSIZE+2, player)
				walls.append(obst)
				
			posX += GRIDSIZE
		posX = centerPos(x=0, r=-1)
		posY += GRIDSIZE
makeMap()
#----------------------------------------------------------------------------------------------------------------------------

def main():
	while (True):
		global FOV, numRays, FOVchange, resolution
		surf2D.fill(0);	surf3D.fill((100, 100, 160));	surfGUI.fill(0)
		
		for e in pygame.event.get():
			if (e.type == pygame.QUIT):
				pygame.quit(); sys.exit()
		
		#Ray Creation
		rays = [];	raysHit = []

		def createRays():
			angle = -numRays
			for r in range(numRays//2, -numRays//2, -1):
				ray = player.Ray(player, angle, WIDTH/1.25)
				angle -= FOVchange/FOV
				
				rays.append(ray)
		createRays()

		#Wall-Ray Collision Detection
		for wall in walls:
			for ray in rays:	
				if (len(ray.hits(wall)) > 0) and (ray.hitWall == False):

					ray.x2, ray.y2 = ray.hits(wall)[0][0], ray.hits(wall)[0][1]
					ray.endPos = ray.hits(wall)[0]
					raysHit.append(ray)

		#3D Rendering:---------------------------------------------------------------------------------------------------------------
		surf3D.blit(ceiling, (0, 0))	#sky
		surf3D.blit(floor, (0, surf3D.get_height()/2))	#floor
		
		for ray in raysHit:
			global wallColor

			#Generate position and size for each sliver of the screen a ray generates
			xPos = rays.index(ray)*resolution
			yPos = surf3D.get_height()/2
			renderHeight = 100 *  ray.distToWall/(ray.distToPlayer+0.01) 	#player's dist to each wall sliver
			theRect = pygame.Rect(xPos, yPos, resolution, renderHeight)
			theRect.center = theRect.x, theRect.y	

			#Colors
			alph = sorted([0, renderHeight/3, 255])[1]	#limits alpha range between 0 and 255
			wallColor = (80, 80, 135, alph)	
			fogColor = (0, 0, 0)		

			if (ray.distToPlayer < 1):	#red if player inside wall
				pygame.draw.rect(surf3D, (200, 50, 50), theRect)

			else:
				pygame.draw.rect(surf3D, fogColor, theRect)	
				sliverSurf = pygame.Surface((resolution, renderHeight), pygame.SRCALPHA)
				sliverSurf.fill(wallColor)
				surf3D.blit(sliverSurf, (xPos - sliverSurf.get_width() // 2, yPos - sliverSurf.get_height() // 2))
		
		pygame.draw.circle(surf3D, (255,255,255), (surf3D.get_width()/2, surf3D.get_height()/2), 2)		#cursor
		#----------------------------------------------------------------------------------------------------------------------------

		#2D Rendering
		#for ray in rays:
		#	ray.draw(surf2D)
		for wall in walls:
			wall.draw(surf2D)	
		player.draw(surf2D)

		#GUI Rendering
		text = font.render(f"Make it to the end of the maze!", True, (255, 255, 255))
		surfGUI.blit(text, text.get_rect())

		
		#Window Updates
		player.move()
		pygame.display.flip()

		screen.blit(surf3D, (0, 0))
		screen.blit(pygame.transform.scale(surf2D, (200, 200)), (0,0))
		screen.blit(surfGUI, ((WIDTH/2) - (surfGUI.get_width()/2), 15))

		clock.tick(FPS)

if (__name__ == "__main__"):
	main()



