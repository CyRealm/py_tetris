from block import Block
from gameBoard import *
import random

T_SHAPE = [[0,0],[-1,0],[1,0],[0,1]]
LINE_SHAPE = [[0,0],[0,-1],[0,1],[0,2]]
L_SHAPE = [[0,0],[0,-1],[0,1],[1,1]]
RL_SHAPE = [[0,0],[0,-1],[0,1],[-1,1]]
Z_SHAPE = [[0,0],[-1,0],[0,1],[1,1]]
S_SHAPE = [[0,0],[1,0],[0,1],[-1,1]]
SQUARE_SHAPE = [[0,0],[1,0],[0,1],[1,1]]
CANCER_SHAPE = [[0,0],[1,1],[-1,1],[0,2]]
ALL_SHAPES = [T_SHAPE, LINE_SHAPE, L_SHAPE, RL_SHAPE, Z_SHAPE, S_SHAPE, SQUARE_SHAPE, CANCER_SHAPE]
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
GREEN = (127, 255, 212)
BLUE = (65, 105, 225)
RED = (255, 0, 0)
MAGENTA = (255, 0, 255)
GOLD = (255, 215, 0)
HOLLOW = pygame.Color(160, 160, 160, 80)
ALL_COLORS = [MAGENTA, CYAN, ORANGE, BLUE, GREEN, RED, GOLD, WHITE]

class Shape:

    def __init__(self, phantom=False, copyShape=None):
        if not phantom:
            self.blockList = []
            r = random.Random()
            index = r.randint(0, 60)
            if index == 60:
                index = 7
            else:
                index = index % 6
            self.chosenShape = ALL_SHAPES[index]
            self.color = WHITE
            for coordinate in self.chosenShape:
                self.blockList.append(Block(coordinate[1] + 10, coordinate[0] + 16, self.color))
        else:
            self.blockList = copyShape.blockList
            self.chosenShape = copyShape.chosenShape
            self.color = HOLLOW
        self.active = True

    def toStorage(self):
        self.blockList = []
        for coordinate in self.chosenShape:
            self.blockList.append(Block(coordinate[1] + 5, coordinate[0] + 16, self.color))
        return self

    def toPlayer(self):
        self.blockList = []
        for coordinate in self.chosenShape:
            self.blockList.append(Block(coordinate[1], coordinate[0] + 5, self.color))
        return self


    def moveDown(self, boardState):
        blocked = False
        mirage_down = []
        for block in self.blockList:
            mirage_down.append(Block(block.row + 1, block.col, block.color))
            if block.row >= GAMEBOARDHEIGHT - 1 or \
                boardState[block.row + 1][block.col] == 1:
                self.active = False
                blocked = True


        if not blocked:
            self.blockList = mirage_down

    def moveLeft(self, boardState):
        blocked = False
        mirage_left = []
        for block in self.blockList:
            mirage_left.append(Block(block.row, block.col - 1, block.color))
            if block.col <= 0 or \
                    boardState[block.row][block.col - 1] == 1:
                blocked = True

        if not blocked:
            self.blockList = mirage_left

    def moveRight(self, boardState):
        blocked = False
        mirage_right = []
        for block in self.blockList:
            mirage_right.append(Block(block.row, block.col + 1, block.color))
            if block.col >= GAMEBOARDWIDTH - 1 or \
                    boardState[block.row][block.col + 1]:
                blocked = True

        if not blocked:
            self.blockList = mirage_right

    def CWRotation(self, boardState):
        if self.chosenShape == SQUARE_SHAPE:
            return
        mirage_CW = []
        blocked = False
        for block in self.blockList:
            # Move the blocks back to the top left corner
            tempRow = block.row - self.blockList[0].row
            tempCol = block.col - self.blockList[0].col
            # Perform the rotation
            # Then move the blocks back to the correct position
            CWBlock = Block(tempCol + self.blockList[0].row,
                                   -tempRow + self.blockList[0].col,
                                   block.color)
            mirage_CW.append(CWBlock)

            # Left Boundary
            if CWBlock.col < 0:
                blocked = True

            # Right Boundary
            elif CWBlock.col > GAMEBOARDWIDTH - 1:
                blocked = True

            # Bottom Boundary
            elif CWBlock.row > GAMEBOARDHEIGHT - 1:
                blocked = True

            # Collision with other Blocks
            elif boardState[CWBlock.row][CWBlock.col] == 1:
                blocked = True

        if not blocked:
            self.blockList = mirage_CW

    def CCWRotation(self, boardState):
        if self.chosenShape == SQUARE_SHAPE:
            return
        mirage_CCW = []
        blocked = False
        for block in self.blockList:
            # Move the blocks back to the top left corner
            tempRow = block.row - self.blockList[0].row
            tempCol = block.col - self.blockList[0].col
            # Perform the rotation
            # Then move the blocks back to the correct position
            CCWBlock = Block(-tempCol + self.blockList[0].row,
                                   tempRow + self.blockList[0].col,
                                   block.color)
            mirage_CCW.append(CCWBlock)

            # Left Boundary
            if CCWBlock.col < 0:
                blocked = True

            # Right Boundary
            elif CCWBlock.col > GAMEBOARDWIDTH - 1:
                blocked = True

            # Bottom Boundary
            elif CCWBlock.row > GAMEBOARDHEIGHT - 1:
                blocked = True

            # Collision with other Blocks
            elif boardState[CCWBlock.row][CCWBlock.col] == 1:
                blocked = True

        if not blocked:
            self.blockList = mirage_CCW


    def render(self, surface):
        for block in self.blockList:
            block.render(surface)

    def renderIllusion(self, surface):
        for block in self.blockList:
            block.renderIllusion(surface)