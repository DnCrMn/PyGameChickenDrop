import pygame 
import random
import time

pygame.init()

# Initialize the screen's size
width = 800
height = 600
size = (width, height)

black = (0, 0, 0)

# Set screen size and window title
screen = pygame.display.set_mode(size) # Set the screen size
pygame.display.set_caption("Chicken Click Game")

# Set up background and sprites
nuke = pygame.image.load("assets/images/nuke.png")
powerUpIMG = pygame.image.load("assets/images/power_up.png")
backgroundImageNormal = pygame.image.load("assets/images/bg_normal.png")
backgroundImageGameOver = pygame.image.load("assets/images/bg_game_over.png")

# Initilize nuke variables
maxNukesOnScreen = 5 # Maximum number of nukes on the screen
startX = [] # Starting x position of the nuke
startY = [] # Starting y position of the nuke
nukeSpeed = 1 # Base nuke speed
previousSpeed = 1 # Nuke's speed before changing it 
speed = [] # How fast the nuke falls

# Initialize power up variables
powerUpStartX = 0                 # Starting x position of the power up
powerUpStartY = 0                 # Starting y position of the power up
powerUpTimer = 0                  # Timer for the power up
effectTimer = 0                   # Timer for the power up's effect  
powerUpLimit = 3
effectLimit = 2
enablePowerUp = False             # Enables power up to fall from the top of the screen
showPowerUp = False               # Bool that shows the power up in draw

score = 0 # Current score
timerStart = time.time()

# Initialize Play again font
bigFont = pygame.font.SysFont(None, 200)
playAgainText = bigFont.render("Play Again?", True, (0, 0, 0))
playAgainX = width/2 - playAgainText.get_rect().width/2

# Initialize Yes/No Text
smallFont = pygame.font.SysFont(None, 100)
yesText = smallFont.render("YES", True, (0, 0, 0))
yesX = width/4 - yesText.get_rect().width/2
noText = smallFont.render("NO", True, (0, 0, 0))
noX = width - width/4 - yesText.get_rect().width/2

# Initialize score font
scoreFont = pygame.font.SysFont(None, 50)

# Game mode variables
replayScreen = False
gameOver = False

# Powers up the player
def PowerUpPlayer():
    global enablePowerUp, showPowerUp, previousSpeed, nukeSpeed, timerStart
    enablePowerUp = True
    showPowerUp = False
    previousSpeed = nukeSpeed
    nukeSpeed = nukeSpeed / 2
    timerStart = time.time()

def ResetEffect():
    global nukeSpeed, enablePowerUp
    nukeSpeed = previousSpeed
    enablePowerUp = False

def TimePowerUp():
    global effectTimer
    effectTimer = time.time() - timerStart

    if effectTimer > effectLimit:
        ResetEffect()

# Set up nukes in the screen
iterator = 0
while iterator < maxNukesOnScreen:
    startX.append(random.randint(0, width - nuke.get_width() + 1))
    startY.append(0 - random.randint(nuke.get_height(), nuke.get_height() * 2))
    speed.append(nukeSpeed)
    iterator += 1

# Game Loop
while gameOver == False:
    # Check for game quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           gameOver = True 

    print(f"Nuke Speed: {nukeSpeed}")
    
    # -- Input checking goes here --
    coords = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed()[0]:
        if replayScreen == False:

            iterator = 0
            while iterator < maxNukesOnScreen:
                if coords[0] >= startX[iterator] and coords[0] <= startX[iterator] + nuke.get_width() and coords[1] >= startY[iterator] and coords[1] <= startY[iterator] + nuke.get_height():
                    score += 1

                    # Increase speed every 10 points
                    if score % 10 == 0 and score > 0:
                        nukeSpeed += 0.5

                    # Spawn power up every 25 points
                    if score % 25 == 0 and score > 0:
                        showPowerUp = True
                        powerUpStartX = random.randint(0, width - powerUpIMG.get_width())
                        powerUpStartY = random.randint(0, height - powerUpIMG.get_height())
                        timerStart = time.time()

                    startX[iterator] = random.randint(0,width - nuke.get_width() + 1)
                    startY[iterator] = 0 - random.randint(nuke.get_height(), nuke.get_height() * 2)
                    speed[iterator] = nukeSpeed 

                    break
                iterator += 1
                # Power-up click
                if showPowerUp:
                    if (powerUpStartX <= coords[0] <= powerUpStartX + powerUpIMG.get_width() and
                        powerUpStartY <= coords[1] <= powerUpStartY + powerUpIMG.get_height()):
                        PowerUpPlayer()
        else:
            if coords[0] > yesX and coords[0] < yesX + yesText.get_rect().width and coords[1] > 450 and coords[1] < 450 + yesText.get_rect().height:
                # Reset variables
                showPowerUp = False
                enablePowerUp = False
                score = 0
                nukeSpeed = 1 
                iterator = 0

                while iterator < maxNukesOnScreen:
                    startX[iterator] = random.randint(0,width - nuke.get_width() + 1)
                    startY[iterator] = 0 - random.randint(nuke.get_height(), nuke.get_height() * 2)
                    speed[iterator] = nukeSpeed 
                    iterator += 1
                replayScreen = False
            if coords[0] > noX and coords[0] <= noX + noText.get_rect().width and coords[1] > 450 and coords[1] < 450 + noText.get_rect().height:
                gameOver = True

    # -- Updates go here --
    # Spawn nuke
    if replayScreen == False:
        iterator = 0
        while iterator < maxNukesOnScreen:
            if startY[iterator] + nuke.get_height() > height:
                replayScreen = True
                break
            startY[iterator] += nukeSpeed 
            iterator += 1

    # Timer for power up
    if enablePowerUp:
        TimePowerUp()

    # Time how long the power up will show in the screen
    if showPowerUp:
        powerUpTimer = time.time() - timerStart

        if powerUpTimer > powerUpLimit:
            showPowerUp =  False
            enablePowerUp = False
    

    # -- Rendering goes here --
    if replayScreen == False:
        # Draw Nuke
        screen.blit(backgroundImageNormal, (0,0))
        iterator = 0
        while iterator < maxNukesOnScreen:
            screen.blit(nuke, (startX[iterator], startY[iterator])) 
            iterator += 1

        # Draw Power Up
        if showPowerUp:
            screen.blit(powerUpIMG, (powerUpStartX, powerUpStartY))

        # Draw score
        scoreText = scoreFont.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(scoreText, (620, 570))
    else:
        screen.blit(backgroundImageGameOver, (0,0))

        # Draw replay prompt
        screen.blit(playAgainText, (playAgainX, 150))  
        screen.blit(yesText, (yesX, 450))  
        screen.blit(noText, (noX, 450))  

    pygame.display.flip() # Update screen

pygame.display.quit()

