from math import floor
import random
import asyncio
import pygame, sys
from pygame.locals import *


import sys, platform
if sys.platform == "emscripten":
    platform.window.canvas.style.imageRendering = "pixelated"



#To do:
# rename variables, do documentation.



#Game board is a list of list of booleans. There are 20 lists (each corresponding to a row)
# and 10 booleans in each (one for each column). To access, should be game_board[y][x].
# A false means there is nothing in that box and it should be white.

class Tetris:

    def __init__(self):
        # Initiates Tetris game

        self.current_block = False
        self.since_moving = 0
        self.paused = False
        self.testing = False

        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.grey = (169, 169, 169)
        self.xnum_box = 10
        self.box_size = 40
        self.ynum_box = 20
        self.width = floor(self.xnum_box * self.box_size)
        self.height = floor(self.ynum_box * self.box_size)

        self.game_board = []
        for a in range(self.ynum_box):
            self.game_board.append([False] * self.xnum_box)

        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Tetris')



    def draw_board(self):
        # Draws board onto window.
        self.window.fill(self.white)
        self.draw_colors()
        for x in range(self.xnum_box - 1):
            pygame.draw.line(self.window, self.black, ((x + 1) * self.box_size, 0),
                             ((x + 1) * self.box_size, self.height), 1)
        for y in range(self.ynum_box - 1):
            pygame.draw.line(self.window, self.black, (0, ((y + 1) * self.box_size)),
                             (self.width, (y + 1) * self.box_size), 1)
        if self.paused:
            pause_size = self.box_size * 4
            dist = (self.width - pause_size) / 2
            pygame.draw.rect(self.window, self.grey, (dist, dist, pause_size, pause_size))
            font = pygame.font.SysFont(None, 24)
            img = font.render('paused', True, self.black)
            self.window.blit(img, (dist + pause_size/3, dist + pause_size / 2))

    def draw_colors(self):
        # Draws blocks onto window for each block in the board.
        for y in range(self.ynum_box):
            for x in range(self.xnum_box):
                color = self.white
                if self.game_board[y][x]:
                    color = self.black
                draw_block(self.window, color, (x, y))
        if not (self.current_block == False):
            self.current_block.draw_block(self.window)

    def can_move(self):
        return (not self.paused) and (not self.current_block == False)


    def on_mouse_click(self, pos):
        # Runs when mouse clicks on the position shown.
        # Flips the square clicked.

        if self.testing:
            y = floor(pos[1] / self.box_size)
            x = floor(pos[0] / self.box_size)
            self.game_board[y][x] = not self.game_board[y][x]

    def on_tick(self):
        if self.current_block == False:
            self.current_block = Block((5, 0), random.randint(0, 6))
        elif self.since_moving == 15:
            self.move_down()
            self.since_moving = 0
        else:
            self.since_moving = self.since_moving + 1

    def clear_row(self):
        to_remove = []
        for x in range(len(self.game_board)):
            all_black = True
            for square in self.game_board[x]:
                all_black = all_black and square
            if all_black:
                to_remove.append(x)
        for x in to_remove:
            self.game_board.pop(x)
            self.game_board.insert(0, [False] * self.xnum_box)

    def rotate(self):
        if self.can_move():
            self.current_block.rotate(self.game_board)
    def move_left(self):
        if self.can_move():
            self.current_block.move_left(self.game_board)
    def move_right(self):
        if self.can_move():
            self.current_block.move_right(self.game_board)
    def move_down(self):
        if (self.can_move() and
                not self.current_block.move_down(self.game_board)):
            self.current_block.add_to_board(self.game_board)
            self.clear_row()
            self.current_block = False
    def all_down(self):
        while not (self.current_block == False):
            self.move_down()
    def flip_pause(self):
        self.paused = not self.paused
    def flip_testing(self):
        self.testing = not self.testing
    def reset(self):
        self.game_board = []
        for a in range(self.ynum_box):
            self.game_board.append([False] * self.xnum_box)

def draw_block(wind, color, pos):
    box_size = 40
    pygame.draw.rect(wind, color,
                     (pos[0] * box_size, pos[1] * box_size,
                      box_size, box_size))

