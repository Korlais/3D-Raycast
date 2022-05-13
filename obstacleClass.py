import __main__ as main
import math, random, pygame

class Obstacle:
	def __init__(self, x, y, winScale, other):
	
		self.x = main.centerPos(x=x)
		self.y = main.centerPos(y=y)
		self.w = winScale
		self.other = other
		
		self.color = (255, 255, 255)

		self.rect = pygame.Rect(self.x, self.y, self.w, self.w)
		self.distToPlayer = math.sqrt( abs(self.other.rect.centerx - self.rect.centerx)**2 + abs(self.other.rect.centery - self.rect.centery) )
		
	def update(self):
		self.distToPlayer = math.sqrt( abs(self.other.rect.centerx - self.rect.centerx)**2 + abs(self.other.rect.centery - self.rect.centery) )
		
	def draw(self, wind):
		self.update()
		pygame.draw.rect(wind, self.color, self.rect)
		#sliverSurf = pygame.Surface((self.w, self.w), pygame.SRCALPHA)
		#sliverSurf.fill((255, 255, 255, 255))
		#main.surf2D.blit(sliverSurf, (self.x, self.y))
		
	def getDist(self):
		return self.distToPlayer