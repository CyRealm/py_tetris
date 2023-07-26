import pygame
from gameBoard import GameBoard
from shape import *
from ball import *

EXIT = False
shape_drop = False
dropDelay = 1000
storageShape = None
futureShape = None
foresightShape = None
menace = None
swapped = False
animationFrame = 0
animationDelay = 5000
pause = False
mute = False
MENU = True
GAMEOVER = False


# Load Game
if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((900, 600))
    board = GameBoard()
    myShape = Shape().toPlayer()
    foresightShape = Shape(True, myShape)
    futureShape = Shape()
    menace = Ball(board)
    nukeIcon = pygame.image.load("imgs/nuke_icon.png")
    nukeIcon = pygame.transform.scale(nukeIcon, (nukeIcon.get_width() * 2, nukeIcon.get_height() * 2))
    npc = pygame.image.load("imgs/npc.png")
    menuBG = pygame.image.load("imgs/backdrop.png")
    GUI_FONT = pygame.font.SysFont('Biting My Nails', 32)
    npcX = 650
    approachTimer = 100
    approach = False
    # Load Music
    pygame.mixer.music.load("bgm.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    # Load a clock
    gameClock = pygame.time.Clock()
    delay = 30.0

def reset():
    global board, npcX, approach, storageShape, myShape, futureShape, swapped, foresightShape, approachTimer
    global EXIT, shape_drop, dropDelay, animationFrame, animationDelay, pause, mute, MENU, GAMEOVER
    board = GameBoard()
    myShape = Shape().toPlayer()
    foresightShape = Shape(True, myShape)
    futureShape = Shape()
    npcX = 650
    approachTimer = 100
    approach = False
    EXIT = False
    shape_drop = False
    dropDelay = 1000
    storageShape = None
    swapped = False
    animationFrame = 0
    animationDelay = 5000
    pause = False
    mute = False
    GAMEOVER = False

def npcControl():
    global npcX, approach, storageShape, myShape, futureShape, swapped, foresightShape
    if npcX > 480 and approach:
        npcX -= 0.1
    elif npcX <= 480:
        # Replace
        if storageShape is None:
            storageShape = myShape.toStorage()
            myShape = futureShape.toPlayer()
            foresightShape = Shape(True, myShape)
            futureShape = Shape()
        # Swap
        else:
            if not swapped:
                swapped = True
                holder = myShape.toStorage()
                myShape = storageShape.toPlayer()
                foresightShape = Shape(True, myShape)
                storageShape = holder
        approach = False

    if npcX < 650 and not approach:
        npcX += 0.1


# Main Game Loop
while not EXIT:
    if MENU:
        screen.blit(menuBG, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                EXIT = True
            if event.type == pygame.KEYDOWN:
                MENU = False
        pygame.display.flip()
        continue

    if GAMEOVER:
        gameOverText = GUI_FONT.render("GAME OVER! Press <r> to retry or <q> to quit!", True, RED)
        screen.blit(gameOverText, (screen.get_width() / 2 - gameOverText.get_width() / 2,
                                   screen.get_height() / 2 - gameOverText.get_height() / 2,
                                   gameOverText.get_width(), gameOverText.get_height()))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                EXIT = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset()
                if event.key == pygame.K_q:
                    EXIT = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            EXIT = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                pause = not pause
            if event.key == pygame.K_m:
                mute = not mute
            if not pause:
                if event.key == pygame.K_DOWN:
                    myShape.moveDown(board.boardSpace)
                    dropDelay = 1000 - (board.level - 1) * 100
                if event.key == pygame.K_LEFT:
                    myShape.moveLeft(board.boardSpace)
                    foresightShape = Shape(True, myShape)
                if event.key == pygame.K_RIGHT:
                    myShape.moveRight(board.boardSpace)
                    foresightShape = Shape(True, myShape)
                if event.key == pygame.K_x:
                    myShape.CWRotation(board.boardSpace)
                    foresightShape = Shape(True, myShape)
                if event.key == pygame.K_z:
                    myShape.CCWRotation(board.boardSpace)
                    foresightShape = Shape(True, myShape)
                if event.key == pygame.K_SPACE:
                    shape_drop = True
                if event.key == pygame.K_c:
                    # Replace
                    if storageShape is None:
                        storageShape = myShape.toStorage()
                        myShape = futureShape.toPlayer()
                        futureShape = Shape()
                    # Swap
                    else:
                        if not swapped:
                            swapped = True
                            holder = myShape.toStorage()
                            myShape = storageShape.toPlayer()
                            storageShape = holder
                    foresightShape = Shape(True, myShape)

    delay -= float(gameClock.get_time()) / 1000.0
    gameClock.tick()
    if delay <= 0:
        # Anything you want to occur every half-minute
        delay = 30.0
        approach = True

    if mute:
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()

    if pause:
        continue

    # if not approach:
    #     approachTimer -= 1
    # if approachTimer <= 0 and board.highestPoint - myShape.blockList[0].row > 3 and \
    #     npcX >= 650 and swapped is False:
    #     approach = True
    #     approachTimer = 5000

    npcControl()

    dropDelay -= 1
    if dropDelay <= 0:
        myShape.moveDown(board.boardSpace)
        dropDelay = 1000 - (board.level - 1) * 100

    while shape_drop and myShape.active:
        myShape.moveDown(board.boardSpace)

    while foresightShape is not None and foresightShape.active:
        foresightShape.moveDown(board.boardSpace)

    if myShape.active == False:
        shape_drop = False
        # Log the inactive shape
        for block in myShape.blockList:
            # Checks if the currentShape is settled on a row that's higher up (or lower in row value) than the current highestPoint
            if block.row < board.highestPoint:
                board.highestPoint = block.row
            board.boardSpace[block.row][block.col] = 1
            board.boardColor[block.row][block.col] = block.color
        board.completeRow()
        if board.checkLoss():
            pause = True
            GAMEOVER = True
        myShape = futureShape.toPlayer()
        foresightShape = Shape(True, myShape)
        futureShape = Shape()
        swapped = False
        print(board.highestPoint)

    # --- Rendering Area ---
    screen.fill(0)
    board.render(screen)
    myShape.render(screen)
    if storageShape is not None:
        storageShape.render(screen)
    futureShape.render(screen)
    foresightShape.renderIllusion(screen)
    if menace is not None:
        menace.update(board)
        menace.render(screen)
    screen.blit(nukeIcon, (305, 450))
    # NPC Animation - Count down the Delay, increase the Frame, adjust the Frame in case it's out of index range
    animationDelay -= 1
    if animationDelay <= 0:
        animationDelay = 100
        animationFrame += 1
        if animationFrame > 3:
            animationFrame = 0

    screen.blit(npc, (npcX, 100), (npc.get_width()/4 * animationFrame, 0, npc.get_width()/4, npc.get_height()))
    pygame.display.flip()   # Re-draw everything on screen