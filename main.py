import pygame
import random
import heapq
import itertools



width, height = 450, 450
rows, cols = 30, 30
cell_size = width // cols
bottom_panel = 40


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (220, 220, 220)

# Set up of the window
pygame.init()
screen = pygame.display.set_mode((width, height + bottom_panel))
pygame.display.set_caption("Maze Generator & Solver")
icon = pygame.image.load("Icon.png")
pygame.display.set_icon(icon)
font = pygame.font.SysFont("Arial", 18)

class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.wall = [True, True, True, True]
        self.visited = False
        self.x = col * cell_size
        self.y = row * cell_size

    def draw(self, surface, color=BLACK):
        # Draw the window with black bakground and white walls
        if color != BLACK:
            pygame.draw.rect(surface, color, (self.x, self.y, cell_size, cell_size))
        if self.wall[0]:
            pygame.draw.line(surface, WHITE, (self.x, self.y), (self.x+cell_size, self.y), 2)
        if self.wall[1]:
            pygame.draw.line(surface, WHITE, (self.x+cell_size, self.y), (self.x+cell_size, self.y+cell_size), 2)
        if self.wall[2]:
            pygame.draw.line(surface, WHITE, (self.x, self.y+cell_size), (self.x+cell_size, self.y+cell_size), 2)
        if self.wall[3]:
            pygame.draw.line(surface, WHITE, (self.x, self.y), (self.x, self.y+cell_size), 2)

    def __hash__(self):
        return hash((self.row, self.col))

    def __eq__(self, other):
        return isinstance(other, Cell) and self.row == other.row and self.col == other.col

def make_grid():
    # grid == 2D list
    return [[Cell(r, c) for c in range(cols)] for r in range(rows)]

def remove_walls(a, b):
    dx = b.col - a.col
    dy = b.row - a.row
    if dx == 1:
        a.wall[1] = False
        b.wall[3] = False
    elif dx == -1:
        a.wall[3] = False
        b.wall[1] = False
    if dy == 1:
        a.wall[2] = False
        b.wall[0] = False
    elif dy == -1:
        a.wall[0] = False
        b.wall[2] = False

def get_neighbors(cell, grid):
    neighbors = []
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    r, c = cell.row, cell.col
    for dx, dy in directions:
        nr, nc = r + dy, c + dx
        if 0 <= nr < rows and 0 <= nc < cols:
            neighbors.append(grid[nr][nc])
    return neighbors

def generate_maze(grid):
    stack = []
    current = grid[0][0]
    current.visited = True
    stack.append(current)
    while stack:
        current = stack[-1]
        neighbors = [n for n in get_neighbors(current, grid) if not n.visited]
        if neighbors:
            next_cell = random.choice(neighbors)
            remove_walls(current, next_cell)
            next_cell.visited = True
            stack.append(next_cell)
        else:
            stack.pop()

def draw_grid(grid):
    for row in grid:
        for cell in row:
            cell.draw(screen)

def draw_path_step_by_step(path, delay=0.01):
    for cell in path:
        pygame.draw.rect(screen, WHITE, (cell.col * cell_size + 3, cell.row * cell_size + 3, cell_size - 6, cell_size - 6))
        pygame.display.update()
        pygame.time.delay(int(delay * 1000))

def neighbors_no_walls(cell, grid):
    result = []
    r, c = cell.row, cell.col
    if not cell.wall[0] and r > 0:
        result.append(grid[r - 1][c])
    if not cell.wall[1] and c < cols - 1:
        result.append(grid[r][c + 1])
    if not cell.wall[2] and r < rows - 1:
        result.append(grid[r + 1][c])
    if not cell.wall[3] and c > 0:
        result.append(grid[r][c - 1])
    return result

def reconstruct_path(came_from, current):
    path = []
    while current in came_from:
        path.append(current)
        current = came_from[current]
    path.append(current)
    path.reverse()
    return path

def heuristic(a, b):
    return abs(a.row - b.row) + abs(a.col - b.col)

def regenerate_maze():
    grid = make_grid()
    generate_maze(grid)
    return grid

def a_star(start, goal, grid):
    open_set = []
    count = itertools.count()
    heapq.heappush(open_set, (0, next(count), start))
    came_from = {}
    g_score = {cell: float('inf') for row in grid for cell in row}
    g_score[start] = 0
    f_score = {cell: float('inf') for row in grid for cell in row}
    f_score[start] = heuristic(start, goal)
    open_set_hash = {start}
    while open_set:
        current = heapq.heappop(open_set)[2]
        open_set_hash.remove(current)
        if current == goal:
            return reconstruct_path(came_from, current)
        for neighbor in neighbors_no_walls(current, grid):
            temp_g_score = g_score[current] + 1
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic(neighbor, goal)
                if neighbor not in open_set_hash:
                    heapq.heappush(open_set, (f_score[neighbor], next(count), neighbor))
                    open_set_hash.add(neighbor)
    return []








def bfs(start, goal, grid):
    pass

def dfs(start, goal, grid):
    pass






def main():
    algo = None
    path = []
    solved = False

    grid = regenerate_maze()
    start = grid[0][0]
    goal = grid[rows - 1][cols - 1]

    running = True
    while running:
        screen.fill(BLACK)
        draw_grid(grid)

        if path and solved:
            draw_path_step_by_step(path)
            solved = False

        # Draw bottom panel
        pygame.draw.rect(screen, GREY, (0, height, width, bottom_panel))
        algo_name = algo if algo else "None"
        label = font.render(f"Algorithm: {algo_name} | Press 1=A*, 2=BFS, 3=DFS, R=Reset", True, BLACK)
        screen.blit(label, (10, height + 10))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    grid = regenerate_maze()
                    start = grid[0][0]
                    goal = grid[rows - 1][cols - 1]
                    path = []
                    algo = None
                    solved = False

                elif event.key == pygame.K_1:
                    algo = "A*"
                    path = a_star(start, goal, grid)
                    solved = True

                elif event.key == pygame.K_2:
                    algo = "BFS"
                    path = bfs(start, goal, grid)
                    solved = True

                elif event.key == pygame.K_3:
                    algo = "DFS"
                    path = dfs(start, goal, grid)
                    solved = True

main()
