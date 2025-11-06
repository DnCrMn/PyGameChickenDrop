import pygame 
import sys
import random

pygame.init()

# Initialize the screen's size
width = 800
height = 600
size = (width, height)

black = (0, 0, 0)

# Set screen size and window title
screen = pygame.display.set_mode(size) # Set the screen size
pygame.display.set_caption("Chicken Click Game")

nuke = pygame.image.load("assets/images/nuke.png")

iterator = 0
maxNukesOnScreen = 5
startX = [] # Starting x position of the nuke
startY = [] # Starting y position of the nuke
speed = [] # How fast the nuke falls

# Initialize nukes
while iterator < maxNukesOnScreen:
    startX.append(random.randint(0, width - nuke.get_width() + 1))
    startY.append(0 - random.randint(nuke.get_height(), nuke.get_height() * 2))
    speed.append(0.5)
    iterator += 1

# Initialize Play again font
bigFont = pygame.font.SysFont(None, 200)
playAgainText = bigFont.render("Play Again?", True, (0, 200, 0))
playAgainX = width/2 - playAgainText.get_rect().width/2

# Initialize Yes/No Text
smallFont = pygame.font.SysFont(None, 100)
yesText = smallFont.render("YES", True, (0, 200, 0))
yesX = width/4 - yesText.get_rect().width/2
noText = smallFont.render("NO", True, (0, 200, 0))
noX = width - width/4 - yesText.get_rect().width/2

# Game mode variables
replayScreen = False
gameOver = False


# Game Loop
while gameOver == False:
    # Check for game quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           gameOver = True 
    
    # -- Input checking goes here --
    coords = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed()[0]:
        if replayScreen == False:

            iterator = 0
            while iterator < maxNukesOnScreen:
                if coords[0] >= startX[iterator] and coords[0] <= startX[iterator] + nuke.get_width() and coords[1] >= startY[iterator] and coords[1] <= startY[iterator] + nuke.get_height():
                    startX[iterator] = random.randint(0,width - nuke.get_width() + 1)
                    startY[iterator] = 0 - random.randint(nuke.get_height(), nuke.get_height() * 2)
                    speed[iterator] = 0.5
                    break
                iterator += 1
        else:
            if coords[0] > yesX and coords[0] < yesX + yesText.get_rect().width and coords[1] > 450 and coords[1] < 450 + yesText.get_rect().height:
                iterator = 0
                while iterator < maxNukesOnScreen:
                    startX[iterator] = random.randint(0,width - nuke.get_width() + 1)
                    startY[iterator] = 0 - random.randint(nuke.get_height(), nuke.get_height() * 2)
                    speed[iterator] = 0.5
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
            startY[iterator] += speed[iterator]
            iterator += 1

    # -- Rendering goes here --
    # Draw Nuke
    if replayScreen == False:
        screen.fill(black)
        iterator = 0
        while iterator < maxNukesOnScreen:
            screen.blit(nuke, (startX[iterator], startY[iterator])) 
            iterator += 1
    else:
        screen.fill((200, 0, 0))

        screen.blit(playAgainText, (playAgainX, 150))  
        screen.blit(yesText, (yesX, 450))  
        screen.blit(noText, (noX, 450))  

    pygame.display.flip() # Update screen

pygame.display.quit()

