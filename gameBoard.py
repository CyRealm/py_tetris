import pygame, random
BLOCKSIZE = 25
GAMEBOARDWIDTH = 12
GAMEBOARDHEIGHT = 20
WHITE = (255, 255, 255)

class GameBoard:

    # Constructor
    def __init__(self):
        self.GAMEBOARDWIDTH = 12
        self.GAMEBOARDHEIGHT = 20
        self.boardSpace = [[0 for j in range(GAMEBOARDWIDTH)] for i in range(GAMEBOARDHEIGHT)]
        self.boardColor = [[(0, 0, 0) for j in range(GAMEBOARDWIDTH)] for i in range(GAMEBOARDHEIGHT)]
        self.score = 0
        self.level = 1
        self.SCORE_FONT = pygame.font.SysFont('Arial', 32)
        self.TINY_FONT = pygame.font.SysFont('Arial', 16)
        self.nuke_cd = 0
        self.highestPoint = self.GAMEBOARDHEIGHT

    def completeRow(self):
        # Look at every row in boardSpace, and identify the rows that are filled
        for row in range(self.GAMEBOARDHEIGHT):
            # 1. Generate a random number (between 0 to 100) that determines if the mini-nuke goes off
            nuke_chance = random.randint(0, 5)
            if self.boardSpace[row].count(0) == 0:
                print(self.nuke_cd)
                if nuke_chance == 0 and self.nuke_cd <= 0:
                    self.clearRow(row - 1)
                    self.clearRow(row)
                    if row + 1 < GAMEBOARDHEIGHT:
                        self.clearRow(row + 1)
                    self.nuke_cd = 3
                else:
                    self.nuke_cd -= 1
                    self.clearRow(row)
                self.score += 100
                self.level = self.score / 500 + 1

    def clearRow(self, rowNum):
        for row in range(rowNum - 1, -1, -1):
            self.boardSpace[row + 1] = self.boardSpace[row]
            self.boardColor[row + 1] = self.boardColor[row]
        self.boardSpace[0] = [0 for i in range(self.GAMEBOARDWIDTH)]
        self.boardColor[0] = [(0, 0, 0) for i in range(self.GAMEBOARDWIDTH)]

    def checkLoss(self):
        # 1. access the top row in gameboard
        # Hint: You may want to choose the variable to inspect(boardSpace, boardColor)
        topRow = self.boardSpace[0]
        # 2. Detect if there are any blocks in the top row
        # 3. If there is, return True. If not, return False
        if topRow.count(1) > 0:
            return True
        else:
            return False


    def render(self, surface):
        for row in range(GAMEBOARDHEIGHT):
            for col in range(GAMEBOARDWIDTH):
                pygame.draw.rect(surface, self.boardColor[row][col],
                                 pygame.Rect(col * BLOCKSIZE, row * BLOCKSIZE, BLOCKSIZE - 1, BLOCKSIZE -1), 0)

        textSurface = self.SCORE_FONT.render('Score: ' + str(self.score), True, WHITE)
        levelSurface = self.SCORE_FONT.render('Level: ' + str(int(self.level)), True, WHITE)
        storageLabel = self.SCORE_FONT.render('Reserved', True, WHITE)
        futureLabel = self.SCORE_FONT.render('Next', True, WHITE)
        if self.nuke_cd > 0:
            corrected_cd_text = self.nuke_cd
        else:
            corrected_cd_text = 0
        nuke_cd_label = self.TINY_FONT.render(str(corrected_cd_text), True, WHITE)
        surface.blit(textSurface, (10, 510))
        surface.blit(levelSurface, (200, 510))
        surface.blit(storageLabel, (350, 50))
        surface.blit(nuke_cd_label, (360, 490))
        surface.blit(futureLabel, (370, 350))
        pygame.draw.rect(surface, WHITE, pygame.Rect(0, 0,
                                                     self.GAMEBOARDWIDTH * BLOCKSIZE,
                                                     self.GAMEBOARDHEIGHT * BLOCKSIZE), 1)
