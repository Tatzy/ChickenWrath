import pygcurse, pygame, sys, socket, json, requests
from io import StringIO
from pygame.locals import *

## Screen Size specification stuff
width = 60
height = 30
SERVER_IP = "http://127.0.0.1:8000"

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
    global s
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

        r = requests.post(url = SERVER_IP, data = "/") 
        r = requests.get(url = SERVER_IP + "/setup") 
        l = r.json()
        print(l)
        player1 = Player()
        win.colors=('black','black')
        win.fill('#',region=(0,0,width,height))

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
        co = {"Xl": player1.xl, "Yl": player1.yl}
        r = requests.post(url = "http://127.0.0.1:8000/coords", data = json.dumps(co))
        win.update()
        #msg = json.dumps({"Xl": player1.xl, "Yl": player1.yl, "Xg": player1.xg, "Yg": player1.yg}, sort_keys=True)
        #s.sendall(msg.encode('utf-8'))


if __name__ == '__main__':
    main()
