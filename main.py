from os import path
import pygame
import time
import math
pygame.font.init()

from pygame.version import ver
from utils import scaleImage, rotateImage, getRotatedImage, setTextCenter

#Loading Assets
TRACK = pygame.image.load("Assets/Tracks/temp-track.png")
TRACK_BORDER = pygame.image.load("Assets/Tracks/temp-track-border.png")
TRACK_MASK = pygame.mask.from_surface(TRACK_BORDER)
GRASS = scaleImage(pygame.image.load("Assets/grass.jpg"), 2.5)
FINISH = scaleImage(getRotatedImage(pygame.image.load("Assets/finish-line.png"), 90), 0.7)
FINISH_MASK = pygame.mask.from_surface(FINISH)
FINISH_POSITION = (200, 250)
RED_CAR = scaleImage(pygame.image.load("Assets/Cars/red-car.png"), 0.04)
BLUE_CAR = scaleImage(pygame.image.load("Assets/Cars/blue-car.png"), 0.04)
BLACK_CAR = scaleImage(pygame.image.load("Assets/Cars/black-car.png"), 0.04)

#Setting Window Size & Title
WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Game")

FPS = 60
MAIN_FONT = pygame.font.SysFont("comicsans", 42)
REGULAR_FONT = pygame.font.SysFont("comicsans", 32)
runGame = True
clock = pygame.time.Clock()
allImages = [(GRASS, (0,0)),(TRACK, (0,0)), (FINISH, FINISH_POSITION), (TRACK_BORDER, (0,0))]
PATH = [(325, 286), (470, 304), (574, 277), (607, 154), (452, 79), (280, 108), (95, 124), (83, 272), (206, 289)]

class ManageGame:
    LEVELS = 2

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

class AbstractCar:
    def __init__(self, maxVelocity, rotationVelocity):
        self.carImg = self.carImg
        self.velocity = 0
        self.angle = 270
        self.xPos, self.yPos = self.START_POS
        self.maxVelocity = maxVelocity
        self.rotationVelocity = rotationVelocity
        self.acceleration = 0.02

    def rotate(self, left = False, right = False):
        if left:
            self.angle += self.rotationVelocity
        elif right:
            self.angle -= self.rotationVelocity

    def moveForward(self):
        self.velocity = min(self.velocity + self.acceleration, self.maxVelocity)
        self.moveCar()

    def moveBackward(self):
        self.velocity = max(self.velocity - self.acceleration, -self.maxVelocity / 2)
        self.moveCar()

    def getCarMask(self):
        return pygame.mask.from_surface(getRotatedImage(self.carImg, self.angle))

    def moveCar(self):
        radians = math.radians(self.angle)
        verticalVelocity = math.cos(radians) * self.velocity
        horizontalVelocity = math.sin(radians) * self.velocity

        self.xPos -= horizontalVelocity
        self.yPos -= verticalVelocity

    def collide(self, mask, xPos = 0, yPos = 0):
        offset = (int(self.xPos - xPos), int(self.yPos - yPos))
        collisionPoint = mask.overlap(self.getCarMask(), offset)
        return collisionPoint

    def resetGame(self):
        self.xPos, self.yPos = self.START_POS
        self.angle = 270
        self.velocity = 0

    def drawCar(self):
        rotateImage(WINDOW, self.carImg, (self.xPos, self.yPos), self.angle)

class PlayerCar(AbstractCar):
    carImg = RED_CAR
    START_POS = (240, 248) #for L1 Track
    #START_POS = (250, 450) for L2 Track

    def reduceSpeed(self):
        self.velocity = max(self.velocity - self.acceleration / 2, 0)
        self.moveCar()

    def bounceCar(self):
        self.velocity = -self.velocity
        self.moveCar()

