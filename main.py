import pygame
import random

# Initialize Pygame
pygame.init()

# Create the screen layout (width, height)
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("background.png")

# Title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("player.png")
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = pygame.image.load("enemy.png")
enemyX = random.randint(0, 770)
enemyY = random.randint(50, 150)
enemyX_change = 0.2
enemyY_change = 40

# Bullet
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletY_change = 0.5 
bullet_state = "ready"  # "ready" means the bullet is not visible; "fire" means the bullet is moving

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y):
    screen.blit(enemyImg, (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 8, y + 10))

# Game loop
running = True
while running:
    screen.fill((0, 0, 0))  # Fill the screen with black
    screen.blit(background, (0, 0))  # Background image

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
               # Cross button to quuit
            running = False

        # Key press event
        #if key stroke is pressed checked wether its is right or left
        #key down means press keys on keyboard on key board
        #key up means release the keys from keyboards

        if event.type == pygame.KEYDOWN:
            print ("A keystroke is pressed")
            if event.key == pygame.K_LEFT:
                print("left arrow is pressed")
                playerX_change = -0.2
            if event.key == pygame.K_RIGHT:
                print("Right arrow is pressed")
                playerX_change = 0.2
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":  # Fire the bullet only if it is ready
                    bulletX = playerX  # Capture the current  coordinate of playerX when firing
                    fire_bullet(bulletX, bulletY)
                    print("FIRE")

                    
        # Key release event
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                print("key stoke is Realeased")
                playerX_change = 0
                #stop moving or add / sub in coordinates


    # Update player position
    #checking for boundaries of spaceship so it doesnot go out of frame
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:  # 800 - width of player image (64) = 736
        playerX = 736

    # Enemy movement
    enemyX += enemyX_change
    if enemyX <= 0:
        print("enemy left side strike")
        enemyX_change = 0.2
        enemyY += enemyY_change
    elif enemyX >= 736:
        print("enemy Right side strike")
        enemyX_change = -0.2
        enemyY += enemyY_change

    # Bullet movement
    #when bullet state ==  fire 
    #because of function in line no 68
    #now it will change the vlaue of CoordinateY by bulletY_change value
    if bullet_state == "fire":
        # fire_bullet(playerX, bulletY)
        fire_bullet(bulletX, bulletY)  
        # this function is call again because bullet must be continously appear in the screen until it hits
        # bulletY == 0
        bulletY -= bulletY_change

    # Reset the bullet when it goes off the screen
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    enemy(enemyX, enemyY)
    player(playerX, playerY)
    pygame.display.update()

pygame.quit()
