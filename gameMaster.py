import pygame, random, sys
from pygame.locals import *
import pygame.mixer
import requests
import math

#set: window size, colours, background, scores and speeds
WINDOWWIDTH = 1024
WINDOWHEIGHT = 683
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BACKGROUND = pygame.image.load('amazon.jpg')
BACKGROUND1 = pygame.image.load('borneo.jpg')
topscore1 = 50
topscore2 = 100
goodieSpeed = 5
baddieSpeed = 14

#api variables
## You will need to create your own API keys on openweathermap in order to
## incorporate the api code later in the script
base_urltwo = 'http://api.openweathermap.org/data/2.5/weather'
api_keytwo = '4ddb6af3300cba0df450a275f3622e1f'  
citytwo = ['Samarinda']

#-------------------classes for game objects-----------------------------------

#class to set up player and move monkey around
class Player(pygame.sprite.Sprite):

    def __init__(self):
        super(Player, self).__init__()

        self.image = pygame.Surface([WINDOWWIDTH, WINDOWHEIGHT])

        self.rect = self.image.get_rect()

    def update(self):
        pos = pygame.mouse.get_pos()

        self.rect.x = pos[0]
        self.rect.y = 500

    def set_image(self, filename = None):
        if (filename != None):
            self.image = pygame.image.load(filename)
            self.rect = self.image.get_rect()

#class to set up falling bananas at random intervals
class Banana(pygame.sprite.Sprite):
    image = None

    def __init__(self):
        super(Banana, self).__init__()

        self.image = pygame.Surface([30, 40])
        self.rect = self.image.get_rect()
        
        if Banana.image is None:
            Banana.image = pygame.image.load('banana.png')
        self.image = Banana.image

    def update(self):
        self.rect.y += goodieSpeed

#for second level
class Banana2(pygame.sprite.Sprite):
    image = None

    def __init__(self):
        super(Banana, self).__init__()

        self.image = pygame.Surface([30, 40])
        self.rect = self.image.get_rect()

        if Banana.image is None:
            Banana.image = pygame.image.load('banana.png')
        self.image = Banana.image

    def update(self):
        self.rect.y += 10

#class to set up falling capuacu and speed
class Capuacu(pygame.sprite.Sprite):
    image = None
    def __init__(self):
        super(Capuacu, self).__init__()

        self.image = pygame.Surface([30, 40])
        self.rect = self.image.get_rect()
        
        if Capuacu.image is None:
            Capuacu.image = pygame.image.load('nut.png')
        self.image = Capuacu.image

    def update(self):
        self.rect.y += baddieSpeed

#class to set up falling watermelon and speed
class Watermelon(pygame.sprite.Sprite):
    image = None
    def __init__(self):
        super(Watermelon, self).__init__()

        self.image = pygame.Surface([30, 40])
        self.rect = self.image.get_rect()

        if Watermelon.image is None:
            Watermelon.image = pygame.image.load('Watermelon.png')
        self.image = Watermelon.image

    def update(self):
        self.rect.y += 22
        
#-------------------------------------------------------------------------------

#api code to access temperature and humidity of jungle        
def get_temperaturetwo(citytwo):
  query = base_urltwo + '?q=%s&units=metric&APPID=%s' % (citytwo, api_keytwo)
  try:
    response = requests.get(query)
    if response.status_code != 200:
      response = 'N/A'
      return response
    else:
      weather_data = response.json()
      return weather_data
  except requests.exceptions.RequestException as error:
    print error

#functions to draw white or black text
def drawTextWhite(text, font, surface, x, y):
   textobj = font.render(text, 1, WHITE)
   textrect = textobj.get_rect()
   textrect.topleft = (x, y)
   surface.blit(textobj, textrect)

def drawTextBlack(text, font, surface, x, y):
   textobj = font.render(text, 1, BLACK)
   textrect = textobj.get_rect()
   textrect.topleft = (x, y)
   surface.blit(textobj, textrect)

#function for score text  
def texts(score):
    font = pygame.font.Font(None, 60)
    scoretext = font.render("Score:" + str(score), 1, WHITE)
    gameDisplay.blit(scoretext, (10, 10))

#initiate mixer before initiating game
pygame.mixer.pre_init(44100, -16, 2, 2048)

#-------------------------------------GAME--------------------------------------

pygame.init()

#sounds and game display
bananaSound = pygame.mixer.Sound('splat.wav')
baddieSound = pygame.mixer.Sound('ouch.wav')
borneoSound = pygame.mixer.Sound('borneo.wav')
gameDisplay = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

#sprite lists
all_sprites_list = pygame.sprite.Group()
banana_list = pygame.sprite.Group()
watermelon_list = pygame.sprite.Group()
capuacu_list = pygame.sprite.Group()

clock = pygame.time.Clock()
pygame.display.set_caption("Monkey Madness")
player = Player()
all_sprites_list.add(player)
player.set_image('monkeyhead.png')
score = 0
       

