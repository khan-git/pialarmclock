import datetime
from music.music import Music
import pygame
from utils.message import Message
from utils.face import Face

class Alarm(Face):
    
    def __init__(self, rect, color=(0,0,255)):
        pygame.sprite.Sprite.__init__(self)
        self._alarmList = {}
        self.color = color
        self.rect = pygame.Rect(rect)
        self.music = Music()

        self.requestingFace = False
        self.baseImage = pygame.Surface((self.rect.width, self.rect.height))
        self.image = self.baseImage
        self.alarmSprite = pygame.sprite.GroupSingle(Message(("Wait....",), vector=(0,0), fontsize=90, align="left", padding=0, fgcolor=(0,0,255)))

        
    def addTime(self, datetime):
        self._alarmList[datetime] = {'music':None}
        print "Add "+str(datetime)
    
    def removeTime(self, datetime):
        if self._alarmList.has_key(datetime):
            self._alarmList.pop(datetime)
    
    def update(self):
        currentDateTime = datetime.datetime.today()
        margin = datetime.timedelta(seconds=1)
        for alarmItem in self._alarmList.keys():
            if currentDateTime - margin <= alarmItem <= currentDateTime + margin:
                self.requestingFace = True
                self.music.playMusic()

        self.image.fill(pygame.Color("black"))
        rect = self.baseImage.get_rect()
        pygame.draw.circle(self.baseImage, self.color, rect.center, rect.height/2, 1);

        surfaceRect = self.image.get_rect()
        self.alarmSprite.sprite.rect.midbottom = surfaceRect.center
        self.alarmSprite.draw(self.baseImage)

    def requestFace(self):
        return self.requestingFace
    
    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(pos):
                print "Hello"
                rect = self.baseImage.get_rect()
                pygame.draw.circle(self.baseImage, self.color, rect.center, rect.width/2, 0);


