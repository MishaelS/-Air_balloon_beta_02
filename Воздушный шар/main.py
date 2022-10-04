try:
	from random import randrange
	import pygame, sys
except Exception as ex:
	print(f'ERROR: {ex}')

#-----------------------------------------------------------------------

class Player(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite().__init__()
		self.image = pygame.image.load('img/air balloon.png')
		self.image = pygame.transform.scale(self.image, (15*1.6, 29*1.6))
		self.rect = self.image.get_rect(center=(WIDTH/2, HEIGHT/1.2))
		self.collider_mask = pygame.Surface((20, 20))
		self.collider_rect = self.collider_mask.get_rect(center=(self.rect.centerx, self.rect.centery-7))
		self.collider_maghet_mask = pygame.Surface((120, 120))
		self.collider_maghet_rect = self.collider_maghet_mask.get_rect(center=(self.rect.centerx, self.rect.centery))

	def move(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_a] or keys[pygame.K_LEFT]:
			self.rect.centerx -= SPEEDX
		if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
			self.rect.centerx += SPEEDX
		if CHIT:
			if keys[pygame.K_w] or keys[pygame.K_UP]:
				self.rect.centery -= SPEEDY
			if keys[pygame.K_s] or keys[pygame.K_DOWN]:
				self.rect.centery += SPEEDY

		if pygame.mouse.get_pressed()[0]:
			if self.rect.right <= pygame.mouse.get_pos()[0]:
				self.rect.centerx += SPEEDX
			elif self.rect.left >= pygame.mouse.get_pos()[0]:
				self.rect.centerx -= SPEEDX

		if self.rect.left <= 0:
			self.rect.left = 0
		elif self.rect.right >= WIDTH:
			self.rect.right = WIDTH
		elif self.rect.bottom >= HEIGHT:
			self.rect.bottom = HEIGHT

		self.collider_rect.centerx = self.rect.centerx
		self.collider_rect.centery = self.rect.centery-7

		self.collider_maghet_rect.centerx = self.rect.centerx
		self.collider_maghet_rect.centery = self.rect.centery

	def update(self):
		global MAGNIT
		self.move()
		# screen.blit(self.collider_maghet_mask, self.collider_maghet_rect)
		# screen.blit(self.collider_mask, self.collider_rect)
		screen.blit(self.image, self.rect)


class Air(pygame.sprite.Sprite):
	def __init__(self, pos=(0, 0)):
		pygame.sprite.Sprite().__init__()
		self.image = pygame.image.load('img/air.png')
		self.image = pygame.transform.scale(self.image, (8*2.2, 8*2.2))
		self.rect = self.image.get_rect(center=pos)

	def move_and_conflict(self):
		global MAX_SCORE, SCORE, SPEEDX, SPEEDY
		self.rect.centery += SPEEDY
		if self.rect.top >= HEIGHT:
			self.rect.centerx = randrange(8, WIDTH-8, 8)
			self.rect.centery = randrange(-8, -HEIGHT, -8)
		if self.rect.colliderect(player.collider_maghet_rect) and MAGNIT:
			if self.rect.top >= player.collider_rect.centery:
				self.rect.centery -= SPEEDY
			if self.rect.bottom <= player.collider_rect.centery:
				self.rect.centery += SPEEDY
			if self.rect.left >= player.collider_rect.centerx:
				self.rect.centerx -= SPEEDY
			if self.rect.right <= player.collider_rect.centerx:
				self.rect.centerx += SPEEDY
		if self.rect.colliderect(player.collider_rect):
			self.rect.centerx = randrange(8, WIDTH-8, 8)
			self.rect.centery = randrange(-8, -HEIGHT, -8)
			SCORE += 1
			SPEEDX += 0.004
			SPEEDY += 0.004

	def update(self):
		self.move_and_conflict()
		screen.blit(self.image, self.rect)


class Thorns(pygame.sprite.Sprite):
	def __init__(self, pos=(0, 0)):
		pygame.sprite.Sprite().__init__()
		self.image = pygame.image.load('img/thorns.png')
		self.image = pygame.transform.scale(self.image, (16*2.5, 5*2.5))
		self.rect = self.image.get_rect(center=pos)

	def move_and_conflict(self):
		global air_list, thorns_list, SCORE, POWER, SECONDS_POWER, SECONDS_MAGHET, SPEEDY
		self.rect.centery += SPEEDY
		if self.rect.top >= HEIGHT:
			obs_x, obs_y = 20, 6
			self.rect.centerx = randrange(obs_x+10, WIDTH-obs_x,  obs_x*2)
			self.rect.centery = randrange( -HEIGHT,      -obs_y, obs_y**3)
		if not POWER:
			if self.rect.colliderect(player.collider_rect):
				SCORE = 0
				SPEEDX = 2.8
				SPEEDY = 2.6
				SECONDS_POWER = 0.0
				SECONDS_MAGHET = 0.0
				air_list = []
				thorns_list = []
				player.rect.centerx = WIDTH/2
				player.rect.centery = HEIGHT/1.2
				air_and_thorns_create(air_list, thorns_list)

	def update(self):
		self.move_and_conflict()
		screen.blit(self.image, self.rect)


class Power(pygame.sprite.Sprite):
	def __init__(self, pos=(0, 0)):
		pygame.sprite.Sprite().__init__()
		self.image = pygame.image.load('img/power.png')
		self.image = pygame.transform.scale(self.image, (11*2.2, 11*2.2))
		self.rect = self.image.get_rect(center=pos)

	def move_and_conflict(self):
		global POWER, SCORE, SECONDS_POWER, SPEEDY
		if not CHIT:
			SECONDS_POWER += 0.01
			if SECONDS_POWER > 23.0:
				if not POWER:
					self.rect.centery += SPEEDY
			if SECONDS_POWER > 4.5:
				POWER = False
		if self.rect.top >= HEIGHT:
			self.rect.centerx = randrange( 11, WIDTH-11,  11)
			self.rect.centery = randrange(-11,  -HEIGHT, -11)
			SECONDS_POWER = 0.0
		if self.rect.colliderect(player.collider_maghet_rect) and MAGNIT:
			if self.rect.top >= player.collider_rect.centery:
				self.rect.centery -= SPEEDY
			if self.rect.bottom <= player.collider_rect.centery:
				self.rect.centery += SPEEDY
			if self.rect.left >= player.collider_rect.centerx:
				self.rect.centerx -= SPEEDY
			if self.rect.right <= player.collider_rect.centerx:
				self.rect.centerx += SPEEDY
		if self.rect.colliderect(player.collider_rect):
			self.rect.centerx = randrange( 11, WIDTH-11,  11)
			self.rect.centery = randrange(-11,  -HEIGHT, -11)
			POWER = True
			SECONDS_POWER = 0.0
			SCORE += 4

	def update(self):
		self.move_and_conflict()
		screen.blit(self.image, self.rect)


class Magnet(pygame.sprite.Sprite):
	def __init__(self, pos=(0, 0)):
		pygame.sprite.Sprite().__init__()
		self.image = pygame.image.load('img/magnet.png')
		self.image = pygame.transform.scale(self.image, (9*2.2, 12*2.2))
		self.rect = self.image.get_rect(center=pos)

	def move_and_conflict(self):
		global MAGNIT, SCORE, SECONDS_MAGHET
		if not CHIT:
			SECONDS_MAGHET += 0.01
			if SECONDS_MAGHET > 18.0:
				if not MAGNIT:
					self.rect.centery += SPEEDY
			if SECONDS_MAGHET > 3.8:
				MAGNIT = False
		if self.rect.top >= HEIGHT:
			self.rect.centerx = randrange(  9, WIDTH-9,   9)
			self.rect.centery = randrange(-12, -HEIGHT, -12)
			SECONDS_MAGHET = 0.0
		elif self.rect.colliderect(player.collider_rect):
			self.rect.centerx = randrange(  9, WIDTH-9,   9)
			self.rect.centery = randrange(-12, -HEIGHT, -12)
			MAGNIT = True
			SECONDS_MAGHET = 0.0
			SCORE += 4

	def update(self):
		self.move_and_conflict()
		screen.blit(self.image, self.rect)

# -----------------------------------------------------------------------

def air_and_thorns_create(air_list, thorns_list):
	for i in range(40):
		x = randrange(8, WIDTH-8, 8)
		y = randrange(-8, -HEIGHT*2, -8)
		air_list.append(Air((x, y)))

	for i in range(18):
		obs_x, obs_y = 20, 6
		x = randrange(obs_x+10, WIDTH-obs_x,  obs_x*2)
		y = randrange( -HEIGHT,      -obs_y, obs_y**3)
		thorns_list.append(Thorns((x, y)))

def render_text():
	if CHIT:
		text_chit = font.render(f'CHIT: {CHIT}', False, (20, 20, 20))
		screen.blit(text_chit, (FONT_SIZE, FONT_SIZE*9))
		if POWER:
			text_power = font.render(f'POWER: {POWER}', False, (20, 20, 20))
			screen.blit(text_power, (FONT_SIZE, FONT_SIZE*11))

	text_seconds_power = font.render(f'SECONDS_POWER: {round(SECONDS_POWER)}', False, (20, 40, 20))
	text_seconds_magnet = font.render(f'SECONDS_MAGHET: {round(SECONDS_MAGHET)}', False, (20, 40, 20))
	text_max_score = font.render(f'MAX SCORE: {MAX_SCORE}', False, (20, 40, 20))
	text_score = font.render(f'SCORE: {SCORE}', False, (20, 40, 20))

	screen.blit(text_seconds_power, (FONT_SIZE, FONT_SIZE))
	screen.blit(text_seconds_magnet, (FONT_SIZE, FONT_SIZE*3))
	screen.blit(text_max_score, (FONT_SIZE, FONT_SIZE*5))
	screen.blit(text_score, (FONT_SIZE, FONT_SIZE*7))

def update_object():
	for air in air_list:
		air.update()
	for thorns in thorns_list:
		thorns.update()
	power.update()
	magnet.update()
	player.update()

# -----------------------------------------------------------------------

FONT_SIZE = 8
HEIGHT = 568
WIDTH = 375

MAX_SCORE = 0
SCORE = 0

SECONDS_POWER = 0.0
SECONDS_MAGHET = 0.0
SPEEDX = 2.8
SPEEDY = 2.6

CHIT = False
POWER = False
MAGNIT = False

FPS = 60

# -----------------------------------------------------------------------

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font('font/Quinquefive-0Wonv.ttf', FONT_SIZE)

# -----------------------------------------------------------------------

player = Player()
power = Power((randrange(11, WIDTH-11, 11), randrange(-11, -HEIGHT, -11)))
magnet = Magnet((randrange(9, WIDTH-9, 9), randrange(-12, -HEIGHT, -12)))

air_list = []
thorns_list = []

air_and_thorns_create(air_list, thorns_list)

# -----------------------------------------------------------------------

running = True
while running:
	screen.fill((255, 255, 255))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				running = False
			if event.key == pygame.K_p and not CHIT:
				CHIT = True
				POWER = True
			elif event.key == pygame.K_p and CHIT:
				CHIT = False
				POWER = False


	if SCORE > MAX_SCORE:
		MAX_SCORE = SCORE


	update_object()
	render_text()


	pygame.display.flip()
	clock.tick(FPS)

# -----------------------------------------------------------------------

pygame.quit()
sys.exit()
