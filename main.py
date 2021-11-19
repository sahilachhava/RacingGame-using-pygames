import pygame
import time
from utils import scaleImage
pygame.font.init()

#Loading Assets
BLACK_BG = pygame.image.load("Assets/bg-black.jpg")
LOGO = scaleImage(pygame.image.load("Assets/logo.png"), 0.8)
LOGO_CARIMAGE = scaleImage(pygame.image.load("Assets/car-image.png"), 0.5)
ARROW = scaleImage(pygame.image.load("Assets/arrow.png"), 0.1)

HEIGHT, WIDTH = 500, 800

#Setting Window Size, Title & Global variables
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Game")
MAIN_FONT = pygame.font.Font("Assets/custom-font/SpaceMission.otf", 42)
REGULAR_FONT = pygame.font.Font("Assets/custom-font/SpaceMission.otf", 32)

FPS = 60
runGame = True
clock = pygame.time.Clock()
optionSelectionFlag = False
mainPageLayout = [(BLACK_BG, (0,0)), (LOGO, (225, 0)), (LOGO_CARIMAGE, (225, 200))]

class ManageGame:
    LEVELS = 3

    def __init__(self, level = 1):
        self.level = level
        self.started = False
        self.levelStartTime = 0

    def nextLevel(self):
        self.level += 1
        self.started = False

    def startLevel(self):
        self.started = True
        self.levelStartTime = time.time()

    def getLevelTime(self):
        if not self.started:
            return 0
        return  round(time.time() - self.levelStartTime)

    def gameFinished(self):
        return self.level > self.LEVELS

    def resetGame(self):
        self.level = 1
        self.started = False
        self.levelStartTime = 0

manageGame = ManageGame() 

def drawImages(optionSelectionFlag):
    for image, position in mainPageLayout:
        WINDOW.blit(image, position)

    multiplayerText = REGULAR_FONT.render(f"Multiplayer", 1, (255, 255, 255))
    WINDOW.blit(multiplayerText, (300, HEIGHT - multiplayerText.get_height() - 80))

    computerText = REGULAR_FONT.render(f"VS Computer", 1, (255,255,255))
    WINDOW.blit(computerText, (300, HEIGHT - computerText.get_height() - 40))

    if not optionSelectionFlag:
        WINDOW.blit(ARROW, (240, HEIGHT - multiplayerText.get_height() - 85))
    else:
        WINDOW.blit(ARROW, (240, HEIGHT - computerText.get_height() - 45))

    pygame.display.update()

while runGame:
    clock.tick(FPS) #60 Frame per second
    WINDOW.fill((0,0,0)) #Making background black

    drawImages(optionSelectionFlag)
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN]:
            optionSelectionFlag = True
    if keys[pygame.K_UP]:
        optionSelectionFlag = False
    if keys[pygame.K_RETURN]:
        from SelectCar import selectCar
        selectCar(manageGame, optionSelectionFlag)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runGame = False
            break
        
pygame.quit()