import pygame

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

def setTextCenter(window, font, text):
    render = font.render(text, 1, (255,255,255))
    window.blit(render, (window.get_width() / 2 - render.get_width() / 2, window.get_height() / 2 - render.get_height() / 2))