import sys, datetime
import pygame
from music.music import Music
from faces import *
from utils.alarm import Alarm
from faces.alarmsetting import AlarmSetting


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


    
    
class PiAlarmClock:
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
        self._currentFace = pygame.sprite.GroupSingle(digitalclock.DigitalClock(pygame.Rect((0, 0),(self.height, self.height))))
        self.audio = Music()
        self.alarm = Alarm(pygame.Rect((0, 0),(self.height, self.height)))
        self.buttons()
        
        self.faces = {}
        self.faces['alarmSettings'] = AlarmSetting(pygame.Rect((0, 0),(self.height, self.height)), self.alarm)

    def buttons(self):
        self.buttons = []
        for i in range(4):
            butt = pygame.sprite.GroupSingle(Button(pygame.Rect((0, 0),(self.height/5, self.height/5))))
            butt.sprite.rect.topright = (self.width, self.height/4*i)
            self.buttons.append(butt)
        self.buttons[0].sprite.setAction(self.toggleFace)
        self.buttons[1].sprite.setAction(self.audio.togglePlay)
        self.buttons[2].sprite.setAction(self.setFaceAlarmSetting)
        self.buttons[3].sprite.setAction(sys.exit)
    
    def setFaceAlarmSetting(self):
        self._currentFace.add(self.faces['alarmSettings'])
        
    def addAlarm(self):
        self.alarm.addTime(datetime.datetime.now() + datetime.timedelta(seconds=5))
        self._currentFace.add(self.alarm)
        
    def toggleFace(self):
        if isinstance(self._currentFace.sprite, digitalclock.DigitalClock):
            self._currentFace.add(analogclock.AnalogClock(pygame.Rect((0, 0),(self.height, self.height))))
        else:
            self._currentFace.add(digitalclock.DigitalClock(pygame.Rect((0, 0),(self.height, self.height))))
            
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
                self._currentFace.sprite.handleEvent(event)
                if event.type == pygame.QUIT:
                    sys.exit()
            self.alarm.update()
            if self.alarm.requestFace():
                self._currentFace.add(self.alarm)
            self._currentFace.update()
            self._currentFace.draw(self.screen)
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

    clock = PiAlarmClock(fullscreen=args.fullscreen, mousevisible=args.mousevisible)
    clock.run()
