import pygame
from time import sleep
from random import randint
import sys

# Settings
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (20, 20, 20)
GREY_LIGHT = (22, 22, 22)

WIN_COLOR = (100, 100, 100)
HIGHLIGHT = GREY_LIGHT
BG_COLOR = GREY
LINE_COLOR = WHITE


# Pygame Setup
pygame.init()
gameWindow = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("TIC TAC TOE")

# Render Grid
def draw_Grid():
    # Vertical Lines
    pygame.draw.line(gameWindow, LINE_COLOR, ((WINDOW_WIDTH / 3), 0), ((WINDOW_WIDTH / 3), WINDOW_HEIGHT))
    pygame.draw.line(gameWindow, LINE_COLOR, ((WINDOW_WIDTH / 3) * 2, 0), ((WINDOW_WIDTH / 3) * 2, WINDOW_HEIGHT))
    # Horizontal Lines
    pygame.draw.line(gameWindow, LINE_COLOR, (0, (WINDOW_HEIGHT / 3)), (WINDOW_WIDTH, (WINDOW_HEIGHT / 3)))
    pygame.draw.line(gameWindow, LINE_COLOR, (0, (WINDOW_HEIGHT / 3) * 2), (WINDOW_WIDTH, (WINDOW_HEIGHT / 3) * 2))

# create pygame.rect's for grid Cells
def get_Grid_Cells():
        
    gridCells = []

    for multiplicator in range(3):
        gridCells.append(pygame.Rect(((WINDOW_WIDTH / 3) * multiplicator, 0), ((WINDOW_HEIGHT / 3), (WINDOW_HEIGHT / 3))))
        gridCells.append(pygame.Rect(((WINDOW_WIDTH / 3) * multiplicator, (WINDOW_HEIGHT / 3)), ((WINDOW_WIDTH / 3), (WINDOW_HEIGHT / 3))))
        gridCells.append(pygame.Rect(((WINDOW_WIDTH / 3) * multiplicator, (WINDOW_HEIGHT / 3) * 2), ((WINDOW_WIDTH / 3), (WINDOW_HEIGHT / 3))))

    return gridCells

def mouse_Over_Cell(cells):
    mousePos = pygame.mouse.get_pos()
    mouseRect = pygame.Rect((mousePos), (0, 0))

    for cell in cells:
        if cell.contains(mouseRect):
            return cell
        else:
            pass

def preview_Selected_Cell(cell, player):
    cellCenter = cell.center
    cellWidth = cell.width

    if player == "O": 
        pygame.draw.rect(gameWindow, HIGHLIGHT, cell)
        pygame.draw.circle(gameWindow, WHITE, cellCenter, (cellWidth / 2 - 30), 3)
    else:
        pygame.draw.rect(gameWindow, HIGHLIGHT, cell)
        pygame.draw.line(gameWindow, WHITE, (cellCenter[0] - (cellWidth / 2 - 30), (cellCenter[1] + (cellWidth / 2 - 30))), (cellCenter[0] + (cellWidth / 2 - 30), (cellCenter[1] - (cellWidth / 2 - 30))), 3)
        pygame.draw.line(gameWindow, WHITE, (cellCenter[0] - (cellWidth / 2 - 30), (cellCenter[1] - (cellWidth / 2 - 30))), (cellCenter[0] + (cellWidth / 2 - 30), (cellCenter[1] + (cellWidth / 2 - 30))), 3)

def get_Cell_Index(cell, givenCells):
    cells = givenCells

    for index, cell2 in enumerate(cells):
        if cell == cell2:
            return index

def index_Is_Already_Marked(index, cellList):
    if cellList[index] == "X":
        return True
    else:
        if cellList[index] == "O":
            return True
        else:
            return False

def draw_Marked_Cells(cellMarker, cells):
    for index, cell in enumerate(cellMarker):
        if cell == "X":
            cellCenter = cells[index].center
            cellWidth = cells[index].width

            pygame.draw.line(gameWindow, WHITE, (cellCenter[0] - (cellWidth / 2 - 30), (cellCenter[1] + (cellWidth / 2 - 30))), (cellCenter[0] + (cellWidth / 2 - 30), (cellCenter[1] - (cellWidth / 2 - 30))), 3)
            pygame.draw.line(gameWindow, WHITE, (cellCenter[0] - (cellWidth / 2 - 30), (cellCenter[1] - (cellWidth / 2 - 30))), (cellCenter[0] + (cellWidth / 2 - 30), (cellCenter[1] + (cellWidth / 2 - 30))), 3)
        elif cell == "O":
            cellCenter = cells[index].center
            cellWidth = cells[index].width

            pygame.draw.circle(gameWindow, WHITE, cellCenter, (cellWidth / 2 - 30), 3)
        else:
            pass

