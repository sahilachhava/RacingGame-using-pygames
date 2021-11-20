import pygame
import math
pygame.font.init()
from utils import rotateImage, getRotatedImage

class AbstractCar:
    def __init__(self, maxVelocity, rotationVelocity, carImage, window):
        self.carImage = carImage
        self.velocity = 0
        self.angle = 270
        self.xPos, self.yPos = self.START_POS
        self.maxVelocity = maxVelocity
        self.rotationVelocity = rotationVelocity
        self.acceleration = 0.02
        self.screenWindow = window

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
        return pygame.mask.from_surface(getRotatedImage(self.carImage, self.angle))

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

    def resetGame(self, levelNumber=False):
        self.xPos, self.yPos = self.START_POS
        self.angle = 270
        self.velocity = 0
        if levelNumber:
            self.angle = 0

    def drawCar(self):
        rotateImage(self.screenWindow, self.carImage, (self.xPos, self.yPos), self.angle)

class Player1Car(AbstractCar):
    #startPosition = (250, 450) for L2 Track
    def __init__(self, maxVelocity, rotationVelocity, carImage, startPosition, window):
        self.START_POS = startPosition
        super().__init__(maxVelocity, rotationVelocity, carImage, window)

    def reduceSpeed(self):
        self.velocity = max(self.velocity - self.acceleration / 2, 0)
        self.moveCar()

    def bounceCar(self):
        tempVelocity = self.velocity
        self.velocity = -self.velocity
        self.velocity = (tempVelocity / 1.5)
        self.moveCar()

class Player2Car(AbstractCar):
    def __init__(self, maxVelocity, rotationVelocity, carImage, startPosition, window):
        self.START_POS = startPosition
        super().__init__(maxVelocity, rotationVelocity, carImage, window)

    def reduceSpeed(self):
        self.velocity = max(self.velocity - self.acceleration / 2, 0)
        self.moveCar()

    def bounceCar(self):
        tempVelocity = self.velocity
        self.velocity = -self.velocity
        self.velocity = (tempVelocity / 1.5)
        self.moveCar()

class ComputerCar(AbstractCar):
    def __init__(self, maxVelocity, rotationVelocity, carImage, startPosition, window, path=[]):
        self.START_POS = startPosition
        super().__init__(maxVelocity, rotationVelocity, carImage, window)
        self.path = path
        self.currentPoint = 0
        self.velocity = maxVelocity

    def drawPoints(self):
        for point in self.path:
            pygame.draw.circle(self.screenWindow, (255,0,0), point, 5)

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
        rect = pygame.Rect(self.xPos, self.yPos, self.carImage.get_width(), self.carImage.get_height())
        if rect.collidepoint(*target):
            self.currentPoint += 1

    def moveCar(self):
        if self.currentPoint >= len(self.path):
            return
        
        self.calculateAngle()
        self.updatePathPoints()
        super().moveCar()

    def resetGame(self, levelNumber=False):
        super().resetGame(levelNumber)
        self.currentPoint = 0
        self.velocity = self.maxVelocity
        if levelNumber:
            self.angle = 0

    def nextLevel(self, level):
        self.resetGame()
        #self.velocity = self.maxVelocity  + (level - 1) * 0.2
        self.currentPoint = 0