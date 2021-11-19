import pygame
from utils import scaleImage, handleCollisions, setTextCenter, movePlayerCars
from Cars import Player1Car, Player2Car, ComputerCar
pygame.font.init()

#Drawing Level 3 Race Track & Cars
def drawLevel(window, manageGame, raceCar1, raceCar2, levelLayouts, displayFont):
    for image, position in levelLayouts:
        window.blit(image, position)

    levelText = displayFont.render(f"Level {manageGame.level}", 1, (255,255,255))
    window.blit(levelText, (10, 635))

    timeText = displayFont.render(f"Time {manageGame.getLevelTime()}s", 1, (255,255,255))
    window.blit(timeText, (10, 635 + levelText.get_height() + 15))

    #Drawing race cars on track
    raceCar1.drawCar()
    raceCar2.drawCar()

    pygame.display.update() #Updating layouts on screen window

#Game level will start from here
def startLevel3(manageGame, multiplayerMode, carImages):
    #Loading Assets
    TRACK = scaleImage(pygame.image.load("Assets/Tracks/L3-Track.png"), 0.8)
    TRACK_BORDER = scaleImage(pygame.image.load("Assets/Tracks/L3-Track-Border.png"), 0.8)
    TRACK_MASK = pygame.mask.from_surface(TRACK_BORDER)
    GRASS = scaleImage(pygame.image.load("Assets/grass.jpg"), 2.5)
    FINISH = scaleImage(pygame.image.load("Assets/finish-line.png"), 0.8)
    FINISH_MASK = pygame.mask.from_surface(FINISH)
    FINISH_POSITION = (120, 225)

    #Setting Window Size, Title & Global Variables
    WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Racing Game - Level 3")

    FPS = 60
    MAIN_FONT = pygame.font.SysFont("comicsans", 42)
    REGULAR_FONT = pygame.font.SysFont("comicsans", 32)
    clock = pygame.time.Clock()
    levelLayouts = [(GRASS, (0,0)), (TRACK, (0,0)), (FINISH, FINISH_POSITION), (TRACK_BORDER, (0,0))]
    COMPUTER_LEVEL1_PATH = [(142, 89), (47, 113), (46, 224), (43, 373), (120, 511), (242, 615), (352, 625), (367, 474), (519, 440), (542, 639), (668, 619), (652, 465), (617, 315), (388, 314), (399, 230), (615, 219), (655, 79), (420, 55), (236, 93), (233, 280), (204, 376), (167, 311), (159, 242), (149, 231)]
    PLAYER_LEVEL1_MAX_SPEED = 2
    PLAYER_LEVEL1_MAX_ROTATION = 5
    COMPUTER_LEVEL1_MAX_SPEED = 1.5
    COMPUTER_LEVEL1_MAX_ROTATION = 5
    LEVEL1_CAR1_START_POSITION = (165, 175)
    LEVEL1_CAR2_START_POSITION = (130, 175)

    runGame = True
    player1Car = Player1Car(PLAYER_LEVEL1_MAX_SPEED, PLAYER_LEVEL1_MAX_ROTATION, carImages[0], LEVEL1_CAR1_START_POSITION, WINDOW)
    player2Car = Player2Car(PLAYER_LEVEL1_MAX_SPEED, PLAYER_LEVEL1_MAX_ROTATION, carImages[1], LEVEL1_CAR2_START_POSITION, WINDOW)
    computerCar = ComputerCar(COMPUTER_LEVEL1_MAX_SPEED, COMPUTER_LEVEL1_MAX_ROTATION, carImages[1], LEVEL1_CAR2_START_POSITION, WINDOW, COMPUTER_LEVEL1_PATH)
    player1Car.angle = 0
    player2Car.angle = 0
    computerCar.angle = 0

    while runGame:
        clock.tick(FPS) #60 Frame per second (FPS)
        
        if not multiplayerMode:
            drawLevel(WINDOW, manageGame, player1Car, computerCar, levelLayouts, REGULAR_FONT) #Calling Draw Function
        else:
            drawLevel(WINDOW, manageGame, player1Car, player2Car, levelLayouts, REGULAR_FONT) #Calling Draw Function

        #Checking level is started or not
        while not manageGame.started:
            setTextCenter(WINDOW, REGULAR_FONT, f"Press any key to start level {manageGame.level}!")
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break
                
                if event.type == pygame.KEYDOWN:
                    manageGame.startLevel()

        if not multiplayerMode:
            movePlayerCars(player1Car=player1Car, multiplayerMode = False)
            computerCar.moveCar()
            handleCollisions(WINDOW, REGULAR_FONT, manageGame, TRACK_MASK, FINISH_MASK, FINISH_POSITION, 1, 0, player1Car, computerCar=computerCar, multiplayerMode=multiplayerMode)
        else:
            movePlayerCars(player1Car=player1Car, player2Car=player2Car, multiplayerMode = True)
            handleCollisions(WINDOW, MAIN_FONT, manageGame, TRACK_MASK, FINISH_MASK, FINISH_POSITION, 1, 0, player1Car, player2Car=player2Car, multiplayerMode=multiplayerMode)

        #If user click close btn of window it will quit the game
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                runGame = False
                break

    pygame.quit()
