import pygame, random, os, pytmx


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
        self.vel = 10

    def draw(self, win):
        win.blit(pygame.image.load('Images\Fire Ball Right.png'), (self.x, self.y))

class heart(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 7
        self.rage = 0
    def draw(self, win):
        win.blit(pygame.image.load('Images\Heart.png'), (self.x, self.y))
        #health bar
        pygame.draw.rect(win, (255, 0, 0), (10, 400, 100, 20))
        pygame.draw.rect(win, (0, 255, 0), (10 + self.rage, 400, 100 - self.rage, 20))

    def hit(self):
        for fb in fireballs:
            if fb.x >= h.x - 16 and fb.x <= h.x + 16 and fb.y >= h.y - 16 and fb.y <= h.y + 16:
                fireballs.pop(fireballs.index(fb))
                self.rage += 5

def redrawGameWindow():
    p.draw(win)
    if bossfight:
        win.blit(pygame.image.load('Images\Boss Fight Screen.png'), (0, 0))
        win.blit(pygame.image.load('Images\WrathDemon.png'), (275, 0))
        h.draw(win)
        for fb in fireballs:
            fb.draw(win)
    pygame.display.update()


global FPS
FPS = 60
bossfight = True
temp = 0
global fireballs
fireballs = []
stage = 1
p = player(450, 300, "s")
h = heart(384, 574)
# game loop
running = True
while running:

    tick = pygame.time.get_ticks()
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
        if stage == 1:
            y = random.randint(470, 647)
            fireballs.append(fireball(10, y))
            temp += 1
            if temp == 7:
                stage += 1
                temp = 0
        if stage == 2:
            y = random.randint(470, 647)
            fireballs.append(fireball(10, y))
            temp += 1
            if temp == 50:
                stage += 1
                temp = 0

    for fb in fireballs:
        if fb.x > 0 and fb.x < 800:
            fb.x += fb.vel
        else:
            fireballs.pop(fireballs.index(fb))
    h.hit()
    win.fill((0, 0, 0))
    redrawGameWindow()
pygame.quit()
