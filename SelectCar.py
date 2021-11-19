import pygame
from utils import scaleImage
pygame.font.init()

#Loading Assets
BLACK_BG = pygame.image.load("Assets/bg-black.jpg")
LOGO = scaleImage(pygame.image.load("Assets/logo.png"), 0.65)
LOGO_CARIMAGE = scaleImage(pygame.image.load("Assets/car-image.png"), 0.2)
ARROW = scaleImage(pygame.image.load("Assets/up-arrow.png"), 0.15)

#All Cars
RED_CAR = scaleImage(pygame.image.load("Assets/Cars/red-car.png"), 0.1)
BLUE_CAR = scaleImage(pygame.image.load("Assets/Cars/blue-car.png"), 0.1)
BLACK_CAR = scaleImage(pygame.image.load("Assets/Cars/black-car.png"), 0.1)
GREEN_CAR = scaleImage(pygame.image.load("Assets/Cars/green-car.png"), 0.1)
ORANGE_CAR = scaleImage(pygame.image.load("Assets/Cars/orange-car.png"), 0.1)
WHITE_CAR = scaleImage(pygame.image.load("Assets/Cars/white-car.png"), 0.1)
YELLOW_CAR = scaleImage(pygame.image.load("Assets/Cars/yellow-car.png"), 0.1)

HEIGHT, WIDTH = 500, 800

#Setting Window Size, Title & Global variables
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Game : Select Car")
MAIN_FONT = pygame.font.Font("Assets/custom-font/SpaceMission.otf", 42)
REGULAR_FONT = pygame.font.Font("Assets/custom-font/SpaceMission.otf", 32)
SMALL_FONT = pygame.font.Font("Assets/custom-font/SpaceMission.otf", 16)

FPS = 60
clock = pygame.time.Clock()
mainPageLayout = [(BLACK_BG, (0,0)), (LOGO, (260, 0))]
allCars = [(RED_CAR, (70, 225)), (BLUE_CAR, (170, 225)), (GREEN_CAR, (270, 225)), (YELLOW_CAR, (370, 225)),(ORANGE_CAR, (470, 225)), (WHITE_CAR, (570, 225)), (BLACK_CAR, (670, 225))]
selectedCars = []

def drawImages(carSelectionNumber, playMode):
    for image, position in mainPageLayout:
        WINDOW.blit(image, position)
    
    for image, position in allCars:
        WINDOW.blit(image, position)

    if len(selectedCars) != 2:
        if carSelectionNumber == 0:
            WINDOW.blit(ARROW, (75, 345))
        else:
            WINDOW.blit(ARROW, (75 + carSelectionNumber * 100, 345))
    
    if playMode and len(selectedCars) != 2:
        if len(selectedCars) == 0:
            infoText = REGULAR_FONT.render(f"Player 1: Select your desired car", 1, (255, 255, 255))
        else:
            infoText = REGULAR_FONT.render(f"Player 2: Select your desired car", 1, (255, 255, 255))

        WINDOW.blit(infoText, (130, HEIGHT - infoText.get_height() - 50))
    elif len(selectedCars) == 2:
            infoText = REGULAR_FONT.render(f"Press Enter to start game", 1, (255, 255, 255))
            WINDOW.blit(infoText, (175, HEIGHT - infoText.get_height() - 50))
    else:
        infoText = REGULAR_FONT.render(f"Select your desired car", 1, (255, 255, 255))
        WINDOW.blit(infoText, (200, HEIGHT - infoText.get_height() - 50))

    noteText = SMALL_FONT.render(f"USE [ SPACE ] TO SELECT CAR", 1, (255, 255, 255))
    WINDOW.blit(noteText, (280, HEIGHT - noteText.get_height() - 30))

    pygame.display.update()

def selectCar(manageGame, playMode):
    runGame = True
    carSelectionNumber = 0
    
    while runGame:
        clock.tick(FPS) #60 Frame per second
        WINDOW.fill((0,0,0)) #Making background black

        drawImages(carSelectionNumber, not playMode)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] and carSelectionNumber != 6:
            carSelectionNumber += 1
            pygame.time.wait(250)
        if keys[pygame.K_LEFT] and carSelectionNumber != 0:
            carSelectionNumber -= 1
            pygame.time.wait(250)
        if keys[pygame.K_SPACE] and len(selectedCars) != 2 and not playMode:
            selectedCars.append(scaleImage(allCars[carSelectionNumber][0], 0.4))
            carSelectionNumber = 0
            pygame.time.wait(250)
        if keys[pygame.K_SPACE] and playMode:
            selectedCars.append(scaleImage(allCars[carSelectionNumber][0], 0.4))
            computerCarIndex = (len(allCars) - 1) - carSelectionNumber
            if computerCarIndex == carSelectionNumber:
                computerCarIndex -= 1
            selectedCars.append(scaleImage(allCars[computerCarIndex][0], 0.4))
            pygame.time.wait(250)
        if keys[pygame.K_RETURN] and len(selectedCars) == 2:
            import LevelOne
            LevelOne.startLevel1(manageGame, not playMode, selectedCars)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runGame = False
                break
        
    pygame.quit()