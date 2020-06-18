
# import modules
import pygame, sys
from pygame.locals import *
import random, time
 
# initializing 
pygame.init()
 
# setting up FPS
FPS = 60
FramePerSec = pygame.time.Clock()
 
# creating colors
RED   = (245, 46, 46)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# other variables for use in the program
DISPLAY_WIDTH = 600
DISPLAY_HEIGHT = 500 
SPEED = 5
SCORE = 0

# setting up fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over" , True, BLACK)

background = pygame.image.load("AgainstTraffic/road.png")
background = pygame.transform.scale(background, (DISPLAY_WIDTH,DISPLAY_HEIGHT))
 
# create a white screen 
DISPLAYSURF = pygame.display.set_mode((DISPLAY_WIDTH,DISPLAY_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Me against Traffic!")
 

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
    	super().__init__() 
    	image = pygame.image.load("AgainstTraffic/car.png")
    	self.image = pygame.transform.scale(image, (70, 50))
    	self.surf = pygame.Surface((70, 50))
    	self.rect = self.surf.get_rect(center = (random.randint(40, DISPLAY_WIDTH-40)
                                               ,0))
        
    def move(self):
    	global SCORE
    	self.rect.move_ip(0,SPEED)
    	if (self.rect.bottom > 600):
    		SCORE += 1
    		self.rect.top = 0
    		self.rect.center = (random.randint(40, DISPLAY_WIDTH-40), 0)
    
 
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        image = pygame.image.load("AgainstTraffic/person.png")
        self.image = pygame.transform.scale(image, (90, 80))
        self.surf = pygame.Surface((90, 80))
        self.rect = self.surf.get_rect(center = (150,455))
    
    def move(self):
        pressed_keys = pygame.key.get_pressed()

        if self.rect.left > 30:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-6, 0)

        if self.rect.right < (DISPLAY_WIDTH-35):        
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(6, 0)


def gameover_screen():
    while True:
         for event in pygame.event.get():
        
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
	

         DISPLAYSURF.fill(RED)
         DISPLAYSURF.blit(game_over, (180, 200))
         DISPLAYSURF.blit(message, (160, 240))

         pygame.display.update()

         for entity in all_sprites:
            entity.kill()

         time.sleep(2)

         pygame.display.update()
         FramePerSec.tick(FPS)


# setting up sprites         
P1 = Player()
E1 = Enemy()

# creating sprites group
enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)

# adding a new user event
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# define sound effect and music
bg_sound = pygame.mixer.Sound('AgainstTraffic/background.wav')
crash = pygame.mixer.Sound('AgainstTraffic/crash.wav')

bg_sound.play()

# game loop 
while True:     
	# cycles through all events occuring
    for event in pygame.event.get():   
    	if ((event.type == INC_SPEED) and (SPEED < 12)):
    		SPEED += 0.5      
    	if event.type == QUIT:
            pygame.quit()
            sys.exit() 

    DISPLAYSURF.blit(background, (0,0))
    scores = font_small.render(str(SCORE), True, BLACK)    
    DISPLAYSURF.blit(scores, (10,10))

    # move and re-draws all sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

	# to be run if collision occurs between Player and Enemy
    if pygame.sprite.spritecollideany(P1, enemies):

        message = font.render("Your Score: " + str(SCORE) , True, BLACK)

        crash.play()

        time.sleep(1)

        bg_sound.stop()

        gameover_screen()
    	
    pygame.display.update()
    FramePerSec.tick(FPS)
    




