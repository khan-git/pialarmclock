import os, sys
import pygame

class AlarmClock:
    """Alarm clock class"""
    
    def __init__(self, width=320, height=240):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        
    def MainLoop(self):
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                    
if __name__ == "__main__":
        MainWindow = AlarmClock()
        MainWindow.MainLoop()
        