class ComputerCar(AbstractCar):
    carImg = BLUE_CAR
    START_POS = (240, 285) #for L1 Track

    def __init__(self, maxVelocity, rotationVelocity, path=[]):
        super().__init__(maxVelocity, rotationVelocity)
        self.path = path
        self.currentPoint = 0
        self.velocity = maxVelocity

    def drawPoints(self):
        for point in self.path:
            pygame.draw.circle(WINDOW, (255,0,0), point, 5)

    def drawCar(self):
        super().drawCar()
        #self.drawPoints()

    def calculateAngle(self):
        targetX, targetY = self.path[self.currentPoint]
        xDiff = targetX - self.xPos
        yDiff = targetY - self.yPos

        if yDiff == 0:
            desiredRadianAngle = math.pi / 2
        else:
            desiredRadianAngle = math.atan(xDiff / yDiff)

        if targetY > self.yPos:
            desiredRadianAngle += math.pi

        diffInAngle = self.angle - math.degrees(desiredRadianAngle)
        if diffInAngle >= 180:
            diffInAngle -= 360

        if diffInAngle > 0:
            self.angle -= min(self.rotationVelocity, abs(diffInAngle))
        else:
            self.angle += min(self.rotationVelocity, abs(diffInAngle))

    def updatePathPoints(self):
        target = self.path[self.currentPoint]
        rect = pygame.Rect(self.xPos, self.yPos, self.carImg.get_width(), self.carImg.get_height())
        if rect.collidepoint(*target):
            self.currentPoint += 1

    def moveCar(self):
        if self.currentPoint >= len(self.path):
            return
        
        self.calculateAngle()
        self.updatePathPoints()
        super().moveCar()

    def resetGame(self):
        super().resetGame()
        self.currentPoint = 0

    def nextLevel(self, level):
        self.resetGame()
        self.velocity = self.maxVelocity  + (level - 1) * 0.2
        self.currentPoint = 0

playerCar = PlayerCar(2, 2)
computerCar = ComputerCar(1, 2, PATH)
manageGame = ManageGame() 

def movePlayer():
    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_UP]:
        moved = True
        playerCar.moveForward()
    if keys[pygame.K_DOWN]:
        moved = True
        playerCar.moveBackward()
    if keys[pygame.K_LEFT]:
        playerCar.rotate(left=True)
    if keys[pygame.K_RIGHT]:
        playerCar.rotate(right=True)
    
    if not moved:
        playerCar.reduceSpeed()

def drawImages():
    for image, position in allImages:
        WINDOW.blit(image, position)

    levelText = REGULAR_FONT.render(f"Level {manageGame.level}", 1, (255,255,255))
    WINDOW.blit(levelText, (10, HEIGHT - levelText.get_height() - 10))

    speedText = REGULAR_FONT.render(f"Speed {abs(round(playerCar.velocity, 1))} px/s", 1, (255,255,255))
    WINDOW.blit(speedText, (100, HEIGHT - levelText.get_height() - 10))

    timeText = REGULAR_FONT.render(f"Time {manageGame.getLevelTime()}s", 1, (255,255,255))
    WINDOW.blit(timeText, (260, HEIGHT - levelText.get_height() - 10))

    playerCar.drawCar()
    computerCar.drawCar()
    pygame.display.update()

def handleCollision():
    if playerCar.collide(TRACK_MASK) != None:
        playerCar.bounceCar()

    playerFinishPoint = playerCar.collide(FINISH_MASK, *FINISH_POSITION)
    if playerFinishPoint != None:
        if playerFinishPoint[0] == 13:
            playerCar.bounceCar()
        else:
            manageGame.nextLevel()
            if not manageGame.gameFinished():
                setTextCenter(WINDOW, MAIN_FONT, f"You won!")
                pygame.display.update()
                pygame.time.wait(2000)
            playerCar.resetGame()
            computerCar.nextLevel(manageGame.level)

    if computerCar.collide(FINISH_MASK, *FINISH_POSITION) != None:
        setTextCenter(WINDOW, MAIN_FONT, f"Computer won!")
        pygame.display.update()
        pygame.time.wait(2000)
        manageGame.resetGame()
        playerCar.resetGame()
        computerCar.resetGame()

    if playerCar.collide(computerCar.getCarMask()) != None:
        print("player hit computer")


while runGame:
    clock.tick(FPS) #60 Frame per second
    drawImages()

    while not manageGame.started:
        setTextCenter(WINDOW, MAIN_FONT, f"Press any key to start level {manageGame.level}!")
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
            
            if event.type == pygame.KEYDOWN:
                manageGame.startLevel()

    movePlayer()
    computerCar.moveCar()
    handleCollision()

    if manageGame.gameFinished():
        setTextCenter(WINDOW, REGULAR_FONT, f"GAME OVER, You beat the game!")
        pygame.display.update()
        pygame.time.wait(3000)
        manageGame.resetGame()
        playerCar.resetGame()
        computerCar.resetGame()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runGame = False
            break
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     position = pygame.mouse.get_pos()
        #     computerCar.path.append(position)

#print(computerCar.path)
pygame.quit()