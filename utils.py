import pygame
import os
pygame.font.init()

def scaleImage(image, factor):
    newSize = round(image.get_width() * factor), round(image.get_height() * factor)
    return pygame.transform.scale(image, newSize)

def rotateImage(window, image, topLeft, angle):
    rotatedImage = pygame.transform.rotate(image, angle)
    newPosition = rotatedImage.get_rect(center = image.get_rect(topleft = topLeft).center)
    window.blit(rotatedImage, newPosition.topleft)

def getRotatedImage(image, angle):
    rotatedImage = pygame.transform.rotate(image, angle)
    return rotatedImage

def setTextTopCenter(window, font, text):
    render = font.render(text, 1, (255,255,255))
    window.blit(render, (140,5))

def setTextCenter(window, font, text):
    render = font.render(text, 1, (255,255,255))
    window.blit(render, (window.get_width() / 2 - render.get_width() / 2, window.get_height() / 2 - render.get_height() / 2))

def handleCollisions(window, font, manageGame, trackMask, finishMask, finishPos, finishInvalidIndex, finishInvalid, player1Car, player2Car = None, computerCar = None, multiplayerMode = False):
    #Runs if Cars colliding with borders
    if player1Car.collide(trackMask) != None:
        player1Car.bounceCar()
    if multiplayerMode:
        if player2Car.collide(trackMask) != None:
            player2Car.bounceCar()

    #Player 1 car touch finish line
    player1Finishes = player1Car.collide(finishMask, *finishPos)
    if player1Finishes != None:
        if player1Finishes[finishInvalidIndex] == finishInvalid:
            player1Car.bounceCar()
        else:
            manageGame.nextLevel()
            if not manageGame.gameFinished():
                if manageGame.level == 2:
                    setTextTopCenter(window, font, f"Level Finished! Player 1 WON.")
                else:
                    setTextCenter(window, font, f"Level Finished! Player 1 WON.")
                pygame.display.update()
                pygame.time.wait(2500)
            else:
                setTextCenter(window, font, f"All Tracks Cleared!, GAME OVER")
                pygame.display.update()
                pygame.time.wait(3000)
                pygame.quit()
                os.system("python3 main.py")
            player1Car.resetGame()
            if multiplayerMode:
                player2Car.resetGame()
            else:
                computerCar.nextLevel(manageGame.level)

    #Player 2 car touch finish line
    if multiplayerMode:
        player2Finishes = player2Car.collide(finishMask, *finishPos)
        if player2Finishes != None:
            if player2Finishes[finishInvalidIndex] == finishInvalid:
                player2Car.bounceCar()
            else:
                manageGame.nextLevel()
                if not manageGame.gameFinished():
                    if manageGame.level == 2:
                        setTextTopCenter(window, font, f"Level Finished! Player 2 WON.")
                    else:
                        setTextCenter(window, font, f"Level Finished! Player 2 WON.")
                    pygame.display.update()
                    pygame.time.wait(2500)
                else:
                    setTextCenter(window, font, f"All Tracks Cleared!, GAME OVER")
                    pygame.display.update()
                    pygame.time.wait(3000)
                    pygame.quit()
                    os.system("python3 main.py")
                player2Car.resetGame()
                player1Car.resetGame()
    
    if not multiplayerMode:
        if computerCar.collide(finishMask, *finishPos) != None:
            if manageGame.level == 2:
                setTextTopCenter(window, font, f"Level Lost! Computer WON!")
            else:
                setTextCenter(window, font, f"Level Lost! Computer WON!")
            pygame.display.update()
            pygame.time.wait(2000)
            if manageGame.level == 3:
                computerCar.resetGame(levelNumber=True)
                player1Car.resetGame(levelNumber=True)
            else:
                computerCar.resetGame()
            manageGame.resetLevel()

    if manageGame.level == 2 and manageGame.currentLevelLayout == 1:
        manageGame.currentLevelLayout += 1
        from LevelTwo import startLevel2
        if multiplayerMode:
            startLevel2(manageGame, multiplayerMode, [player1Car.carImage, player2Car.carImage])
        else:
            startLevel2(manageGame, multiplayerMode, [player1Car.carImage, computerCar.carImage])
    elif manageGame.level == 3 and manageGame.currentLevelLayout == 2:
        manageGame.currentLevelLayout += 1
        from LevelThree import startLevel3
        if multiplayerMode:
            startLevel3(manageGame, multiplayerMode, [player1Car.carImage, player2Car.carImage])
        else:
            startLevel3(manageGame, multiplayerMode, [player1Car.carImage, computerCar.carImage])


def movePlayerCars(player1Car = None, player2Car = None, multiplayerMode = False):
    keys = pygame.key.get_pressed()
    player1Moved = False

    #Player 1 Car Controls
    if keys[pygame.K_UP]:
        player1Moved = True
        player1Car.moveForward()
    if keys[pygame.K_DOWN]:
        player1Moved = True
        player1Car.moveBackward()
    if keys[pygame.K_LEFT]:
        player1Car.rotate(left=True)
    if keys[pygame.K_RIGHT]:
        player1Car.rotate(right=True)
    
    if not player1Moved:
        player1Car.reduceSpeed()

    #Player 2 Car Controls
    if multiplayerMode:
        player2Moved = False
        if keys[pygame.K_w]:
            player2Moved = True
            player2Car.moveForward()
        if keys[pygame.K_s]:
            player2Moved = True
            player2Car.moveBackward()
        if keys[pygame.K_a]:
            player2Car.rotate(left=True)
        if keys[pygame.K_d]:
            player2Car.rotate(right=True)
        
        if not player2Moved:
            player2Car.reduceSpeed()

#Code for making path for computer car
# if event.type == pygame.MOUSEBUTTONDOWN:
#     position = pygame.mouse.get_pos()
#     computerCar.path.append(position)

    