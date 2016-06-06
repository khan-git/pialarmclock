from utils.face import Face
import pygame
from utils.message import Message
from utils.alarm import Alarm

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

class Line(Face):
    def __init__(self, rect, color=(0,0,255), text=""):
        pygame.sprite.Sprite.__init__(self)
        self._alarmList = {}
        self.color = color
        self.rect = pygame.Rect(rect)
        self.text = text
        self.baseImage = pygame.Surface((self.rect.width, self.rect.height))
        self.image = self.baseImage
        self.faceSprite = pygame.sprite.GroupSingle(Message((self.text,), vector=(0,0), fontsize=45, align="left", padding=0, fgcolor=(0,0,255)))
        surfaceRect = self.image.get_rect()
        self.faceSprite.sprite.rect.midleft = surfaceRect.midleft
        
    def update(self):
        self.faceSprite.draw(self.baseImage)
        
class AlarmSetting(Face):

    def __init__(self, rect, alarm, color=(0,0,255)):
        pygame.sprite.Sprite.__init__(self)
        self._alarmList = {}
        if isinstance(alarm, Alarm):
            self._alarmObject = alarm
        else:
            raise Exception("Not an Alarm-class object")
        self.color = color
        self.rect = pygame.Rect(rect)

        self.requestingFace = False
        self.baseImage = pygame.Surface((self.rect.width, self.rect.height))
        self.image = self.baseImage
        self._lines = []
        for i in range(4):
            line = pygame.sprite.GroupSingle(Line(pygame.Rect((0, 0),(rect.height/5*4, rect.height/5)), text="Hello"))
            line.sprite.rect.topright = (rect.width, rect.height/4*i)
            self._lines.append(line)

    def addAlarm(self):
            line = pygame.sprite.GroupSingle(Button(pygame.Rect((0, 0),(self.rect.height/5, self.rect.height/5))))
            line.sprite.rect.topright = (self.rect.width, self.rect.height/4)
            line.sprite.setAction(self.addAlarm)
            self._lines.append(line)
        
    def update(self):
        for line in self._lines:
            line.update()
#             line.sprite.rect.midbottom = self.image.get_rect()
            line.draw(self.baseImage)

    def handleEvent(self, event):
        pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            for butt in self._lines:
                if butt.sprite.rect.collidepoint(pos):
                    butt.sprite.touchDown()
        if event.type == pygame.MOUSEBUTTONUP:
            for butt in self._lines:
                if butt.sprite.rect.collidepoint(pos):
                    butt.sprite.touchUp()
