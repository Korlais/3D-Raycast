import __main__ as main
from obstacleClass import Obstacle
import math, random, pygame, pygame.math

class Player:
	def __init__(self, x, y, speed, dir, turnSpeed=0.05):

		self.x = main.centerPos(x=x)
		self.y = main.centerPos(y=y)
		self.speed = speed
		self.dir = dir
		self.turnSpeed = turnSpeed
		self.color = (0, 255, 0)
		self.r = main.surf2D.get_width()//(main.GRIDSIZE*1.5)

		self.rect = pygame.Rect(self.x, self.y, 2*self.r, 2*self.r) ; 	self.rect.x, self.rect.y = self.rect.center
		self.angleX= self.x + math.sin(self.dir) * self.speed*10 ;	self.angleY= self.y + math.cos(self.dir) * self.speed*10
		
		self.ray = self.Ray(self, self.dir, 0)
		
	def update(self):
		self.rect = pygame.Rect(self.x, self.y, 2*self.r, 2*self.r)
		self.angleX= self.x + math.sin(self.dir) * self.speed
		self.angleY= self.y + math.cos(self.dir) * self.speed	
		
	def draw(self, wind):
		self.update()
		#pygame.draw.circle(wind, self.color, (self.x, self.y), self.r)
		#pygame.draw.line(wind, (255, 0, 0), (self.x, self.y), (self.x + math.sin(self.dir) * 20, self.y + math.cos(self.dir) * 20), int(self.r/2))
		thisRect = pygame.Rect((self.x, self.y, 2*self.r, 2*self.r));	thisRect.center = thisRect.x, thisRect.y
		pygame.draw.rect(wind, (255,0,0), thisRect)


	def move(self):
		self.update()
		nx = self.angleX - self.x ; 	ny = self.angleY - self.y
		
		keys = pygame.key.get_pressed()
		if (keys[pygame.K_LEFT] or keys[pygame.K_a]): 	self.dir += self.turnSpeed
		if (keys[pygame.K_RIGHT] or keys[pygame.K_d]): 	self.dir -= self.turnSpeed
		if (keys[pygame.K_UP] or keys[pygame.K_w]): 		self.x += nx;	self.y += ny
		if (keys[pygame.K_DOWN] or keys[pygame.K_s]): 	self.x -= nx;	self.y -= ny

	class Ray:
		def __init__(self, player, angle, length):
			self.player = player
			
			self.x1 = self.player.x
			self.y1 = self.player.y
			self.angle = angle
			self.length = length

			self.x2 = (self.x1 + math.sin(self.player.dir + self.angle) * self.length)
			self.y2 = (self.y1 + math.cos(self.player.dir + self.angle) * self.length)
			self.endPos = (self.x2, self.y2)

			self.distToPlayer = math.sqrt( ((self.x2 - self.x1)**2) + ((self.y2 - self.y1)**2) )
			self.distToWall = self.distToPlayer * (sorted([0.99, abs(math.cos(player.dir)), 1])[1])

			self.hitWall = False
			self.color = (20, 150, 255)
			
		def update(self):
			self.x1 = self.player.x
			self.y1 = self.player.y
			self.distToPlayer = math.sqrt( ((self.x2 - self.x1)**2) + ((self.y2 - self.y1)**2) )


		def draw(self, wind):
			self.update()

			pygame.draw.line(wind, self.color, (self.x1, self.y1), self.endPos, 1)
			pygame.draw.circle(wind, (0, 255, 0), self.endPos, 2)
			
			
		def hits(self, other):
			self.update()
			collision = other.rect.clipline((self.x1, self.y1), (self.x2, self.y2))
			return collision

