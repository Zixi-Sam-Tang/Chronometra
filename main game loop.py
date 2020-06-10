import pygame, random, os


pygame.init()
global win
win = pygame.display.set_mode((800, 800))


#title and Icon
pygame.display.set_caption("Chronometra")
icon = pygame.image.load('Images\Chronometra Icon.png')
pygame.display.set_icon(icon)



class player(object):
    def __init__(self, x, y, move):
        self.x = x
        self.y = y
        self.move = move
        self.vel = 0.5
    def draw(self, win):
        if self.move != "hidden":
            if self.move == "s": mainCharacter = pygame.image.load('Images\Main Character Front.png')
            elif self.move == "a": mainCharacter = pygame.image.load('Images\Main Character Left.png')
            elif self.move == "d": mainCharacter = pygame.image.load('Images\Main Character Right.png')
            elif self.move == "w": mainCharacter = pygame.image.load('Images\Main Character Back.png')
            win.blit(mainCharacter, (self.x, self.y))

class fireball(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def draw(self, win):
        win.blit(pygame.image.load('Images\Fire Ball Right.png'), (self.x, self.y))

class heart(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 7
    def draw(self, win):
        win.blit(pygame.image.load('Images\Heart.png'), (self.x, self.y))


def bf(stage):
    if stage == 1:
        for i in range(0, 10):
            y = random.randint(470, 647)
            fireballs.append(fireball(10, y))
        stage += 1

def redrawGameWindow():
    p.draw(win)


    if bossfight:
        win.blit(pygame.image.load('Images\Boss Fight Screen.png'), (0, 0))
        win.blit(pygame.image.load('Images\WrathDemon.png'), (275, 0))
        h.draw(win)
        for fb in fireballs:
            fb.draw(win)

    pygame.display.update()



bossfight = True
global fireballs
fireballs = []
stage = 1
p = player(450, 300, "s")
h = heart(384, 574)
# game loop
running = True
while running:


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_s] and not bossfight:
        p.y += p.vel
        p.move = "s"
    elif keys[pygame.K_s] and bossfight and h.y <= 657:
        h.y += h.vel
    if keys[pygame.K_d] and not bossfight:
        p.x += p.vel
        p.move = "d"
    elif keys[pygame.K_d] and bossfight and h.x <= 473:
        h.x += h.vel
    if keys[pygame.K_a] and not bossfight:
        p.x -= p.vel
        p.move = "a"
    elif keys[pygame.K_a] and bossfight and h.x >= 295:
        h.x -= h.vel
    if keys[pygame.K_w] and not bossfight:
        p.y -= p.vel
        p.move = "w"
    elif keys[pygame.K_w] and bossfight and h.y >= 480:
        h.y -= h.vel
    if bossfight and stage <= 3:
        p.move = "hidden"
        bf(stage)
        stage += 1

    for fb in fireballs:
        if fb.x > 0 and fb.x < 800:
            fb.x += 10
        else:
            fireballs.pop(fireballs.index(fb))
    win.fill((0, 0, 0))
    redrawGameWindow()
    pygame.display.update()