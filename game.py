import math
import pygame
import random
from pygame import mixer
from pygame import K_LEFT, K_RIGHT, K_SPACE

pygame.init()  # initialize pygame
screen = pygame.display.set_mode((1000, 600))  # creation of screen 1000=length=X 600=breadth=Y
background = pygame.image.load("C:\\Users\\USER\\PycharmProjects\\PythonProject\\space.png")
mixer.music.load("bgm.wav")
mixer.music.play(-1)
mixer.music.set_volume(0.3)
# Title & Icon
pygame.display.set_caption("Allienoid")
icon = pygame.image.load("C:\\Users\\USER\\PycharmProjects\\PythonProject\\monster.png")
pygame.display.set_icon(icon)
# Player
playerI = pygame.image.load("C:\\Users\\USER\\PycharmProjects\\PythonProject\\space-ship.png")
playerX = 480
playerY = 500
playerX_change = 0
# Enemy
enemyI = []
enemyX = []
enemyY = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyI.append(pygame.image.load("C:\\Users\\USER\\PycharmProjects\\PythonProject\\alien.png"))
    enemyX.append(random.randint(0,938))
    enemyY.append(random.randint(50,150))
    enemyX_change = 2
    enemyY_change = 40
# Bullet
bulletI = pygame.image.load("C:\\Users\\USER\\PycharmProjects\\PythonProject\\laser.png")
bulletX = 0
bulletY = 500
bulletX_change = 0
bulletY_change = 5
bullet_state = "ready" #bullet not moving
#SCORE
score_value = 0
font = pygame.font.Font("freesansbold.ttf",40)
textX = 10
textY = 10
#Game Over
over_font = pygame.font.Font("freesansbold.ttf",90)

def show_score(x,y):
    score = font.render("Score-->" + str(score_value),True,(255, 255, 255))
    screen.blit(score, (x, y))

def game_over():
    over = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over, (220, 250))

def player(x, y):  # update player movement
    screen.blit(playerI, (x, y))

def enemy(x, y, i):  # update enemy movement
    screen.blit(enemyI[i], (x, y))

def fire(x,y): #fire bullet moves
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletI,(x+16,y+10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2))) #formula of distance between two coordinate
    if distance < 27:
        return True
    return False

# GameLoop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # when keyboard is pressed left or right
        if event.type == pygame.KEYDOWN:  # pressing key button
            if event.key == K_LEFT:
                playerX_change = -5
            if event.key == K_RIGHT:
                playerX_change = +5
            if event.key == K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX #get current x coordinate of spaceship
                    fire(bulletX,bulletY)
        if event.type == pygame.KEYUP:  # releasing key button
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    # R,G,B
    screen.fill((0, 0, 0))
    screen.blit(background,(0,0))
    #Player Boundary Check
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 938:  # 1000-62pix=938
        playerX = 938
    #Enemy Movement
    for i in range(num_of_enemies):
        if enemyY[i] > 440: #Game Over
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over()
            break
        enemyX[i] += enemyX_change
        if enemyX[i] <= 0:
            enemyX_change = 2
            enemyY[i] += enemyY_change
        elif enemyX[i] >= 968:
            enemyX_change = -2
            enemyY[i] += enemyY_change
        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            kill_sound = mixer.Sound("killS.wav")
            kill_sound.play()
            bulletY = 500
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 938)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)
    #Bullet Movement
    if bulletY <= 0:
        bulletY = 500
        bullet_state = "ready"
    if bullet_state == "fire":
        fire(bulletX,bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)  # coordinate change of player
    show_score(textX,textY)
    pygame.display.update()