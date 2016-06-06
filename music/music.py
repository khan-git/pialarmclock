import  os, random, pygame, sys

class Music(object):
    """ Plays selected audio files or picks a random file named music*.mp3."""
    def __init__(self):
        self.music = {};
        for fileMp3 in os.listdir(os.path.expanduser('~/.config/pialarmclock/audio')):
            if fileMp3.endswith(".mp3"):
                fileMp3 = os.path.join(os.path.expanduser('~/.config/pialarmclock/audio'),fileMp3)
                self.music[fileMp3] = False;
        if len(self.music) == 0:
            print "No music found. Music disabled!";
            self.disabled = True;
        else:
            self.disabled = False;
        self._playing = False
        
    def togglePlay(self):
        if self._playing == True:
            self.stopMusic()
            self._playing = False
        else:
            self.playMusic()
            self._playing = True
    
    def playMusic(self, music=None):
        if self.disabled:
            return;
        if(music == None):
            while(True):
                music = self.music.keys();
                music = music[random.randrange(len(music))];
                if(self.music[music] == False):
                    self.music[music] = True;
                    break;
                free = False;
                for mu in self.music:
                    if(self.music[mu] == False):
                        free = True;
                        break;
                if(free == False): self.resetPlayed();
        try:
            pygame.mixer.music.load(music);
            pygame.mixer.music.play(-1);
        except:
            print(str.format("Error loading music:  {0}.", music));
            sys.exit();

    def stopMusic(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
            
    def resetPlayed(self):
        if self.disabled:
            return;
        for mus in self.music:
            self.music[mus] = False;
