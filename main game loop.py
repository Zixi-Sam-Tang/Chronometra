import pygame, random, math


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
        if self.rage < 100: pygame.draw.rect(win, (0, 255, 0), (10 + self.rage, 400, 100 - self.rage, 20))

    def hit(self):
        for fb in fireballs:
            if fb.x >= self.x - 16 and fb.x <= self.x + 16 and fb.y >= self.y - 16 and fb.y <= self.y + 16:
                fireballs.pop(fireballs.index(fb))
                self.rage += 8
        for fs in fireSpirits:
            if fs.x >= self.x - 16 and fs.x <= self.x + 16 and fs.y >= self.y - 16 and fs.y <= self.y + 16:
                fireSpirits.pop(fireSpirits.index(fs))
                self.rage += 5
        if len(lasers) != 0 and lasers[0].status == "shoot" and self.y >= lasers[0].y - 50 and self.y <= lasers[0].y + 15:
            self.rage += 5


class laser(object):
    def __init__(self, y):
        self.x = 295
        self.y = y
        self.timer = 0
        self.status = "ready"
    def draw(self, win):
        if self.status == "ready":
            pygame.draw.rect(win, (255, 0, 0), (self.x, self.y, 220, 3))
        else:
            win.blit(pygame.image.load('Images\Laser.png'), (self.x - 50, self.y - 150))

class actB(object):
    def __init__(self):
        self.x = 80
        self.y = 500
        self.status = "not chosen"
    def draw(self, win):
        mouseX, mouseY = pygame.mouse.get_pos()
        if mouseX >= self.x and mouseX <= self.x + 228 and mouseY >= self.y and mouseY <= self.y + 108:
            self.status = "chosen"
            win.blit(pygame.image.load('Images\Act Chosen.png'), (self.x, self.y))
        else:
            self.status = "not chosen"
            win.blit(pygame.image.load('Images\Act.png'), (self.x, self.y))

class fightB(object):
    def __init__(self):
        self.x = 500
        self.y = 500
        self.status = "not chosen"
    def draw(self, win):
        mouseX, mouseY = pygame.mouse.get_pos()
        if mouseX >= self.x and mouseX <= self.x + 228 and mouseY >= self.y and mouseY <= self.y + 108:
            self.status = "chosen"
            win.blit(pygame.image.load('Images\Fight Chosen.png'), (self.x, self.y))
        else:
            self.status = "not chosen"
            win.blit(pygame.image.load('Images\Fight.png'), (self.x, self.y))

class text(object):
    def __init__(self):
        self.timer = 0
    def draw(self, win):
        if act and not fight:
            font = pygame.font.SysFont('Comic Sans MS', 30)
            t = font.render('The Demon Blushes Deeply At Your Compliment.', False, (255, 255, 255))
            win.blit(t, (50, 500))
        else:
            font = pygame.font.SysFont('Comic Sans MS', 30)
            t = font.render('The Violence Increased Your Rage.', False, (255, 255, 255))
            win.blit(t, (150, 500))
            t2 = font.render('It Is Not The Way.', False, (255, 255, 255))
            win.blit(t2, (150, 600))