def win_Condition(markedCells, player):
    
    conditionList = [
        (markedCells[0] == player) and (markedCells[1] == player) and (markedCells[2] == player), 
        (markedCells[3] == player) and (markedCells[4] == player) and (markedCells[5] == player),
        (markedCells[6] == player) and (markedCells[7] == player) and (markedCells[8] == player),

        (markedCells[0] == player) and (markedCells[3] == player) and (markedCells[6] == player),
        (markedCells[1] == player) and (markedCells[4] == player) and (markedCells[7] == player),
        (markedCells[2] == player) and (markedCells[5] == player) and (markedCells[8] == player),

        (markedCells[0] == player) and (markedCells[4] == player) and (markedCells[8] == player),
        (markedCells[2] == player) and (markedCells[4] == player) and (markedCells[6] == player)
    ]

    for index, condition in enumerate(conditionList):
        if condition == True:
            return index
        
    return "no_Win"

def get_Win_Condition_Cells(index):

    winningCells = [(0, 1 ,2), (3, 4, 5), (6, 7, 8),
                    (0, 3, 6), (1, 4, 7), (2, 5, 8),
                    (0, 4, 8), (2, 4, 6)]

    return winningCells[index]

def draw_Win(winIndicies, gridCells, counter):
    cell01 = gridCells[winIndicies[0]]
    cell02 = gridCells[winIndicies[1]]
    cell03 = gridCells[winIndicies[2]]

    pygame.draw.rect(gameWindow, (100 + counter, 100 + counter, 100 + counter), cell01)
    pygame.draw.rect(gameWindow, (100 + counter, 100 + counter, 100 + counter), cell02)
    pygame.draw.rect(gameWindow, (100 + counter, 100 + counter, 100 + counter), cell03)
   

def ki_Move(alreadyMarkedCells):
    randomChoice = 0
    found = False
    while found == False:
        randomChoice = randint(0, 8)
        if (alreadyMarkedCells[randomChoice] == "X") or (alreadyMarkedCells[randomChoice] == "O"):
            pass
        else:
            found = True
            return randomChoice

def game_is_a_tie(alreadyMarkedCells):
    for cell in alreadyMarkedCells:
        if (cell == "X") or (cell == "O"):
            pass
        else:
            return False
    return True

# GAMELOOP
def tic_Tac_toe():
    gameLoopRun = True
    clock = pygame.time.Clock()
    tick = 10

    gridCells = get_Grid_Cells()
    lastSelectedCell = gridCells[4]
    markedCells = [x for x in range(9)]

    player = "O"
    moveMade = False
    changePlayer = lambda x:"X" if x == "O" else "O"

    while gameLoopRun:
        clock.tick(tick)
        gameWindow.fill(BG_COLOR)      

        # Always have a cell selected
        # can be None if mouse is between the Cells  
        activeCell = mouse_Over_Cell(gridCells)
        if activeCell == None:
            activeCell = lastSelectedCell
        else:
            lastSelectedCell = activeCell

        activeCellIndex = get_Cell_Index(activeCell, gridCells)
        
        
        # Mark a Cell permantly and check for Win Condition
        if player == "X":
            kiCellChoice = ki_Move(markedCells)
            del markedCells[kiCellChoice]
            markedCells.insert(kiCellChoice, player)
            moveMade = True
            
        if index_Is_Already_Marked(activeCellIndex, markedCells):
            pass
        else:
            preview_Selected_Cell(activeCell, player)     
            if (pygame.mouse.get_pressed(num_buttons=3)[0]) and (player == "O"):
                del markedCells[activeCellIndex]
                markedCells.insert(activeCellIndex, player)
                moveMade = True
            
                                
        winningIndex = win_Condition(markedCells, player)             
        if winningIndex != "no_Win":
            print(player, " WON!")

            # Win animation
            makeNegative = 1
            for firstCounter in range(7):
                makeNegative *= -1
            
                for counter in range(50):
                    counter *= makeNegative
                    draw_Win(get_Win_Condition_Cells(winningIndex), gridCells, counter)
                    draw_Grid()
                    draw_Marked_Cells(markedCells, gridCells)
                    pygame.display.update()
                    
                    sleep(0.0005)

            gameLoopRun = False
        else:
            pass

        # Change Player
        if moveMade == True:
            player = changePlayer(player)
            moveMade = False

        # Check for Tie
        if game_is_a_tie(markedCells) and (winningIndex == "no_Win"):
            gameLoopRun = False
            print("Game is a Tie!")
            sleep(0.5)

        draw_Marked_Cells(markedCells, gridCells)
        draw_Grid()
        pygame.display.update()

        # Exit Window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameLoopRun = False
                pygame.quit()
                sys.exit()
                
    
    sleep(0.5)
    tic_Tac_toe()
    


if __name__ == "__main__":
    tic_Tac_toe()