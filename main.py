import pygame, random, sys
from pygame.locals import *

import gameMaster
import startinstruction
import math
import requests
import time

#set: width and height of surface, colours, background and start screen
WINDOWWIDTH = 1024
WINDOWHEIGHT = 683
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (30, 144, 255)
BACKGROUND= pygame.image.load('amazon.jpg')
STARTSCREEN = pygame.image.load('Monkeystartscreen.jpg')

#api variables
## You will need to create your own API keys on openweathermap in order to
## incorporate the api code later in the script
base_url = 'http://api.openweathermap.org/data/2.5/weather'
api_key = '09f18f6760ad3c443c1e854420880f41'  
city = ['Amazon']

#functions to draw black or blue text
def drawTextBlack(text, font, surface, x, y):
   textobj = font.render(text, 1, BLACK)
   textrect = textobj.get_rect()
   textrect.topleft = (x, y)
   surface.blit(textobj, textrect)

def drawTextBlue(text, font, surface, x, y):
   textobj = font.render(text, 1, BLUE)
   textrect = textobj.get_rect()
   textrect.topleft = (x, y)
   surface.blit(textobj, textrect)

##--------only in use if have API key access------------------------------------
   
#api code to access temperature and humidity of jungle 
def get_temperature(city):
  query = base_url + '?q=%s&units=metric&APPID=%s' % (city, api_key)
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
    
#--------------------------------------------------------------------------------
    
#initiate mixer for sounds before initiating game
pygame.mixer.pre_init(44100, -16, 2, 2048)

#---------------------------START SCREEN AND GAME INITIATE-----------------------
pygame.init()

rainforestSound = pygame.mixer.Sound('rainforest.wav')
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Monkey Madness')
pygame.mouse.set_visible(False)

#font settings
font = pygame.font.Font('GoodDog.otf', 38)
biggerfont = pygame.font.Font('GoodDog.otf', 70)
apifont = pygame.font.Font ('GoodDog.otf',45)
smallerfont = pygame.font.Font('GoodDog.otf', 35)
mediumfont = pygame.font.Font('GoodDog.otf', 40)
clock = pygame.time.Clock()

#information screen on amazon jungle     
def weather(jungle):
   jungle = True
   
   while jungle:
      rainforestSound.play()
      seconds = int(pygame.time.get_ticks())
      windowSurface.blit(BACKGROUND, (0,0))
 #     location = get_temperature(city)
      drawTextBlack('Welcome to the Amazon rainforest...',biggerfont, windowSurface, 150, 40)
      drawTextBlack('Catch 50 Bananas! Avoid Coconuts!', apifont, windowSurface, 250, 100)
 #     drawTextBlack('The temperature is currently:' + ' ' + str(math.ceil(location['main']['temp'])) + ' C ',apifont, windowSurface, 250, 100)
 #     drawTextBlack('The humidity is:' + ' ' + str(math.ceil(location['main']['humidity'])) + '%  ',apifont, windowSurface, 350, 140)
      drawTextBlue('Did you know.....', smallerfont, windowSurface, 20, 350)
      drawTextBlue('* The Amazon has been around for at least 55 million years!', smallerfont, windowSurface, 20, 400)
      drawTextBlue('* Due to the thickness of the canopy (the top branches and leaves of the trees),', smallerfont, windowSurface, 20, 440)
      drawTextBlue('  the Amazon floor is in permanent darkness!', smallerfont, windowSurface, 20, 470)
      drawTextBlue("*In fact, it's SO thick that when it rains,", smallerfont, windowSurface, 20, 510)
      drawTextBlue(" it takes around ten minutes for the water to reach the ground!", smallerfont, windowSurface, 20, 540)
      drawTextBlue('Slide mouse to begin game!', biggerfont, windowSurface, 210, 600)
      
      for event in pygame.event.get():
         
         if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            jungle = False
            
         if seconds % 20 == 0:
            rainforestSound.stop()
            gameMaster.game(jungle)
            
      pygame.display.update()

#To initiate start screen and then the rest of the scenes
def main():
   
   windowSurface.blit(STARTSCREEN, (0,0)) 
   drawTextBlack ('Press enter to continue',biggerfont, windowSurface, 300, 470)
   pygame.display.update()
   time.sleep(2.0)

   jungle = True
   weather(jungle)
   
   pygame.quit
   exit()
   
if __name__ == '__main__':
   main()

#--------------------------------------------------------------------------------------

