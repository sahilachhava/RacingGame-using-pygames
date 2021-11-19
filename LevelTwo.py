import pygame
from utils import scaleImage, handleCollisions, getRotatedImage, setTextTopCenter, movePlayerCars
from Cars import Player1Car, Player2Car, ComputerCar
pygame.font.init()

#Drawing Level 2 Race Track & Cars
def drawLevel(window, manageGame, raceCar1, raceCar2, levelLayouts, displayFont):
    for image, position in levelLayouts:
        window.blit(image, position)

    levelText = displayFont.render(f"Level {manageGame.level}", 1, (255,255,255))
    window.blit(levelText, (200, 575))

    timeText = displayFont.render(f"Time {manageGame.getLevelTime()}s", 1, (255,255,255))
    window.blit(timeText, (200 + levelText.get_width() + 25, 575))

    #Drawing race cars on track
    raceCar1.drawCar()
    raceCar2.drawCar()

    pygame.display.update() #Updating layouts on screen window

#Game level will start from here
def startLevel2(manageGame, multiplayerMode, carImages):
    #Loading Assets
    TRACK = pygame.image.load("Assets/Tracks/L2-Track.jpg")
    TRACK_BORDER = pygame.image.load("Assets/Tracks/L2-Track-Border.png")
    TRACK_MASK = pygame.mask.from_surface(TRACK_BORDER)
    FINISH = scaleImage(getRotatedImage(pygame.image.load("Assets/finish-line.png"), 90), 0.7)
    FINISH_MASK = pygame.mask.from_surface(FINISH)
    FINISH_POSITION = (240, 490)

    #Setting Window Size, Title & Global Variables
    WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Racing Game - Level 2")

    FPS = 60
    MAIN_FONT = pygame.font.SysFont("comicsans", 42)
    REGULAR_FONT = pygame.font.SysFont("comicsans", 32)
    clock = pygame.time.Clock()
    levelLayouts = [(TRACK, (0,0)), (FINISH, FINISH_POSITION), (TRACK_BORDER, (0,0))]
    COMPUTER_LEVEL1_PATH = [(412, 515), (505, 447), (510, 307), (509, 169), (459, 62), (326, 76), (124, 65), (59, 152), (109, 250), (215, 195), (296, 305), (387, 195), (426, 311), (409, 422), (258, 357), (95, 339), (76, 488), (233, 526)]
    PLAYER_LEVEL1_MAX_SPEED = 2
    PLAYER_LEVEL1_MAX_ROTATION = 5
    COMPUTER_LEVEL1_MAX_SPEED = 1.4
    COMPUTER_LEVEL1_MAX_ROTATION = 5
    LEVEL1_CAR1_START_POSITION = (280, 495)
    LEVEL1_CAR2_START_POSITION = (280, 520)

    runGame = True
    player1Car = Player1Car(PLAYER_LEVEL1_MAX_SPEED, PLAYER_LEVEL1_MAX_ROTATION, carImages[0], LEVEL1_CAR1_START_POSITION, WINDOW)
    player2Car = Player2Car(PLAYER_LEVEL1_MAX_SPEED, PLAYER_LEVEL1_MAX_ROTATION, carImages[1], LEVEL1_CAR2_START_POSITION, WINDOW)
    computerCar = ComputerCar(COMPUTER_LEVEL1_MAX_SPEED, COMPUTER_LEVEL1_MAX_ROTATION, carImages[1], LEVEL1_CAR2_START_POSITION, WINDOW, COMPUTER_LEVEL1_PATH)

    while runGame:
        clock.tick(FPS) #60 Frame per second (FPS)
        
        if not multiplayerMode:
            drawLevel(WINDOW, manageGame, player1Car, computerCar, levelLayouts, REGULAR_FONT) #Calling Draw Function
        else:
            drawLevel(WINDOW, manageGame, player1Car, player2Car, levelLayouts, REGULAR_FONT) #Calling Draw Function

        #Checking level is started or not
        while not manageGame.started:
            setTextTopCenter(WINDOW, REGULAR_FONT, f"Press any key to start level {manageGame.level}!")
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
            handleCollisions(WINDOW, REGULAR_FONT, manageGame, TRACK_MASK, FINISH_MASK, FINISH_POSITION, 0, 13, player1Car, computerCar=computerCar, multiplayerMode=multiplayerMode)
        else:
            movePlayerCars(player1Car=player1Car, player2Car=player2Car, multiplayerMode = True)
            handleCollisions(WINDOW, MAIN_FONT, manageGame, TRACK_MASK, FINISH_MASK, FINISH_POSITION, 0, 13, player1Car, player2Car=player2Car, multiplayerMode=multiplayerMode)

        #If user click close btn of window it will quit the game
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                runGame = False
                break

    pygame.quit()
