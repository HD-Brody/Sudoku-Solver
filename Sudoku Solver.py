import random
import copy
import pygame, sys
import time
from pygame.locals import QUIT
pygame.init()

############################# FUNCTIONS ###############################
def printBoard(board):
    for i in range(9):
        for j in range(9):
            print(board[i][j],end=" ")
            if j == 2 or j == 5:
                print('|', end=" ")
        print()
        if i == 2 or i == 5:
            print('-'*22)
    print()

def isValid(r, c, num, board): #num is a string
    not_in_row = board[r].count(num) < 1
    if not not_in_row:
        return False

    not_in_col = True
    for i in range(9):
        if board[i][c] == num and i != r:
            return False

    not_in_square = True
    for i in range(r//3*3, r//3*3+3):
        if i != r and num in board[i]:
            if board[i].index(num) in range(c//3*3, c//3*3+3):
                return False
    return True

def fillBoard(r,c, board, num_list):
    if r == 8 and c == 9:
        return True

    if c == 9:
        c = 0
        r += 1

    if board[r][c] != '.':
        return fillBoard(r,c+1, board, num_list)
    
    for num in num_list:
        if isValid(r,c,num, board):
            board[r][c] = num
            if fillBoard(r,c+1, board, num_list):
                return board
            else:
                board[r][c] = '.'
    return False

def getSolutions(r, c, board):
    if c == 9:
        c = 0
        r += 1

    if board[r][c] != '.':
        return getSolutions(r,c+1, board)
    
    for num in range(1,10):
        num = str(num)
        if isValid(r,c,num, board):
            board[r][c] = num
            if all(['.' not in board[i] for i in range(9)]):
                global solutions
                solutions += 1
                break
            else:
                getSolutions(r,c+1, board)
    board[r][c] = '.'
    return False


def generateFilledBoard(num_list):
    board = [['.' for i in range(9)] for j in range(9)]
    random.shuffle(num_list)
    return fillBoard(0,0,board,num_list)

def getFilledSquares(board):
    filled_squares = []
    for i in range(9):
        for j in range(9):
            if board[i][j] != '.':
                filled_squares.append((i,j))
    random.shuffle(filled_squares)
    return filled_squares

def removeNums(board):
    filled_squares = getFilledSquares(board)
    filled_squares_count = len(filled_squares)
    rounds = 5
    while rounds > 0 and filled_squares_count >= 17:
        row, col = filled_squares.pop()
        filled_squares_count -= 1
        removed_square = board[row][col]
        board[row][col] = '.'
        board_copy = copy.deepcopy(board)
        global solutions
        solutions = 0
        getSolutions(0,0,board_copy)
        if solutions != 1:
            board[row][col] = removed_square
            filled_squares_count += 1
            rounds -= 1
    return board

def generateSudoku():
    new_board = generateFilledBoard(std_num_list)
    without_squares = removeNums(new_board)
    return without_squares

#Pygame stuff
def drawBackground(screen):
    screen.fill((255,255,255))
    pygame.display.update()

def redraw(screen):
    pygame.display.update()

############################# CLASSES ###############################

class Block():
  def __init__(self, screen, letter, posx, posy, gridsize):
    self.screen = screen
    self.letter = letter
    self.gridsize = gridsize
    self.posx = posx * gridsize
    self.posy = posy * gridsize
    self.clr = (255, 255, 255)
  
  def drawBlock(self):
    pygame.draw.rect(self.screen, self.clr, (self.posx, self.posy, self.gridsize - 2, self.blockheight - 2))

  def drawText(self):
    text = font.render(self.letter, 1, (0,0,0))
    self.screen.blit(text,(self.posx, self.posy))


############################# VARIABLES ###############################
clock = pygame.time.Clock()
std_num_list = ['1','2','3','4','5','6','7','8','9']

screen = pygame.display.set_mode((900,600))
gridsize = 10
fps = 10
font = pygame.font.SysFont("Arial Black", gridsize)

board = generateSudoku()
printBoard(board)

solved = fillBoard(0,0,board, std_num_list)
printBoard(solved)

############################# MAIN GAME LOOP ###############################
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            pass

    drawBackground(screen)
    redraw(screen)
    clock.tick(30)