#main game for level 1              
def game(jungle):
    score = 0
    jungle = True
    while jungle:

        new_list = pygame.sprite.Group()
        new_list.add(player)
        gameDisplay.blit(BACKGROUND, (0,0))
        seconds = int(pygame.time.get_ticks())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                jungle = False

        if seconds % 20 == 0:
            banana = Banana()

            banana.rect.x = random.randrange(650)
            banana.rect.y = 0

            all_sprites_list.add(banana)
            banana_list.add(banana)

        if seconds % 80 == 0:
            capuacu = Capuacu()

            capuacu.rect.x = random.randrange(650)
            capuacu.rect.y = 0

            all_sprites_list.add(capuacu)
            capuacu_list.add(capuacu)

        if score == topscore1:
            newLevel(jungle)


        all_sprites_list.update()
        all_sprites_list.draw(gameDisplay)

        for banana in banana_list:
            if pygame.sprite.spritecollide(banana, new_list, True):
                bananaSound.play()
                banana_list.remove(banana)
                all_sprites_list.remove(banana)
                all_sprites_list.add(player)
                score += 1

        for capuacu in capuacu_list:
            if pygame.sprite.spritecollide(capuacu, new_list, True):
                baddieSound.play()
                capuacu_list.remove(capuacu)
                all_sprites_list.remove(capuacu)
                all_sprites_list.add(player)
                score -= 1
        
        texts(score)
        pygame.display.flip()

    clock.tick(100)

#font settings
font = pygame.font.Font('GoodDog.otf', 65)
factfont = pygame.font.Font('GoodDog.otf',55)
apifont= pygame.font.Font('GoodDog.otf',40)
titlefont= pygame.font.Font('GoodDog.otf',70)
        
#creates second level of game with borneo specific settings
def newLevel(jungle):
    jungle = True
    
    while jungle:
        borneoSound.play()
        seconds = int(pygame.time.get_ticks())
        gameDisplay.blit(BACKGROUND1, (0,0))
        
        #location = get_temperaturetwo(citytwo) ##api code 
        drawTextWhite('Welcome to the Borneo rainforest...',titlefont, gameDisplay, 150, 50)
        drawTextWhite('Catch 100 bananas! Avoid watermelons!', apifont, gameDisplay, 250, 115)
        #drawTextWhite('The temperature is currently:' + ' ' + str(math.ceil(location['main']['temp'])) + ' C ',apifont, gameDisplay, 250, 115) ##api code
        #drawTextWhite('The humidity is:' + ' ' + str(math.ceil(location['main']['humidity'])) + '%  ',apifont, gameDisplay, 350, 150) ##api code
        drawTextWhite("Did you know....", factfont, gameDisplay, 20, 200)
        drawTextWhite("* Borneo rainforest is one of the oldest in the world... ", factfont, gameDisplay, 20, 250)
        drawTextWhite("  and is estimated to be about 130 million years old!", factfont, gameDisplay, 20, 290)
        drawTextWhite("* Orangutans can only be found... ", factfont, gameDisplay, 20, 330)
        drawTextWhite("  in the rainforests of Borneo and Sumatra! ", factfont, gameDisplay, 20, 370)
        drawTextWhite("* Borneo is twice the size of Germany ", factfont, gameDisplay, 20, 410)
        drawTextWhite("LEVEL 2: THE BORNEO RAINFOREST", font, gameDisplay, 300, 600)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                jungle = False

            if seconds % 20 == 0:
                borneoSound.stop()
                game2(jungle)

        pygame.display.update()
        
#end screen for winners    
def youWon(jungle):
    jungle = True
    while jungle:
        BACKGROUND = pygame.image.load('hooray.jpg')
        gameDisplay.blit(BACKGROUND, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                jungle = False
                
        pygame.display.update()

#main game for level 2               
def game2(jungle):
    score = 0
    jungle = True
    while jungle:
        new_list = pygame.sprite.Group()
        new_list.add(player)
        gameDisplay.blit(BACKGROUND1, (0,0))
        seconds = int(pygame.time.get_ticks())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                jungle = False

        if seconds % 30 == 0:
            banana = Banana()

            banana.rect.x = random.randrange(650)
            banana.rect.y = 0

            all_sprites_list.add(banana)
            banana_list.add(banana)

        if seconds % 40 == 0:
            watermelon = Watermelon()

            watermelon.rect.x = random.randrange(650)
            watermelon.rect.y = 0

            all_sprites_list.add(watermelon)
            watermelon_list.add(watermelon)

        if score == topscore2:
            youWon(jungle)


        all_sprites_list.update()
        all_sprites_list.draw(gameDisplay)

        for banana in banana_list:
            if pygame.sprite.spritecollide(banana, new_list, True):
                bananaSound.play()
                banana_list.remove(banana)
                all_sprites_list.remove(banana)
                all_sprites_list.add(player)
                score += 1

        for watermelon in watermelon_list:
            if pygame.sprite.spritecollide(watermelon, new_list, True):
                baddieSound.play()
                watermelon_list.remove(watermelon)
                all_sprites_list.remove(watermelon)
                all_sprites_list.add(player)
                score -= 1
        
        texts(score)
        pygame.display.flip()

    clock.tick(100)


#---------following commented out since using main.py as main script--------------------
    
#def main():
 #   jungle = True
 #   gameCHANGER.weather(jungle)
 #   game(jungle)

 #   pygame.quit
 #   exit()

#main()
        
        






        
    
     
              