class Block:
    def __init__(self, pos, rand):
        self.pos = pos
        self.connections = []
        self.add_connections(rand)

        self.black = (0, 0, 0)
        self.xnum_box = 10
        self.ynum_box = 20


    def add_connections(self, rand):
        if rand == 0:  # Long brick
            self.connections.append((0, 1))
            self.connections.append((0, 2))
            self.connections.append((0, -1))
        elif rand == 1:  # Square
            self.connections.append((-1, 0))
            self.connections.append((-1, -1))
            self.connections.append((0, -1))
        elif rand == 2: #L
            self.connections.append((0, 1))
            self.connections.append((1, -1))
            self.connections.append((0, -1))
        elif rand == 3: #other L
            self.connections.append((0, 1))
            self.connections.append((-1, -1))
            self.connections.append((0, -1))
        elif rand == 4: #Squiggly bit
            self.connections.append((0, 1))
            self.connections.append((-1, 0))
            self.connections.append((-1, -1))
        elif rand == 5:  # other squiggly bit
            self.connections.append((0, 1))
            self.connections.append((1, 0))
            self.connections.append((1, -1))
        elif rand == 6:   #t shape
            self.connections.append((0, 1))
            self.connections.append((1, 0))
            self.connections.append((-1, 0))


    def draw_block(self, wind):
        draw_block(wind, self.black, self.pos)
        for p in self.connections:
            draw_block(wind, self.black, (self.pos[0] + p[0], self.pos[1] + p[1]))

    def move_down(self, board):
        # Returns true if successful
        new_pos = (self.pos[0], self.pos[1] + 1)
        if not self.test_collisions(new_pos, board):
            self.pos = new_pos
            return True
        else:
            return False

    def rotate(self, board):
        new_connections = []
        for c in self.connections:
            new_connections.append((c[1], -c[0]))
        if not self.test_collisions_rotate(new_connections, board):
            self.connections = new_connections

    def move_left(self, board):
        new_pos = (self.pos[0] - 1, self.pos[1])
        if not self.test_collisions(new_pos, board):
            self.pos = new_pos

    def move_right(self, board):
        new_pos = (self.pos[0] + 1, self.pos[1])
        if not self.test_collisions(new_pos, board):
            self.pos = new_pos

    def test_collisions_rotate(self, new_connections, board):
        squares = new_connections.copy()
        squares.append((0,0))
        collision = False
        for s in squares:
            test = (s[0] + self.pos[0], s[1] + self.pos[1])
            if test[0] == -1 or test[0] == self.xnum_box or test[1] == self.ynum_box:
                collision = True
            else:
                collision = collision or board[test[1]][test[0]]
        return collision

    def test_collisions(self, new_pos, board):
        #Returns false if it's clear
        squares = self.connections.copy()
        squares.append((0,0))
        collision = False
        for s in squares:
            test = (s[0] + new_pos[0], s[1] + new_pos[1])
            if test[0] == -1 or test[0] == self.xnum_box or test[1] == self.ynum_box:
                collision = True
            else:
                collision = collision or board[test[1]][test[0]]
        return collision

    def add_to_board(self, board):
        squares = self.connections.copy()
        squares.append((0,0))
        for s in squares:
            temp = (s[0] + self.pos[0], s[1] + self.pos[1])
            board[temp[1]][temp[0]] = True


async def main():
    pygame.init()
    tetris_game = Tetris()

    fps = 30  # frames per second setting
    fps_clock = pygame.time.Clock()

    # You can initialise pygame here as well

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                tetris_game.on_mouse_click(pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    tetris_game.rotate()
                if event.key == pygame.K_LEFT:
                    tetris_game.move_left()
                if event.key == pygame.K_RIGHT:
                    tetris_game.move_right()
                if event.key == pygame.K_DOWN:
                    tetris_game.move_down()
                if event.key == pygame.K_SPACE or event.key == pygame.K_KP_ENTER:
                    tetris_game.all_down()
                if event.key == pygame.K_p:
                    tetris_game.flip_pause()
                if event.key == pygame.K_t:
                    tetris_game.flip_testing()
                if event.key == pygame.K_r:
                    tetris_game.reset()
        tetris_game.draw_board()
        tetris_game.on_tick()
        fps_clock.tick(fps)
        pygame.display.update()
        await asyncio.sleep(0)  # do not forget that one, it must be called on every frame

    # Closing the game (not strictly required)


if __name__ == "__main__":
    asyncio.run(main())