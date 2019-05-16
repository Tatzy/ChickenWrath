import pygcurse, pygame, sys, socket, json
from io import StringIO
from pygame.locals import *

## Screen Size specification stuff
width = 60
height = 30

## Menu Screen Setup
win = pygcurse.PygcurseWindow(width,height, fullscreen = False, caption = 'Chicken Wrath')
win.colors = ('red', 'black')
win.cursor = (23.5, 14)
win.write('Chicken Wrath')
win.colors = ('green','green')
win.fill('#', region=(0, 0, 1, 30))
win.fill('#', region=(59, 0, 1, 30))
win.cursor = (28,16)#
win.colors = ('red','gray')
win.write('Play')
win.cursor = (28,18)
win.colors = ('green','black')
win.write('Exit')
win.autoupdate = False
win.update()

class Player:
    xl = 0
    yl = 0
    xg = 0
    yg = 0
    def __init__(self):
        pass

    def controls(self, k):
        if k == K_ESCAPE:
            pygame.quit()
            sys.exit()
        elif k == K_UP:
            self.yl -= 1
        elif k == K_DOWN:
            self.yl += 1
        elif k == K_RIGHT:
            self.xl += 1
        elif k == K_LEFT:
            self.xl -= 1
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
    
    ## Initialize the Game
    if gameStart == True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 5000))
        player1 = Player()
        win.colors=('black','black')
        win.fill('#',region=(0,0,width,height))
        msg = s.recv(1024)
        my_json = msg.decode('utf8').replace("'", '"')
        data = json.loads(my_json)
        s = json.dumps(data, indent=4, sort_keys=True)                               
        l = json.loads(s)
        player1.xl = l["Xl"]
        player1.yl = l["Yl"]
        win.colors= ('yellow','black')
        win.fill('@', region = (l["Xl"], l["Yl"],1,1))
        win.update()
    
    while gameStart:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                player1.controls(event.key)
        win.colors=('black','black')
        win.fill('#',region=(0,0,width,height))
        win.colors=('yellow','black')
        win.fill('@', region = (player1.xl, player1.yl,1,1))
        win.update()


if __name__ == '__main__':
    main()
