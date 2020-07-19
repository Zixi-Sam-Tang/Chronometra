import pygame as pg
import random
from os import path
import math

pg.init()
global win
win = pg.display.set_mode((800, 800))

#title and Icon
pg.display.set_caption("Chronometra")
icon = pg.image.load('Images\Chronometra Icon.png')
pg.display.set_icon(icon)

class fireball(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 1

    def draw(self, win):
        win.blit(pg.image.load('Images\Fire Ball Right.png'), (self.x, self.y))

class heart(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 7
        self.rage = 0
    def draw(self, win):
        win.blit(pg.image.load('Images\Heart.png'), (self.x, self.y))
        #health bar
        pg.draw.rect(win, (255, 0, 0), (10, 400, 100, 20))
        if self.rage < 100: pg.draw.rect(win, (0, 255, 0), (10 + self.rage, 400, 100 - self.rage, 20))

    def hit(self):
        for fb in fireballs:
            if fb.x >= self.x - 16 and fb.x <= self.x + 16 and fb.y >= self.y - 16 and fb.y <= self.y + 16:
                fireballs.pop(fireballs.index(fb))
                self.rage += 8
                hit_sound.play()
        for fs in fireSpirits:
            if fs.x >= self.x - 16 and fs.x <= self.x + 16 and fs.y >= self.y - 16 and fs.y <= self.y + 16:
                fireSpirits.pop(fireSpirits.index(fs))
                self.rage += 5
                hit_sound.play()
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
            pg.draw.rect(win, (255, 0, 0), (self.x, self.y, 220, 3))
        else:
            win.blit(pg.image.load('Images\Laser.png'), (self.x - 50, self.y - 150))

class actB(object):
    def __init__(self):
        self.x = 80
        self.y = 500
        self.status = "not chosen"
    def draw(self, win):
        mouseX, mouseY = pg.mouse.get_pos()
        if mouseX >= self.x and mouseX <= self.x + 228 and mouseY >= self.y and mouseY <= self.y + 108:
            self.status = "chosen"
            win.blit(pg.image.load('Images\Act Chosen.png'), (self.x, self.y))
        else:
            self.status = "not chosen"
            win.blit(pg.image.load('Images\Act.png'), (self.x, self.y))

class fightB(object):
    def __init__(self):
        self.x = 500
        self.y = 500
        self.status = "not chosen"
    def draw(self, win):
        mouseX, mouseY = pg.mouse.get_pos()
        if mouseX >= self.x and mouseX <= self.x + 228 and mouseY >= self.y and mouseY <= self.y + 108:
            self.status = "chosen"
            win.blit(pg.image.load('Images\Fight Chosen.png'), (self.x, self.y))
        else:
            self.status = "not chosen"
            win.blit(pg.image.load('Images\Fight.png'), (self.x, self.y))

class text(object):
    def __init__(self):
        self.timer = 0
    def draw(self, win):
        if act and not fight:
            font = pg.font.SysFont('Comic Sans MS', 30)
            t = font.render('The Demon Blushes Deeply At Your Compliment.', False, (255, 255, 255))
            win.blit(t, (50, 500))
        else:
            font = pg.font.SysFont('Comic Sans MS', 30)
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
        win.blit(pg.image.load('Images\Fire Spirit.png'), (int(self.x), int(self.y)))


def redrawGameWindow():
    if bossfight:
        win.blit(pg.image.load('Images\Boss Fight Screen.png'), (0, 0))
        win.blit(pg.image.load('Images\WrathDemon.png'), (275, 50))
        h.draw(win)
        for fb in fireballs:
            fb.draw(win)
        if len(lasers) != 0: lasers[0].draw(win)
        for fs in fireSpirits:
            fs.draw(win)
    if playermove:
        win.blit(pg.image.load('Images\Playermove Background.png'), (0, 0))
        win.blit(pg.image.load('Images\WrathDemon.png'), (275, 0))
        if not act and not fight:
            a.draw(win)
            f.draw(win)
        elif t.timer < 30:
                t.draw(win)
                t.timer += 1
    if end and not playermove:
        if h.rage > 100:
            win.blit(pg.image.load('Images\Bad Ending BG.jpg'), (0, 0))
            font = pg.font.SysFont('Comic Sans MS', 30)
            txt = font.render('You Have Been Consumed By Your Rage.', False, (255, 255, 255))
            txt2 = font.render('GAME OVER.', False, (255, 255, 255))
            win.blit(txt, (125, 400))
            win.blit(txt2, (300, 500))
        elif compliment == 2:
            win.blit(pg.image.load('Images\Weird Ending ish.png'), (0, 0))
            win.blit(pg.image.load('Images\WrathDemon.png'), (200, 300))
            win.blit(pg.image.load('Images\Main Character Front.png'), (500, 500))
            font = pg.font.SysFont('Comic Sans MS', 25)
            txt = font.render('After Your Compliments, The Demon Falls In Love With You.', False, (255, 255, 255))
            txt2 = font.render('You Live Happily Ever After. THE END.', False, (255, 255, 255))
            win.blit(txt, (50, 600))
            win.blit(txt2, (150, 700))
        else:
            win.blit(pg.image.load('Images\Best Ending BG.png'), (0, 0))
            font = pg.font.SysFont('Comic Sans MS', 25)
            txt = font.render('CONGRATULATIONS! You Defeated The Wrath Demon.', False, (255, 255, 255))
            txt2 = font.render('THE END.', False, (255, 255, 255))
            win.blit(txt, (70, 600))
            win.blit(txt2, (350, 700))

    pg.display.update()

global compliment
compliment = 0
global act
act = False
global fight
fight = False
global bossfight
bossfight = True
global playermove
playermove = False
global end
end = False
temp = 0
global fireballs
fireballs = []
global lasers
lasers = []
global fireSpirits
fireSpirits = []
global a
a = actB()
global f
f = fightB()
global stage
stage = 1
global h
h = heart(384, 574)
global t
t = text()
global tick
tick = 0
# game loop
global running
running = True
game_folder = path.dirname(__file__)
music_folder = path.join(game_folder, 'music')
sound_folder = path.join(game_folder, 'snd')
pg.mixer.music.load(path.join(music_folder, 'Through the Fire and the Flames.mp3'))
pg.mixer.music.play(-1, 0.0)
pg.mixer.music.set_volume(0.25)
global laser_sound
laser_sound = pg.mixer.Sound(path.join(sound_folder, 'Laser.wav'))
laser_sound.set_volume(0.25)
global hit_sound
hit_sound = pg.mixer.Sound(path.join(sound_folder, 'hit sound.wav'))
hit_sound.set_volume(0.45)
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    keys = pg.key.get_pressed()
    if keys[pg.K_s] and bossfight and h.y <= 657:
        h.y += h.vel
    if keys[pg.K_d] and bossfight and h.x <= 473:
        h.x += h.vel
    if keys[pg.K_a] and bossfight and h.x >= 295:
        h.x -= h.vel
    if keys[pg.K_w] and bossfight and h.y >= 480:
        h.y -= h.vel
    if keys[pg.K_DOWN] and bossfight and h.y <= 657:
        h.y += h.vel
    if keys[pg.K_RIGHT] and bossfight and h.x <= 473:
        h.x += h.vel
    if keys[pg.K_LEFT] and bossfight and h.x >= 295:
        h.x -= h.vel
    if keys[pg.K_UP] and bossfight and h.y >= 480:
        h.y -= h.vel
    if playermove and pg.mouse.get_pressed()[0] and a.status == "chosen" and t.timer == 0:
        act = True
        compliment += 1
    elif playermove and pg.mouse.get_pressed()[0] and f.status == "chosen" and t.timer == 0:
        fight = True
        h.rage += 5

    if bossfight and stage <= 3:
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
                if lasers[0].timer == 20:
                    lasers[0].status = "shoot"
                    laser_sound.play()
                elif lasers[0].timer == 60:
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

    for fs in fireSpirits:
        velx = random.randint(0, 1)
        vely = random.randint(0, 1)
        fs.x += velx
        fs.y += vely
    for fb in fireballs:
        if fb.x > 0 and fb.x < 800:
            fb.x += fb.vel
        else:
            fireballs.pop(fireballs.index(fb))

    if t.timer >= 30:
        bossfight = True
        playermove = False
        t.timer = 0
        fight = False
        act = False

    h.hit()
    win.fill((0, 0, 0))
    redrawGameWindow()
pg.quit()