import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Create the screen layout (width, height)
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("background.png")

# Title and icon
pygame.display.set_caption("Space Invaders Main")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("player.png")
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change= []
no_of_enemy = 16

for i in range(no_of_enemy):
    enemyImg.append(pygame.image.load("enemy.png")) 
    enemyX.append(random.randint(0, 705)) 
    enemyY.append(random.randint(50, 150)) 
    enemyX_change.append(0.4) 
    enemyY_change.append(40) 


# enemyImg = pygame.image.load("enemy.png")
# enemyX = random.randint(0, 705)
# enemyY = random.randint(50, 150)
# enemyX_change = 0.2
# enemyY_change = 40

# Bullet
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletY_change = 1.5
bullet_state = "ready"  # "ready" means the bullet is not visible; "fire" means the bullet is moving

#score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)
textX = 10
textY = 10
def show_score(x,y):
    score = font.render("Score: "+str(score_value),True,(255,255,255))
    screen.blit(score, (x, y))

#game over text
# game_over_text
over_font = pygame.font.Font('freesansbold.ttf',62)
def game_over_text():
    over_text = over_font.render("GAME OVER",True,(255,255,255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):  
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10)) #center bullet


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(bulletX - enemyX, 2)) + (math.pow(bulletY - enemyY, 2)))
    #10 class ko distance formula
    return distance < 20
    



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
            # print ("A keystroke is pressed")
            if event.key == pygame.K_LEFT:
                # print("left arrow is pressed")
                playerX_change = -0.3
            if event.key == pygame.K_RIGHT:
                # print("Right arrow is pressed")
                playerX_change = 0.3
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":  # Fire the bullet only if it is ready
                    bulletX = playerX  # Capture the current  coordinate of playerX when firing
                    fire_bullet(bulletX, bulletY)
                    # print("FIRE")

                    
        # Key release event
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                # print("key stoke is Realeased")
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
    for i in range(no_of_enemy):

        #game over
        if enemyY[i]> playerY-10:
            for j in range(no_of_enemy):
                #move all enemy out of the screen
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 30:
            # print("enemy left side strike")
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            # print("enemy Right side strike")
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]
        
            #colllisoon betwen enemy and bullet
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480  # Reset bullet position after collision
            bullet_state = "ready"  # Set bullet state back to "ready"
            score_value += 1  # Increment the score
            print("Score:", score_value)  # Debugging score output
            
            # Respawn the enemy at a random location
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # enemyX += enemyX_change
    # if enemyX <= 0:
    #     # print("enemy left side strike")
    #     enemyX_change = 0.2
    #     enemyY += enemyY_change
    # elif enemyX >= 736:
    #     # print("enemy Right side strike")
    #     enemyX_change = -0.2
    #     enemyY += enemyY_change



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

    # #colllisoon betwen enemy and bullet
    # collision = isCollision(enemyX, enemyY, bulletX, bulletY)
    # if collision:
    #     bulletY = 480
    #     bullet_state = "ready"
    #     score +=1
    #     print("score: ",score)
    #     enemyX = random.randint(0, 705)
    #     enemyY = random.randint(50, 150)


    player(playerX, playerY)
    show_score(textX,textY) 
    pygame.display.update()
#while ends here

pygame.quit()    
