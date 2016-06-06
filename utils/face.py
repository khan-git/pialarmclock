import pygame

class Face(pygame.sprite.Sprite):

    def update(self):
        raise NotImplementedError("A must have")
    
    def requestFace(self):
        return False
    
    def surrenderFace(self):
        return True
    
    def handleEvent(self, event):
        pass
    
    