import pygame
import time
import math
from utils.face import Face

class AnalogClock(Face):
    """Clock object"""
    
    def __init__(self, rect, color=(0,0,255)):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.rect = pygame.Rect(rect)
        self.baseImage = pygame.Surface((self.rect.width, self.rect.height))
        self.image = self.baseImage

    def calcTickPos(self, center, radius, value, stretch=1.0):
        """Value is the value to calculate position for on a 60 items circle"""
        value = value - 15
        value = value % 60
        
        value = 60 - value
        
        x = math.cos(2 * math.pi * (value/60.0))
        y = -1 * math.sin(2 * math.pi * (value / 60.0))
        
        x *= stretch
        y *= stretch
        
        x += center[0]
        y += center[1]
        
        return (x,y)
    
    def drawArms(self):
        """Draw the actual arms"""
        rect = self.baseImage.get_rect()

        local = time.localtime(time.time())
        sec = self.calcTickPos(rect.center, rect.center[0], local[5]+(time.time() % 1), stretch=rect.center[0])
        pygame.draw.line(self.baseImage, self.color, rect.center, sec, 1)
        
        minute = self.calcTickPos(rect.center, rect.center[0], local[4]+local[5]/60.0, stretch=rect.center[0])
        pygame.draw.line(self.baseImage, self.color, rect.center, minute, 4)
        
        hour = self.calcTickPos(rect.center, rect.center[0], local[3]%12*5+local[4]*5/60.0, stretch=rect.center[0]/4*3)
        pygame.draw.line(self.baseImage, self.color, rect.center, hour, 8)
        
    def update(self):
        """Update ticks"""
        self.image.fill(pygame.Color("black"))
        ## Face
        rect = self.baseImage.get_rect()
        pygame.draw.circle(self.baseImage, self.color, rect.center, rect.height/2, 1);
        self.drawArms()

