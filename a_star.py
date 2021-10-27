import pygame
import math

BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
RED      = ( 255,   0,   0)
GREEN    = (   0, 255,   0)
BLUE     = (  25, 120, 250)

WIDTH = 800
HEIGHT = 800
COLS = 100
ROWS = 100
W = WIDTH // COLS
H = HEIGHT // ROWS

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.f = 0
        self.g = 0
        self.h = 0
        self.neighbors = []
        self.prev = None
        self.wall = False
    
    def draw(self, screen, color):
        if self.wall == True:
            color = BLACK
        pygame.draw.rect(screen, color, (self.x * W, self.y * H, W - 1, H - 1))

    def add_neighbors(self, grid):
        if self.x < COLS - 1:
            self.neighbors.append(grid[self.x+1][self.y])
        if self.x > 0:
            self.neighbors.append(grid[self.x-1][self.y])
        if self.y < ROWS - 1:
            self.neighbors.append(grid[self.x][self.y+1])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y-1])

        if self.x < COLS - 1 and self.y < ROWS - 1:
            self.neighbors.append(grid[self.x+1][self.y+1])
        if self.x < COLS - 1 and self.y > 0:
            self.neighbors.append(grid[self.x+1][self.y-1])
        if self.x > 0 and self.y < ROWS - 1:
            self.neighbors.append(grid[self.x-1][self.y+1])
        if self.x > 0 and self.y > 0:
            self.neighbors.append(grid[self.x-1][self.y-1])

def add_wall(pos):
    grid[pos[0] // W][pos[1] // H].wall = True
def remove_wall(pos):
    grid[pos[0] // W][pos[1] // H].wall = False

def heuristic(n, e):
    return math.sqrt((n.x - e.x) ** 2 + abs(n.y - e.y) ** 2)





def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("A* Pathfinder")

    start = grid[0][0]
    end = grid[COLS - COLS // 2][ROWS - COLS // 4]
    open_set = []
    open_set.append(start)
    closed_set = []
    path = []
    finished = False
    begin = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return 0
            if event.type == pygame.MOUSEBUTTONUP:
                if pygame.mouse.get_pressed()[0]:
                    add_wall(pygame.mouse.get_pos())
                if pygame.mouse.get_pressed()[2]:
                    remove_wall(pygame.mouse.get_pos())
            if event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    add_wall(pygame.mouse.get_pos())
                if pygame.mouse.get_pressed()[2]:
                    remove_wall(pygame.mouse.get_pos())
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    begin = True
        if begin == True:
            if len(open_set) > 0:
                lowest_index = 0
                for i in range(len(open_set)):
                    if open_set[i].f < open_set[lowest_index].f:
                        lowest_index = i

                current = open_set[lowest_index]

                if current == end:
                    finished = True
                    temp = current
                    while temp.prev:
                        path.append(temp.prev)
                        temp = temp.prev
                if finished == False:
                    open_set.remove(current)
                    closed_set.append(current)

                    for neighbor in current.neighbors:
                        if neighbor in closed_set or neighbor.wall == True:
                            continue
                        temp_g = current.g + 1

                        new_path = False
                        if neighbor in open_set:
                            if temp_g < neighbor.g:
                                neighbor.g = temp_g
                                new_path = True
                        else:
                            neighbor.g = temp_g
                            new_path = True
                            open_set.append(neighbor)
                        if new_path == True:
                            neighbor.h = heuristic(neighbor, end)
                            neighbor.f = neighbor.g + neighbor.h
                            neighbor.prev = current
        screen.fill((0, 20, 20))
        for i in range(COLS):
            for j in range(ROWS):
                point = grid[j][i]
                point.draw(screen, WHITE)
                if finished and point in path:
                    point.draw(screen, BLUE)
                elif point in closed_set:
                    point.draw(screen, RED)
                elif point in open_set:
                    point.draw(screen, GREEN)
                try:
                    if point == end:
                        point.draw(screen, BLUE)
                except Exception:
                    pass
                
        pygame.display.flip()


if __name__ == "__main__":
    grid = []

    for i in range(COLS):
        temp = []
        for j in range(ROWS):
            temp.append(Point(i, j))
        grid.append(temp)

    for i in range(COLS):
        for j in range(ROWS):
            grid[i][j].add_neighbors(grid)
    main()