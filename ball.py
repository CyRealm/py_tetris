import math

import pygame
import random
from block import *

class Ball:

    def __init__(self, board):
        self.x = board.GAMEBOARDWIDTH * BLOCKSIZE / 2
        self.y = BLOCKSIZE
        # The angle is stored in degrees form
        self.angle = random.randint(210, 330)
        self.speed = 1
        self.radius = 5

    def update(self, board):
        ySpeed = -math.sin(math.radians(self.angle)) * self.speed
        xSpeed = math.cos(math.radians(self.angle)) * self.speed
        self.x += xSpeed
        self.y += ySpeed
        # Collision with top or bottom of game board
        boardRect = pygame.rect.Rect(0, 0, board.GAMEBOARDWIDTH * BLOCKSIZE, board.GAMEBOARDHEIGHT * BLOCKSIZE)
        if not boardRect.collidepoint(self.x, self.y):
            if 0 <= self.x <= boardRect.right:
                self.angle = 360 - self.angle
            if 0 <= self.y <= boardRect.bottom:
                self.angle = (540 - self.angle) % 360


    def render(self, surface):
        pygame.draw.circle(surface, (255, 0, 0), (self.x, self.y), self.radius)