import pygame

# Future Add-on: Texture for blocks
BLOCKSIZE = 25
class Block:

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color

    def render(self, surface):
        pygame.draw.rect(surface, self.color, pygame.Rect(self.col * BLOCKSIZE,
                                                          self.row * BLOCKSIZE,
                                                          BLOCKSIZE - 1, BLOCKSIZE - 1))

    def renderIllusion(self, surface):
        pygame.draw.rect(surface, self.color, pygame.Rect(self.col * BLOCKSIZE,
                                                          self.row * BLOCKSIZE,
                                                          BLOCKSIZE - 1, BLOCKSIZE - 1), 2)
