import pygame, sys
from pygame.locals import QUIT
import numpy as np
import math
import random

#functions
def make_board():
  board = np.zeros((6,7))
  return board

def check(board, col):
#sees if there is any space left in the column
  return board[5][col]==0

def drop(board, r, c, team):
  board[r][c] = team
  
def getOpen(board, col):
  for r in range(ROWS):
    if board[r][col]==0:
      return r

def printBoard():
  print(np.flip(board,0))

def drawGAME(board):
  for c in range(COLS):
    for r in range(ROWS):
      pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
      pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), radius)
      
    for c in range(COLS):
      for r in range(ROWS):
        if board[r][c] == 1:
          pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), radius)
        elif board[r][c] == 2:
          pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), radius)
  pygame.display.update()

def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLS-3):
        for r in range(ROWS):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
 
    # Check vertical locations for win
    for c in range(COLS):
        for r in range(ROWS-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
 
    # Check positively sloped diaganols
    for c in range(COLS-3):
        for r in range(ROWS-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True
 
    # Check negatively sloped diaganols
    for c in range(COLS-3):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True
 
def draw_board(board):
    for c in range(COLS):
        for r in range(ROWS):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), radius)
     
    for c in range(COLS):
        for r in range(ROWS):      
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), radius)
            elif board[r][c] == 2: 
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), radius)
    pygame.display.update()

#expands pieces
def pickPiece(board):
  r=random.randint(0,5)
  c=random.randint(0,6)
  direct = random.randint(0,1)

  if (board[r][c] == 1) or (board[r][c] == 2):
    expand(board, r, c, direct)
  else:
    pickPiece(board)

def expand(board, row, col, direction):
  #goes up
  r=ROWS-1
  while r > row:
    board[r][col] = board[r-1][col]
    r-=1

  drawGAME(board)
#variables
board = make_board()
game_over = False
turn = 0
ROWS = 6
COLS = 7
counter = random.randrange(1, 11) #same as randint(1,10)

SQUARESIZE=100
width = COLS*SQUARESIZE
height = (ROWS+1)*SQUARESIZE
size=(width, height)
screen=pygame.display.set_mode(size)
radius = SQUARESIZE/2-5


#colors
RED=(255,0,0)
BLACK=(0,0,0)
BLUE=(0,0,255)
YELLOW=(255,255,0)
PURPLE=(230,230,250)

#loop
pygame.init()
myfont = pygame.font.SysFont("Arial", 75)
drawGAME(board)
pygame.display.update()
while not game_over:
  
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()

    if event.type == pygame.MOUSEMOTION:
      pygame.draw.rect(screen, BLACK, (0,0,width, SQUARESIZE))
      x = event.pos[0]
      if turn%2==0:
        pygame.draw.circle(screen, RED, (x, int(SQUARESIZE/2)), radius)
      else:
        pygame.draw.circle(screen, YELLOW, (x, int(SQUARESIZE/2)), radius)
    pygame.display.update()

    if event.type == pygame.MOUSEBUTTONDOWN:
      pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
      if turn%2 == 0:
        x=event.pos[0]
        col=int(math.floor(x/SQUARESIZE))

        if check(board, col):
          row = getOpen(board, col)
          drop(board, row, col, 1)

        #check for wins
          if winning_move(board, 1):
            label = myfont.render("Player 1 wins!!", 1, RED)
            screen.blit(label, (40,10))
            game_over = True
      else:
        x=event.pos[0]
        col=int(math.floor(x/SQUARESIZE))

        if check(board, col):
          row = getOpen(board, col)
          drop(board, row, col, 2)

          #check for win
          if winning_move(board, 2):
            label = myfont.render("Player 2 wins!!", 2, YELLOW)
            screen.blit(label, (40,10))
            game_over = True
            
    #player 1 turn
    if (turn % 2 == 0):
      move = int(input("Player 1 pick a column 0-6"))
      if check(board, move):
        row=getOpen(board, move)
        drop(board, row, move, 1)

        if winning_move(board, 1):
            label = myfont.render("Player 1 wins!!", 1, RED)
            screen.blit(label, (40,10))
            game_over = True

    #player 2 turn
    else:
      move = int(input("Player 2 pick a column 0-6"))
      if check(board, move):
        row=getOpen(board, move)
        drop(board, row, move, 2)

        if winning_move(board, 2):
            label = myfont.render("Player 2 wins!!", 2, YELLOW)
            screen.blit(label, (40,10))
            game_over = True

    if (turn%counter == 0 and turn>=5):
      pygame.display.set_caption("SPECIAL TURN")
      pygame.time.wait(5000)
      pickPiece(board)
  
    turn +=1
    pygame.display.set_caption(str(turn)+ ": Player {} turn".format(turn%2 + 1))
    
    printBoard()
    drawGAME(board)

if game_over:
  pygame.time.wait(30000)