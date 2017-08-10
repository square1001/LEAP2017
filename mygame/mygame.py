import pygame
import random
from os import path


WIDTH = 480 #WIDTH of the game window
HEIGHT = 600 #HEIGHT of the game window
FPS = 30 #FPS: Frames per Second

#Colors rgb

BLACK = ( 0, 0, 0 )
WHITE = ( 255, 255, 255 )
RED = ( 255, 0, 0 )
GREEN = ( 0, 255, 0 )
BLUE = ( 0, 0, 255 )

pygame.init()
pygame.mixer.init() #Initialize sound
screen = pygame.display.set_mode((WIDTH, HEIGHT)) #Create screen
pygame.display.set_caption("Game") #Give game a title
clock = pygame.time.Clock() #Keep clock of speed/time

img_dir = path.join(path.dirname(__file__), "PNG")
player_img = pygame.image.load(path.join(img_dir, "ufoRed.png")).convert()
mob_img = pygame.image.load(path.join(img_dir, "Meteors/meteorGrey_med1.png")).convert()
bullet_img = pygame.image.load(path.join(img_dir, "Lasers/laserBlue01.png")).convert()

font_name = pygame.font.match_font("cursive")

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (30, 30))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 16 * 15)
        self.speedx = 0
    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
        self.rect.x += self.speedx
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        bullets.add(bullet)
        all_sprites.add(bullet)

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(mob_img, (20, 20))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-500, -40)
        self.speedy = random.randrange(8, 16)
        self.speedx = random.randrange(-3, 4)
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top >= HEIGHT or self.rect.right < 0 or self.rect.left >= WIDTH:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-120, -40)
            self.speedy = random.randrange(8, 16)
            self.speedx = random.randrange(-3, 4)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet_img, (3, 12))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -20
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

#Initialize and create game window

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
numbermobs = 32
for i in range(numbermobs):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

score = 0

#Game Loop

running = True
while running:
    clock.tick(FPS)
    #Process Inputs (events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    #Updates
    all_sprites.update()
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    while len(mobs) < numbermobs:
        m = Mob()
        mobs.add(m)
        all_sprites.add(m)
        score += 1
    hits = pygame.sprite.spritecollide(player, mobs, False)
    if hits:
        running = False
    #Renders (draws)
    screen.fill(BLACK)
    all_sprites.draw(screen)
    draw_text(screen, "SCORE: " + str(score), 20, WIDTH / 2, 10)
    #After drawing everything, flip the drawing
    pygame.display.flip()

print("SCORE: ", score)
pygame.quit()
