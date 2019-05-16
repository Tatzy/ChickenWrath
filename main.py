import pygcurse, pygame, sys, socket
from pygame.locals import *
width = 60
height = 30
FPS = 30
win = pygcurse.PygcurseWindow(width,height, fullscreen = False, caption = 'Chicken Wrath')
win.colors = ('red', 'black')
win.cursor = (23.5, 14)
win.write('Chicken Wrath')
#win.fill('x')
win.colors = ('green','green')
win.fill('#', region=(0, 0, 1, 30))
win.fill('#', region=(59, 0, 1, 30))
win.cursor = (28,16)
win.colors = ('red','gray')
win.write('Play')
win.cursor = (28,18)
win.colors = ('green','black')
win.write('Exit')
win.update()

class Player:
    def __init__(self):
        pass

    def controls(self, k):
        if k == K_ESCAPE:
            pygame.quit()
            sys.exit()
        else:
            pass



def main():
    menu = True
    key = 0
    while menu:

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == K_DOWN:
                    key = (key + 1) % 2

                elif event.key == K_UP:
                    key = (key-1) % 2
                elif event.key == K_RETURN:
                    if key == 0:
                        menu = False
                        gameStart = True
                    else:
                        pygame.quit()
                        sys.exit()

            if key == 0:
                win.cursor = (28, 16)
                win.colors = ('red', 'gray')
                win.write('Play')
                win.cursor = (28, 18)
                win.colors = ('green', 'black')
                win.write('Exit')
                win.update()

            else:
                win.cursor = (28, 16)
                win.colors = ('green', 'black')
                win.write('Play')
                win.cursor = (28, 18)
                win.colors = ('red', 'gray')
                win.write('Exit')
                win.update()
    
    if gameStart == True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 5000))
        player1 = Player()
        win.colors=('black','black')
        win.fill('#',region=(0,0,width,height))
        msg = s.recv(1024)                                     
        print(msg.decode('utf-8')) 
    
    while gameStart:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                player1.controls(event.key)

if __name__ == '__main__':
    main()
