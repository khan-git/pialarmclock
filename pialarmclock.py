import os, sys, time, datetime
import pygame
from Message import *
import math


class AnalogFace(pygame.sprite.Sprite):
    """Clock object"""
    
    def __init__(self, rect, color=(0,0,255)):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.rect = pygame.Rect(rect)
        self.createImages()
        self.image = self.baseImage

    def createImages(self):
        """Draw Logan."""
        self.baseImage = pygame.Surface((self.rect.width, self.rect.height))


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
        """Draw tha actual arms"""
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

class DigitalFace(pygame.sprite.Sprite):
    
    def __init__(self, rect, color=(0,0,255)):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.rect = pygame.Rect(rect)
        self.createImages()
        self.image = self.baseImage
        
    def createImages(self):
        """Draw Logan."""
        self.baseImage = pygame.Surface((self.rect.width, self.rect.height))
            
    def update(self):
        """Update ticks"""
        local = time.localtime(time.time())
        
        timeSprite = pygame.sprite.GroupSingle(
            Message((time.strftime("%H:%M:%S", local),), vector=(0,0), fontsize=90, align="left", padding=0, fgcolor=(0,0,255)))
        surfaceRect = self.image.get_rect()
        timeSprite.sprite.rect.midbottom = surfaceRect.center
        timeSprite.draw(self.baseImage)
        dateSprite = pygame.sprite.GroupSingle(
            Message((time.strftime("%Y-%m-%d", local),), vector=(0,0), fontsize=25, align="left", padding=0, fgcolor=(0,0,255)))
        dateSprite.sprite.rect.midtop = timeSprite.sprite.rect.midbottom
        dateSprite.draw(self.baseImage)
        

class Button(pygame.sprite.Sprite):
    
    def __init__(self, rect, color=(0,0,255), action=None):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.action = action
        self.rect = pygame.Rect(rect)
        self.baseImage = pygame.Surface((self.rect.width, self.rect.height))
        self.image = self.baseImage
        
    def update(self):
        rect = self.baseImage.get_rect()
        pygame.draw.circle(self.baseImage, self.color, rect.center, rect.width/2, 1);
        
    def touchDown(self):
        rect = self.baseImage.get_rect()
        pygame.draw.circle(self.baseImage, self.color, rect.center, rect.width/2, 0);
        
    def touchUp(self):
        rect = self.baseImage.get_rect()
        self.image.fill(pygame.Color("black"))
        pygame.draw.circle(self.baseImage, self.color, rect.center, rect.width/2, 1);
        if self.action is not None:
            self.action()
        
    def setAction(self, action):
        self.action = action
                 
class AlarmClock:
    """Alarm clock class"""
    
    def __init__(self, width=320, height=240, fullscreen=False, mousevisible=False):
        pygame.init()
        pygame.mouse.set_visible(mousevisible)
        self.width = width
        self.height = height
        self.time = pygame.time.Clock()
        if fullscreen:
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((self.width, self.height))
        self.setFace(analog=False)
        self.buttons()

    def buttons(self):
        self.buttons = []
        for i in range(4):
            butt = pygame.sprite.GroupSingle(Button(pygame.Rect((0, 0),(self.height/5, self.height/5))))
            butt.sprite.rect.topright = (self.width, self.height/4*i)
            self.buttons.append(butt)
        self.buttons[0].sprite.setAction(self.toggleFace)
        self.buttons[3].sprite.setAction(sys.exit)
    
    def action(self):
        sys.exit()
    
    def toggleFace(self):
        if self.analogface:
            self.setFace(analog=False)
        else:
            self.setFace()
            
    def setFace(self, analog=True):
        if analog:
            self.analogface = True
            self.clock = pygame.sprite.GroupSingle(AnalogFace(pygame.Rect((0, 0),(self.height, self.height))))
        else:
            self.analogface = False
            self.clock = pygame.sprite.GroupSingle(DigitalFace(pygame.Rect((0, 0),(self.height, self.height))))
            
    def run(self):
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for butt in self.buttons:
                        if butt.sprite.rect.collidepoint(pos):
                            butt.sprite.touchDown()
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
#                     if self.clock.sprite.rect.collidepoint(pos):
#                         self.setFace(analog=(True if self.analogface == False else False))
                    for butt in self.buttons:
                        if butt.sprite.rect.collidepoint(pos):
                            butt.sprite.touchUp()
                if event.type == pygame.QUIT:
                    sys.exit()
            self.clock.update()
            self.clock.draw(self.screen)
            for butt in self.buttons:
                butt.update()
                butt.draw(self.screen)
            pygame.display.flip()
            self.time.tick(25)
            
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--fullscreen", action="store_true", help="Full screen", default=False)
    parser.add_argument("-m", "--mousevisible", action="store_false", help="Mouse visible", default=True)
    args = parser.parse_args()

    clock = AlarmClock(fullscreen=args.fullscreen, mousevisible=args.mousevisible)
    clock.run()
