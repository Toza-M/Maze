import pygame

width, height = 450, 500
rows, cols = 30, 30
cell_size = width // height

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
LIGHTBLUE = (173, 216, 230)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GREY = (220, 220, 220)

pygame.init() 
screen = pygame.display.set_mode((width, height+40)) # +40 for write the approaches at the bottom of the screen
pygame.display.set_caption("Maze Genreator & Solver")
icon = pygame.image.load("Icon.png")
pygame.display.set_icon(icon)

class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.wall = [True, True, True, True]
        self.visted = False
        self.x = col * cell_size
        self.y = row * cell_size
        
    def draw(self, surface, color=WHITE):
        if color != WHITE: 
            pygame.draw.rect(surface, color, (self.x, self.y, cell_size, cell_size)) # cell_size appears twice to define the start and end
        
        if self.wall[0]:
            pygame.draw.line(surface, BLACK, (self.x, self.y), (self.x+cell_size, self.y), 2) # top
        if self.wall[1]:
            pygame.draw.line(surface, BLACK, (self.x+cell_size, self.y), (self.x+cell_size, self.y+cell_size), 2) # right
        if self.wall[2]:
            pygame.draw.line(surface, BLACK, (self.x, self.y+cell_size), (self.x+cell_size, self.y+cell_size), 2) # bottom
        if self.wall[3]:
            pygame.draw.line(surface, BLACK, (self.x, self.y), (self.x, self.y+cell_size), 2) # left
            

        
        
        
def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
                
main()