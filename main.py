import pygame as pg
import sys
from settings import *
from sprites import *
from os import path
from tilemap import *
import random

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        icon = pg.image.load('Images\Chronometra Icon.png')
        pg.display.set_icon(icon)
        self.load_data()
        self.orange_collected = False
        self.purple_collected = False
        self.yellow_collected = False
        self.green_collected = False
        self.orange_placed = False
        self.purple_placed = False
        self.yellow_placed = False
        self.green_placed = False
        self.next_level = False
        self.bf = False

    def load_data(self):
        self.game_folder = path.dirname(__file__)
        self.img_folder = path.join(self.game_folder, 'img')
        self.map_folder = path.join(self.game_folder, 'maps')
        self.music_folder = path.join(self.game_folder, 'music')
        self.snd_folder = path.join(self.game_folder, 'snd')
        self.player_img_front = pg.image.load(path.join(self.img_folder, 'Main Character Front.png')).convert_alpha()
        self.player_img_back = pg.image.load(path.join(self.img_folder, 'Main Character Back.png')).convert_alpha()
        self.player_img_left = pg.image.load(path.join(self.img_folder, 'Main Character Left.png')).convert_alpha()
        self.player_img_right = pg.image.load(path.join(self.img_folder, 'Main Character Right.png')).convert_alpha()
        self.collect_sound = pg.mixer.Sound(path.join(self.snd_folder, 'Collect_Ore_Chime.wav'))
        self.collect_sound.set_volume(0.3)
        self.place_sound = pg.mixer.Sound(path.join(self.snd_folder, 'Ore_Drop_Place.wav'))
        self.place_sound.set_volume(0.5)
        pg.mixer.music.load(path.join(self.music_folder, 'Stone.ogg'))

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.bossfight = pg.sprite.Group()
        self.yellow = pg.sprite.Group()
        self.orange = pg.sprite.Group()
        self.purple = pg.sprite.Group()
        self.green = pg.sprite.Group()
        self.imgs = {'stone': TiledMap(path.join(self.map_folder, 'Stone.tmx')),
                     'lava': TiledMap(path.join(self.map_folder, 'Lava.tmx'))}
        if self.next_level:
            self.map = self.imgs['lava']
        elif not self.next_level:
            self.map = self.imgs['stone']
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == 'Player':
                self.player = Player(self, tile_object.x, tile_object.y)
            if tile_object.name == 'Walls':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == 'Boss Fight':
                Boss_Fight(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == 'Green':
                Green(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == 'Purple':
                Purple(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == 'Orange':
                Orange(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == 'Yellow':
                Yellow(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
        self.camera = Camera(self.map.width, self.map.height)


    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        pg.mixer.music.play(-1, 0.0)
        pg.mixer.music.set_volume(0.1)
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)
        if self.next_level:
            self.playing = False
        green_hit = pg.sprite.spritecollide(self.player, self.green, False)
        if green_hit:
            if self.map == self.imgs['stone']:
                if not self.green_collected:
                    status = 'Green ore collected.'
                    print(status)
                    self.collect_sound.play()
                    self.green_collected = True
            elif self.map == self.imgs['lava']:
                if not self.green_placed:
                    status = 'Green ore placed.'
                    print(status)
                    self.place_sound.play()
                    self.green_placed = True

        purple_hit = pg.sprite.spritecollide(self.player, self.purple, False)
        if purple_hit:
            if self.map == self.imgs['stone']:
                if not self.purple_collected:
                    status = 'Purple ore collected.'
                    print(status)
                    self.collect_sound.play()
                    self.purple_collected = True
            elif self.map == self.imgs['lava']:
                if not self.purple_placed:
                    status = 'Purple ore placed.'
                    print(status)
                    self.place_sound.play()
                    self.purple_placed = True

        orange_hit = pg.sprite.spritecollide(self.player, self.orange, False)
        if orange_hit:
            if self.map == self.imgs['stone']:
                if not self.orange_collected:
                    status = 'Orange ore collected.'
                    print(status)
                    self.collect_sound.play()
                    self.orange_collected = True
            elif self.map == self.imgs['lava']:
                if not self.orange_placed:
                    status = 'Orange ore placed.'
                    print(status)
                    self.place_sound.play()
                    self.orange_placed = True

        yellow_hit = pg.sprite.spritecollide(self.player, self.yellow, False)
        if yellow_hit:
            if self.map == self.imgs['stone']:
                if not self.yellow_collected:
                    status = 'Yellow ore collected.'
                    print(status)
                    self.collect_sound.play()
                    self.yellow_collected = True
            elif self.map == self.imgs['lava']:
                if not self.yellow_placed:
                    status = 'Yellow ore placed.'
                    print(status)
                    self.place_sound.play()
                    self.yellow_placed = True

        bossfight = pg.sprite.spritecollide(self.player, self.bossfight, False)
        if bossfight:
            if self.map == self.imgs['stone']:
                if self.yellow_collected and self.orange_collected and self.purple_collected and self.green_collected:
                    status = 'Next Level!'
                    print(status)
                    self.next_level = True
                else:
                    status = 'Collect all the ores!'
                    print(status)
            if self.map == self.imgs['lava']:
                if self.yellow_placed and self.orange_placed and self.purple_placed and self.green_placed:
                    status = 'Boss Fight!'
                    print(status)
                    self.bf = True
                else:
                    status = 'Place all the ores!'
                    print(status)

        if self.next_level:
            self.show_load_screen()
            self.new()
            pg.mixer.music.fadeout(1000)
            pg.mixer.music.load(path.join(self.music_folder, 'Lava.ogg'))
            pg.mixer.music.play(-1, 0.0)
            pg.mixer.music.set_volume(0.25)
            self.next_level = False

        if self.bf:
            exec(open('main_game_loop.py').read())
            self.quit()


    def draw(self):
        # self.screen.fill(BGCOLOR)
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        # self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()

    def menu(self):
        background = pg.image.load('Images\Chronometra_Start.png')
        background_rect = background.get_rect()
        pg.display.set_mode((768, 368)).blit(background, background_rect)
        pg.display.flip()
        pg.event.wait()
        waiting = True
        while waiting:
            pg.time.Clock().tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.KEYUP or event.type == pg.MOUSEBUTTONDOWN:
                    waiting = False

    def show_load_screen(self):
        background = pg.image.load(path.join(path.join(path.dirname(__file__), 'img'), 'Loading.png')).convert_alpha()
        background_rect = background.get_rect()
        pg.display.set_mode((WIDTH, HEIGHT)).blit(background, background_rect)
        pg.display.flip()
        pg.event.wait()
        temp = 0
        while temp <= 50:
            pg.time.Clock().tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.KEYUP or event.type == pg.MOUSEBUTTONDOWN:
                    temp = 100
            temp+=1

# create the game object
g = Game()
g.new()
g.menu()
g.show_load_screen()
while not g.bf:
    g.run()