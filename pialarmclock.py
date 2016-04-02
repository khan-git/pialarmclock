import os, sys, time, datetime
import pygame
from Message import *


class AnalogFace(pygame.sprite.Sprite):
    """Clock object"""
    
    def __init__(self, rect, color=(0,0,255)):
        pygame.sprite.Sprite.__init__(self)
        self.color = color; 
        self.rect = pygame.Rect(rect);
        self.createImages();
        self.image = self.baseImage

    def createImages(self):
        """Draw Logan."""
        self.baseImage = pygame.Surface((self.rect.width, self.rect.height));
        rect = self.baseImage.get_rect()

        ## Face
        pygame.draw.circle(self.baseImage, self.color, rect.center, rect.width/2, 1);

    def drawArms(self):
        """Draw tha actual arms"""
        rect = self.baseImage.get_rect()
        pygame.draw.line(self.baseImage, self.color, rect.center, (rect.width/2, 0), 1)
        pygame.draw.line(self.baseImage, self.color, rect.center, (rect.width/2, 0), 1)
        pygame.draw.line(self.baseImage, self.color, rect.center, (rect.width/2, 0), 1)
        print time.localtime()
        
    def update(self):
        """Update ticks"""
        self.drawArms()

class DigitalFace(pygame.sprite.Sprite):
    
    def __init__(self, rect, color=(0,0,255)):
        pygame.sprite.Sprite.__init__(self)
        self.color = color; 
        self.rect = pygame.Rect(rect);
        self.createImages();
        self.image = self.baseImage

    def createImages(self):
        """Draw Logan."""
        self.baseImage = pygame.Surface((self.rect.width, self.rect.height));
            
    def update(self):
        """Update ticks"""
        msgSprite = pygame.sprite.GroupSingle(
            Message((time.strftime("%H:%M:%S", time.localtime(time.time())),), fontsize=50, align="center"));
        msgSprite.sprite.rect.topleft = self.baseImage.get_rect().topleft;
        msgSprite.draw(self.baseImage)
        
                
class AlarmClock:
    """Alarm clock class"""
    
    def __init__(self, width=320, height=240):
        pygame.init()
        self.width = width
        self.height = height
        self.time = pygame.time.Clock();
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.setFace(analog=False)
        self.clock = pygame.sprite.GroupSingle(DigitalFace(pygame.Rect((0, 0),(self.height, self.height))));

    def setFace(self, analog=True):
        if analog:
            self.analogface = True
            self.clock = pygame.sprite.GroupSingle(AnalogFace(pygame.Rect((0, 0),(self.height, self.height))));
        else:
            self.analogface = False
            self.clock = pygame.sprite.GroupSingle(DigitalFace(pygame.Rect((0, 0),(self.height, self.height))));
            
    def run(self):
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    if self.clock.sprite.rect.collidepoint(pos):
                        self.setFace(analog=(True if self.analogface == False else False))
                if event.type == pygame.QUIT:
                    sys.exit()
            self.clock.update()
            self.clock.draw(self.screen)
            pygame.display.flip()
            self.time.tick(1)
            
if __name__ == "__main__":
        clock = AlarmClock()
        clock.run()
        