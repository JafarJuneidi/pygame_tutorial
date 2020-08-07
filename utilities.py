import pygame

class Player(object):
	walkRight, walkLeft = [], []
	char = pygame.image.load("images/standing.png")
	for i in range(1, 10):
		walkLeft.append(pygame.image.load(f"images/L{i}.png"))
		walkRight.append(pygame.image.load(f"images/R{i}.png"))
	def __init__(self, x, y, width, height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.vel = 5
		self.isJump = False
		self.jumpCount = 10
		self.left = False
		self.right = False
		self.walkCount = 0
		self.standing = True
		self.hitbox = (self.x + 17, self.y + 11, 29, 52)

	def draw(self, win):
		if self.walkCount + 1 >= 27: # 9 sprites, each for 3 frames
			self.walkCount = 0

		if not self.standing:
			if self.left:
				win.blit(self.walkLeft[self.walkCount//3], (self.x, self.y))
				self.walkCount += 1
			elif self.right:
				win.blit(self.walkRight[self.walkCount//3], (self.x, self.y))
				self.walkCount += 1
		else:
			if self.left:
				win.blit(self.walkLeft[0], (self.x, self.y))
			else:
				win.blit(self.walkRight[0], (self.x, self.y))
		self.hitbox = (self.x + 17, self.y + 11, 29, 52)
		# pygame.draw.rect(win, (255,0,0), self.hitbox, 2)

	def hit(self, win, screenW, screenH):
		self.isJump = False
		self.jumpCount = 10
		self.x = 60
		self.y = 410
		self.walkCount = 0
		FONT1 = pygame.font.SysFont("magnito", 100)
		text = FONT1.render("-10", 1, (255,0,0))
		win.blit(text, (screenW//2 - text.get_width()//2, 200))
		pygame.display.update()

		for i in range(50):
			pygame.time.delay(10)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					# i = 301
					pygame.quit()


class Projectile(object):
	def __init__(self, x, y, radius, color, facing):
		self.x = x
		self.y = y
		self.radius = radius
		self.color = color
		self.facing = facing
		self.vel = 8 * facing 

	def draw(self, win):
		pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


class Enemy(object):
	walkRight, walkLeft = [], []
	for i in range(1, 12):
		walkRight.append(pygame.image.load(f"images/R{i}E.png"))
		walkLeft.append(pygame.image.load(f"images/L{i}E.png"))

	def __init__(self, x, y, width, height, end):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.end = end
		self.path = [self.x, self.end]
		self.walkCount = 0
		self.vel = 3
		self.hitbox = (self.x + 17, self.y + 2, 31, 57)
		self.health = 50
		self.visible = True

	def draw(self, win):
		self.move()
		if self.visible:
			if self.walkCount + 1 >= 33:
				self.walkCount = 0

			if self.vel > 0:
				win.blit(self.walkRight[self.walkCount//3], (self.x, self.y))
				self.walkCount += 1
			else:
				win.blit(self.walkLeft[self.walkCount//3], (self.x, self.y))
				self.walkCount += 1

			pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
			pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 20, self.health, 10))
			# above width 50 - (5 * (10 - self.health)) and health was 10
			self.hitbox = (self.x + 17, self.y + 2, 31, 57)
			# pygame.draw.rect(win, (255,0,0), self.hitbox, 2)

	def move(self):
		if self.vel > 0:
			if self.x  + self.vel < self.path[1]:
				self.x += self.vel
			else:
				self.vel *= -1
				self.walkCount = 0
		else:
			if self.x + self.vel > self.path[0]:
				self.x += self.vel
			else:
				self.vel *= -1
				self.walkCount = 0
	
	def hit(self):
		if self.health > 0:
			self.health -= 1
		else:
			self.visible = False
		print("hit")