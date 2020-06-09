import pygame

pygame.init()

screen = pygame.display.set_mode((800, 800))

#title and Icon
pygame.display.set_caption("Chronometra")
icon = pygame.image.load('Images\Chronometra Icon.png')
pygame.display.set_icon(icon)



def player(move, x, y):
    if move == "s": mainCharacter = pygame.image.load('Images\Main Character Front.png')
    elif move == "a": mainCharacter = pygame.image.load('Images\Main Character Left.png')
    elif move == "d": mainCharacter = pygame.image.load('Images\Main Character Right.png')
    elif move == "w": mainCharacter = pygame.image.load('Images\Main Character Back.png')
    screen.blit(mainCharacter, (x, y))


PlayerX = 450
PlayerY = 300
move = "s"
speed = 0.5
xChange = 0
yChange = 0
w = False
a = False
d = False
s = False

# game loop
running = True
while running:

    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                yChange = speed
                move = "s"
                s = True
            elif event.key == pygame.K_d:
                xChange = speed
                move = "d"
                d = True
            elif event.key == pygame.K_a:
                xChange = -speed
                move = "a"
                a = True
            elif event.key == pygame.K_w:
                yChange = -speed
                move = "w"
                w = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                a = False
                if d:
                    xChange = speed
                else:
                    xChange = 0
            if event.key == pygame.K_d:
                d = False
                if a:
                    xChange = -speed
                else:
                    xChange = 0
            if event.key == pygame.K_s:
                s = False
                if w:
                    yChange = -speed
                else:
                    yChange = 0
            if event.key == pygame.K_w:
                w = False
                if s:
                    yChange = speed
                else:
                    yChange = 0

    PlayerX += xChange
    PlayerY += yChange
    player(move, PlayerX, PlayerY)
    pygame.display.update()