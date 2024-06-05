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


def reconstruct_path(came_from, current, draw):
    pathway = []
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()
        pathway.append(current)
    for path in pathway:
        print(str(path.row) + ";" + str(path.col))


def algorithm(draw, grid, start, end):
    print("We are calling algorithm")
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
                print("We are exiting")
                pygame.quit()
                sys.exit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True # make path

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
                    print("We just made our neighbor open")

            draw()
            print("We just called draw pathfinding in our algorithm")

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
    print("We called draw_pathfinding")
    for row in grid:
        for tile in row:
            tile.draw(surf)


def check_tilemap(tilemap, grid):
    for i in range(1, ROWS):
        for j in range(ROWS):
            path_tile_pos = (i, j)
            if tilemap.get_tile(path_tile_pos) is not None:
                if tilemap.get_tile(path_tile_pos)["type"] == "grass":
                    grid[i][j].make_barrier()


class Pathfinding:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("pathfinding")

        self.SCREEN_WIDTH = pygame.display.get_desktop_sizes()[0][0]
        self.SCREEN_HEIGHT = pygame.display.get_desktop_sizes()[0][1]
        print(pygame.display.get_desktop_sizes()[0][0], pygame.display.get_desktop_sizes()[0][1])

        self.bg_color = (25, 25, 25)

        # screen is now a "Surface" as that is the return type from setting the display mode
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        # screen is now a "Surface" as that is the return type from setting the display mode
        self.screen = pygame.display.set_mode(
            (pygame.display.get_desktop_sizes()[0][0], pygame.display.get_desktop_sizes()[0][1]))

        # Here we will initialize 16 x 9 ratios (My PC)
        if self.screen.get_size()[0] == 2560 and self.screen.get_size()[1] == 1440:
            self.display = pygame.Surface((640, 360))

        # Here we will initialize 16 x 10 ratios (My Laptop)
        if self.screen.get_size()[0] == 1440 and self.screen.get_size()[1] == 900:
            self.display = pygame.Surface((640, 360))

        self.clock = pygame.time.Clock()

        self.tile_size = 16

        # here we will import all the assets we need in our game at runtime
        self.assets = {
            'pathfinding': load_images("pathfinding"),
            'grass': load_images("grass"),
            'dirt': load_images("dirt")
        }

        # here is where we initialize our tilemap
        self.tilemap = Tilemap(self, tile_size=16)
        filepath = r"data"
        try:
            if os.path.exists(filepath):
                print('loaded tilemap successfully')
                self.tilemap.load("data/map.json")
            else:
                print("File not found: " + filepath)
        except FileNotFoundError:
            print("File not found: " + filepath)
        except PermissionError:
            print("Did not have permission to load file")

        self.clicking = False
        self.right_clicking = False
        self.shift = False

    def run(self):
        # Here is where we handle drawing our pathfinding stuff

        grid = make_grid(ROWS, WIDTH)
        check_tilemap(self.tilemap, grid)

        start = None
        end = None

        started = False

        # Here we enter the game loop, it is called "every frame"
        while True:
            # Here is where we can draw our background
            self.screen.fill(self.bg_color)
            self.display.fill(self.bg_color)
            self.tilemap.render(self.display)
            draw_pathfinding(self.display, grid, ROWS, WIDTH)
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 16))
            # self.screen.blit(pygame.transform.scale(self.pf_display, self.screen.get_size()), (0, 16))


            mpos = pygame.mouse.get_pos()
            mpos = (mpos[0] / RENDER_SCALE, (mpos[1] / RENDER_SCALE) - 8)
            m_tile_pos = (int(mpos[0] // self.tilemap.tile_size), int(mpos[1] // self.tilemap.tile_size))

            # This is the event checker for each frame
            for event in pygame.event.get():
                # This is where we make sure the game breaks out of the loop when the player wishes to exit
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if started:
                    continue
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True
                        row = m_tile_pos[0]
                        col = m_tile_pos[1]
                        tile = grid[row][col]
                        if not start and tile != end:
                            print('start made')
                            start = tile
                            start.make_start()
                        elif not end and tile != start:
                            end = tile
                            end.make_end()
                        elif tile != end and tile != start:
                            tile.make_barrier()

                    if event.button == 3:
                        self.right_clicking = True
                        row = m_tile_pos[0]
                        col = m_tile_pos[1]
                        tile = grid[row][col]
                        tile.reset()
                        if tile == start:
                            start = None
                        if tile == end:
                            end = None
                    if self.shift:
                        if event.button == 4:
                            pass
                        if event.button == 5:
                            pass
                    else:
                        if event.button == 4:
                            pass
                        if event.button == 5:
                            pass
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
                    if event.button == 3:
                        self.right_clicking = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        pass
                    if event.key == pygame.K_RIGHT:
                        pass
                    if event.key == pygame.K_UP:
                        pass
                    if event.key == pygame.K_DOWN:
                        pass
                    if event.key == pygame.K_LSHIFT:
                        self.shift = True
                    if event.key == pygame.K_SPACE:
                        if not started:
                            for row in grid:
                                for tile in row:
                                    tile.update_neighbors(grid)

                            algorithm(lambda: draw_pathfinding(self.display, grid, ROWS, WIDTH), grid, start, end)

                    if event.key == pygame.K_g:
                        pass
                    if event.key == pygame.K_o:
                        pass
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        pass
                    if event.key == pygame.K_RIGHT:
                        pass
                    if event.key == pygame.K_UP:
                        pass
                    if event.key == pygame.K_DOWN:
                        pass
                    if event.key == pygame.K_LSHIFT:
                        self.shift = False

            pygame.display.update()
            self.clock.tick(FPS)


Pathfinding().run()