class fireSpirit(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.timer = 0
    def draw(self, win):
        win.blit(pygame.image.load('Images\Fire Spirit.png'), (int(self.x), int(self.y)))




def redrawGameWindow():
    if puzzle: p.draw(win)
    if bossfight:
        win.blit(pygame.image.load('Images\Boss Fight Screen.png'), (0, 0))
        win.blit(pygame.image.load('Images\WrathDemon.png'), (275, 0))
        h.draw(win)
        for fb in fireballs:
            fb.draw(win)
        if len(lasers) != 0: lasers[0].draw(win)
        for fs in fireSpirits:
            fs.draw(win)
    if playermove:
        win.blit(pygame.image.load('Images\Playermove Background.png'), (0, 0))
        win.blit(pygame.image.load('Images\WrathDemon.png'), (275, 0))
        if not act and not fight:
            a.draw(win)
            f.draw(win)
        elif t.timer < 30:
            t.draw(win)
            t.timer += 1
    if end and not playermove:
        if h.rage > 100:
            win.blit(pygame.image.load('Images\Bad Ending BG.png'), (0, 0))
            font = pygame.font.SysFont('Comic Sans MS', 30)
            txt = font.render('You Have Been Consumed By Your Rage.', False, (255, 255, 255))
            txt2 = font.render('GAME OVER', False, (255, 255, 255))
            win.blit(txt, (150, 400))
            win.blit(txt2, (300, 500))
        elif compliment >= 2:
            win.blit(pygame.image.load('Images\Weird Ending ish.png'), (0, 0))
            win.blit(pygame.image.load('Images\WrathDemon.png'), (200, 300))
            win.blit(pygame.image.load('Images\Main Character Front.png'), (500, 400))
            font = pygame.font.SysFont('Comic Sans MS', 25)
            txt = font.render('After Your Compliments, The Demon Falls In Love With You.', False, (255, 255, 255))
            txt2 = font.render('You Live Happily Ever After. THE END', False, (255, 255, 255))
            win.blit(txt, (30, 600))
            win.blit(txt2, (120, 700))
        else:
            font = pygame.font.SysFont('Comic Sans MS', 25)
            txt = font.render('CONGRADULATIONS! You Survived The Wrath Demon.', False, (255, 255, 255))
            txt2 = font.render('THE END.', False, (255, 255, 255))
            win.blit(txt, (70, 400))
            win.blit(txt2, (350, 500))

    pygame.display.update()

global compliment
compliment = 0
act = False
fight = False
bossfight = True
playermove = False
puzzle = False
end = False
temp = 0
global fireballs
fireballs = []
global lasers
lasers = []
global fireSpirits
fireSpirits = []
stage = 1
p = player(450, 300, "s")
h = heart(384, 574)
t = text()
global tick
tick = 0
# game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_s] and puzzle:
        p.y += p.vel
        p.move = "s"
    elif keys[pygame.K_s] and bossfight and h.y <= 657:
        h.y += h.vel
    if keys[pygame.K_d] and puzzle:
        p.x += p.vel
        p.move = "d"
    elif keys[pygame.K_d] and bossfight and h.x <= 473:
        h.x += h.vel
    if keys[pygame.K_a] and puzzle:
        p.x -= p.vel
        p.move = "a"
    elif keys[pygame.K_a] and bossfight and h.x >= 295:
        h.x -= h.vel
    if keys[pygame.K_w] and puzzle:
        p.y -= p.vel
        p.move = "w"
    elif keys[pygame.K_w] and bossfight and h.y >= 480:
        h.y -= h.vel
    if playermove and pygame.mouse.get_pressed()[0] and a.status == "chosen":
        act = True
        compliment += 1
    elif playermove and pygame.mouse.get_pressed()[0] and f.status == "chosen":
        fight = True
        h.rage += 5



    if bossfight and stage <= 3:
        p.move = "hidden"
        if stage == 1:
            if temp != 50:
                y = random.randint(470, 647)
                fireballs.append(fireball(10, y))
                temp += 1
            if temp == 50 and len(fireballs) == 0:
                stage += 1
                temp = 0
                bossfight = False
                playermove = True
        elif stage == 2:
            if temp != 5:
                y = random.randint(470, 647)
                lasers.append(laser(y))
                temp += 1
            if len(lasers) != 0:
                if lasers[0].timer == 10:
                    lasers[0].status = "shoot"
                elif lasers[0].timer == 20:
                    lasers.pop(0)
                if len(lasers) != 0: lasers[0].timer += 1
            else:
                bossfight = False
                stage += 1
                temp = 0
                playermove = True
        elif stage == 3:
            x = random.randint(100, 500)
            if temp != 70:
                fireSpirits.append(fireSpirit(x, 470))
                temp += 1
            if len(fireSpirits) != 0:
                for fs in fireSpirits:
                    if fs.y > 800:
                        fireSpirits.pop(fireSpirits.index(fs))
                    else:
                        fs.timer += 1
            else:
                end = True
                bossfight = False
                playermove = False

    if h.rage > 100:
        end = True
        bossfight = False
        playermove = False

    if playermove and not fight and not act:
        a = actB()
        f = fightB()

    for fs in fireSpirits:
        velx = random.randint(1, 10)
        vely = random.randint(1, 10)
        fs.x += velx
        fs.y += vely
    for fb in fireballs:
        if fb.x > 0 and fb.x < 800:
            fb.x += fb.vel
        else:
            fireballs.pop(fireballs.index(fb))

    if t.timer == 30:
        bossfight = True
        playermove = False
        t.timer = 0
        fight = False
        act = False

    h.hit()
    win.fill((0, 0, 0))
    redrawGameWindow()
pygame.quit()
