import pygame, sys, os
from pygame.locals import *
from collections import deque
import heapq
import time
import numpy as np

class SokobanPuzzle:
    def __init__(self, grid, player_pos, g=0):
        self.grid = grid
        self.player_pos = player_pos
        self.g = g
        self.h = len(grid)
        self.w = len(grid[0])
        self.targets = {(row, col) for row in range(self.h) for col in range(self.w) if grid[row][col] == 'S'} 

    @staticmethod
    def default_grid():
        return [
            list("OOOOOOOOOOOO"),  # Row 0
            list("O     OOOOOO"),  # Row 1
            list("O OBOB     O"),  # Row 2
            list("O   O  O O O"),  # Row 3
            list("OSO OB    RO"),  # Row 4
            list("O         OO"),  # Row 5
            list("OSO OOOOOOO "),   # Row 6
            list("OS  O       "),   # Row 7
            list("OOOOO       ")    # Row 8
        ]
    
    def __hash__(self):
        return hash((tuple(tuple(row) for row in self.grid), self.player_pos))
    
    def __eq__(self, other):
        return self.grid == other.grid and self.player_pos == other.player_pos

    def isGoal(self):
        for row, col in self.targets:
            if self.grid[row][col] != 'B':  # Ensure each target contains a box
                return False
        return True

    def successorFunction(self, direction):
        x, y = self.player_pos
        new_x, new_y = x, y

        if direction == "UP":
            new_x -= 1
        elif direction == "DOWN":
            new_x += 1
        elif direction == "LEFT":
            new_y -= 1
        elif direction == "RIGHT":
            new_y += 1

        if new_x < 0 or new_x >= self.h or new_y < 0 or new_y >= self.w:
            return None  # Out of bounds

        if self.grid[new_x][new_y] == 'O':
            return None  # Cannot move into walls

        new_grid = [row[:] for row in self.grid]

        if new_grid[new_x][new_y] == 'B':
            next_x, next_y = new_x + (new_x - x), new_y + (new_y - y)
            if next_x < 0 or next_x >= self.h or next_y < 0 or next_y >= self.w:
                return None  # Box would move out of bounds
            if new_grid[next_x][next_y] not in (' ', 'S'):
                return None  # Box cannot be pushed

            new_grid[next_x][next_y] = 'B'
            new_grid[new_x][new_y] = ' ' if new_grid[new_x][new_y] == 'B' else 'S'

        new_grid[x][y] = ' ' if new_grid[x][y] == 'R' else 'S'
        new_grid[new_x][new_y] = 'R'
        
        return SokobanPuzzle(new_grid, (new_x, new_y), self.g + 1)
   
    def display(self):
        # Restore target points before displaying the grid
        for row, col in self.targets:
            if self.grid[row][col] == ' ':
                self.grid[row][col] = 'S'
        
        for row in self.grid:
            print(''.join(row))
        print()

    def draw(self, screen, skin):
        w = skin.get_width() / 4
        offset = (w - 4) / 2
        
        # Restore target points for visual consistency
        for row, col in self.targets:
            if self.grid[row][col] == ' ':
                self.grid[row][col] = 'S'

        # Render the grid as before
        for row_idx in range(self.h):
            for col_idx in range(self.w):
                cell = self.grid[row_idx][col_idx]
                if cell == 'O':  # Wall
                    screen.blit(skin, (col_idx * w, row_idx * w), (0, 2 * w, w, w))
                elif cell == ' ':  # Empty space
                    screen.blit(skin, (col_idx * w, row_idx * w), (0, 0, w, w))
                elif cell == 'R':  # Player
                    screen.blit(skin, (col_idx * w, row_idx * w), (w, 0, w, w))
                elif cell == 'B':  # Box
                    screen.blit(skin, (col_idx * w, row_idx * w), (2 * w, 0, w, w))
                elif cell == 'S':  # Storage/Goal area
                    screen.blit(skin, (col_idx * w, row_idx * w), (0, w, w, w))
                elif cell == '.':  # Player on storage
                    screen.blit(skin, (col_idx * w, row_idx * w), (w, w, w, w))
                elif cell == '*':  # Box on storage
                    screen.blit(skin, (col_idx * w, row_idx * w), (2 * w, w, w, w))

        pygame.display.flip()

    def __lt__(self, other):
        return (self.g + self.h) < (other.g + other.h)