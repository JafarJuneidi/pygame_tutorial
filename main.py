from utilities import Player, Projectile, pygame, Enemy
pygame.init()

screenWidth = 500
screenHeight = 480
win = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Jafar's Game")

# colors
RED = (255,0,0)
BLACK = (0,0,0)

# fonts
FONT = pygame.font.SysFont("gabriola", 30, True)

# load images
bg = pygame.image.load("images/bg.jpg")

# load sound
bulletSound = pygame.mixer.Sound("sound/bullet.wav")
hitSound = pygame.mixer.Sound("sound/hit.wav")
music = pygame.mixer.music.load("sound/slayerGates.mp3")
pygame.mixer.music.play(-1)

# game variables
clock = pygame.time.Clock()

def redrawGameWindow():
	win.blit(bg, (0,0))
	text = FONT.render(f"Score = {score}", 1, BLACK)
	win.blit(text, (360, 10))
	man.draw(win)
	goblin.draw(win)
	for bullet in bullets:
		bullet.draw(win)
	pygame.display.update()

# game loop
man = Player(10, 410, 64, 64)
goblin = Enemy(100, 410, 64, 64, 450)
shootLoop = 0
bullets = []
score = 0
run = True
while run:
	clock.tick(27)
	if goblin.visible:
		if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
			if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
				man.hit(win, screenWidth, screenHeight)
				score -= 10

	if shootLoop > 0:
		shootLoop += 1
	if shootLoop > 3:
		shootLoop = 0

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	for bullet in bullets:
		if goblin.visible:
			if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
				if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
					hitSound.play()
					goblin.hit()
					score += 1
					bullets.pop(bullets.index(bullet))

		if bullet.x < 500 and bullet.x > 0:
			bullet.x += bullet.vel
		else:
			bullets.pop(bullets.index(bullet))


	keys = pygame.key.get_pressed()
	if keys[pygame.K_ESCAPE]:
		run = False


	if keys[pygame.K_SPACE] and shootLoop == 0:
		bulletSound.play()
		if man.left:
			facing = -1
		else:
			facing = 1
		if len(bullets) < 5:
			bullets.append(Projectile(round(man.x + man.width//2), round(man.y + man.height//2), 6, RED, facing))
		shootLoop = 1

	if keys[pygame.K_LEFT] and man.x > man.vel:
		man.x -= man.vel
		man.left = True
		man.right = False
		man.standing = False
	elif keys[pygame.K_RIGHT] and man.x < screenWidth - man.width - man.vel:
		man.x += man.vel
		man.right = True
		man.left = False
		man.standing = False
	else:
		man.standing = True
		man.walkCount = 0

	if not man.isJump:
		if keys[pygame.K_UP]:
			man.isJump = True
			man.right, man.left = False, False
			man.walkCount = 0
	else:
		if man.jumpCount >= -10:
			neg = 1
			if man.jumpCount < 0:
				neg = -1
			man.y -= (man.jumpCount**2) * 0.5 * neg
			man.jumpCount -= 1
		else:
			man.isJump = False
			man.jumpCount = 10

	redrawGameWindow()
	
pygame.quit()