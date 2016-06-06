import pygame
import time
from utils.message import Message
from utils.face import Face

class DigitalClock(Face):
    
    def __init__(self, rect, color=(0,0,255)):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.rect = pygame.Rect(rect)
        self.baseImage = pygame.Surface((self.rect.width, self.rect.height))
        self.image = self.baseImage
        self.timeSprite = pygame.sprite.GroupSingle(Message(["wait...",]))
        self.dateSprite = pygame.sprite.GroupSingle(Message(["wait...",]))
        
    def update(self):
        """Update ticks"""
        local = time.localtime(time.time())
        
        self.timeSprite.add(Message((time.strftime("%H:%M:%S", local),), vector=(0,0), fontsize=90, align="left", padding=0, fgcolor=(0,0,255)))
        surfaceRect = self.image.get_rect()
        self.timeSprite.sprite.rect.midbottom = surfaceRect.center
        self.timeSprite.draw(self.baseImage)
        self.dateSprite.add(
            Message((time.strftime("%Y-%m-%d", local),), vector=(0,0), fontsize=25, align="left", padding=0, fgcolor=(0,0,255)))
        self.dateSprite.sprite.rect.midtop = self.timeSprite.sprite.rect.midbottom
        self.dateSprite.draw(self.baseImage)

        