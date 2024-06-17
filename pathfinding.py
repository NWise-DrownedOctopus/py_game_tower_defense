import os
import sys
from queue import PriorityQueue

import pygame

from scripts.utils import load_images
from scripts.tilemap import Tilemap

FPS = 60
WIDTH = 640
ROWS = 40
RENDER_SCALE = 4

RED = (190, 47, 66)
GREEN = (100, 160, 63)
BLUE = (49, 162, 242)
YELLOW = (241, 197, 52)
WHITE = (253, 253, 253)
BLACK = (0, 0, 0)
PURPLE = (137, 82, 141)
ORANGE = (235, 137, 49)
GREY = (157, 157, 157)
TEAL = (63, 253, 239)


class Tile:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TEAL

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TEAL

    def make_path(self):
        self.color = PURPLE

    def draw(self, surf):
        pygame.draw.circle(surf, self.color, (self.x + 8, self.y + 8), 3)

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():  # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False


def h(t1, t2):
    x1, y1 = t1
    x2, y2 = t2
    return abs(x1 - x2) + abs(y1 - y2)


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            tile = Tile(i, j, gap,  rows)
            grid[i].append(tile)

    return grid


def reconstruct_path(came_from, current, draw, vizulize=False):
    pathway = []
    while current in came_from:
        current = came_from[current]
        current.make_path()
        if vizulize:
            draw()
        pathway.append(current)
    for path in pathway:
        pass
    return pathway


def algorithm(draw, grid, start, end, game):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {tile: float('inf') for row in grid for tile in row}
    g_score[start] = 0
    f_score = {tile: float('inf') for row in grid for tile in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            # This is where we make sure the game breaks out of the loop when the player wishes to exit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            if game.pathfinding_mode:
                game.pathfinding.pathway = reconstruct_path(came_from, end, draw, True)
            else:
                game.pathfinding.pathway = reconstruct_path(came_from, end, draw)

            end.make_end()
            return True  # make path

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

            draw()

        if current != start:
            current.make_closed()

    return False


def draw_grid(surf, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(surf, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(surf, GREY, (j * gap, 0), (j * gap, width))


def draw_pathfinding(surf, grid, rows, width):
    for row in grid:
        for tile in row:
            tile.draw(surf)


def check_tilemap(tilemap, grid):
    for i in range(1, ROWS):
        for j in range(ROWS):
            path_tile_pos = (i, j)
            if tilemap.get_tile(path_tile_pos) is not None:
                if tilemap.get_tile(path_tile_pos)["type"] != "dirt":
                    grid[i][j].make_barrier()
            else:
                grid[i][j].make_barrier()
            if tilemap.get_tile(path_tile_pos) is None:
                grid[i][j].make_barrier()


class Pathfinding:
    def __init__(self, game):
        self.game = game
        self.pathway = []

    def update(self):
        # NOTE:
        # THIS is getting called every frame I'm pretty sure, and I think we could just call this once at the beginning,
        # and then once anytime the path changes
        check_tilemap(self.game.tilemap, self.game.pf_grid)
        # Here we enter the game loop, it is called "every frame"
        draw_pathfinding(self.game.display, self.game.pf_grid, ROWS, WIDTH)
