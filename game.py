import pygame
import random

from constants import *
from player import Player
from cell import Cell


class Game:
    # Classe qui gère le jeu lorsque le joueur est dans un niveau

    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        self.bg_color = BLACK

        # Grille des cases du labyrinthe
        self.grid_x = (WINDOW_WIDTH - MAZE_WIDTH) / 2
        self.grid_y = (WINDOW_HEIGHT - MAZE_HEIGHT) / 2
        self.grid = []
        for y_index in range(HEIGHT):
            y = y_index * CELL_SIZE + self.grid_y
            line = []
            for x_index in range(WIDTH):
                x = x_index * CELL_SIZE + self.grid_x
                line.append(Cell(x, y))
            self.grid.append(line)

        # Choix aléatoire de la première case
        x = random.randint(0, WIDTH - 1)
        y = random.randint(0, HEIGHT - 1)
        self.visited_cells = [self.grid[y][x]]

        self.maze_complete = False

        # Player setup
        self.player = Player()
        self.player.rect.x = self.grid_x + CELL_SIZE / 4
        self.player.rect.y = self.grid_y + CELL_SIZE / 4

    def draw_grid(self, surface):
        # Affiche le labyrinthe

        grid = self.grid
        for line in grid:
            for cell in line:
                cell.draw(surface)

    def create_passage(self, cell1, cell2):
        # breaks the wall between 2 adjacent cells

        x1 = int((cell1.x - self.grid_x) // CELL_SIZE)
        y1 = int((cell1.y - self.grid_y) // CELL_SIZE)
        x2 = int((cell2.x - self.grid_x) // CELL_SIZE)
        y2 = int((cell2.y - self.grid_y) // CELL_SIZE)

        if x1 < x2:
            cell1.walls['right'] = False
            cell2.walls['left'] = False
        elif x2 < x1:
            cell1.walls['left'] = False
            cell2.walls['right'] = False
        elif y1 < y2:
            cell1.walls['bottom'] = False
            cell2.walls['top'] = False
        elif y2 < y1:
            cell1.walls['top'] = False
            cell2.walls['bottom'] = False

    def select_neighbor(self, cell):
        # Renvoie une case adjacente qui n'a pas été visitée, s'il n'y en a pas : renvoie None

        x_index = int((cell.x - self.grid_x) // CELL_SIZE)
        y_index = int((cell.y - self.grid_y) // CELL_SIZE)
        possible_cells = []

        if y_index > 0:
            cell = self.grid[y_index - 1][x_index]
            if cell not in self.visited_cells:
                possible_cells.append(cell)
        if y_index < HEIGHT - 1:
            cell = self.grid[y_index + 1][x_index]
            if cell not in self.visited_cells:
                possible_cells.append(cell)
        if x_index > 0:
            cell = self.grid[y_index][x_index - 1]
            if cell not in self.visited_cells:
                possible_cells.append(cell)
        if x_index < WIDTH - 1:
            cell = self.grid[y_index][x_index + 1]
            if cell not in self.visited_cells:
                possible_cells.append(cell)

        if len(possible_cells) > 0:
            i = random.randint(0, len(possible_cells) - 1)
            return possible_cells[i]
        else:
            return None

    def maze_generation_step(self):
        # Effectue une étape de génération du labyrinthe en cassant un mur
        # Utilise l'algorithme 'growing tree' avec un 'backtracker' récursif lorsqu'il est bloqué

        i = -1
        new_cell = None

        while new_cell is None:  # Revient en arrière de manière jusqu'à trouver un chemin qui n'a pas déjà été pris
            current_cell = self.visited_cells[i]
            new_cell = self.select_neighbor(current_cell)
            i -= 1
            if -i == WIDTH * HEIGHT:  # On vérifie si le labyrinthe est terminé
                self.maze_complete = True
                break

        if not self.maze_complete:
            self.visited_cells.append(new_cell)
            self.create_passage(current_cell, new_cell)

    def player_collision(self, dt):

        x = int((self.player.rect.centerx - self.grid_x) // CELL_SIZE)
        y = int((self.player.rect.centery - self.grid_y) // CELL_SIZE)
        x_left = int((self.player.rect.left - self.grid_x) // CELL_SIZE)
        x_right = int((self.player.rect.right - self.grid_x - 1) // CELL_SIZE)
        y_top = int((self.player.rect.top - self.grid_y) // CELL_SIZE)
        y_bottom = int((self.player.rect.bottom - self.grid_y - 1) // CELL_SIZE)

        #   Collisions Horizontales
        x_offset = self.player.horizontal_movement * dt
        if x_offset > 0:  # le joueur va vers la droite
            next_x = int((self.player.rect.right + x_offset - self.grid_x) // CELL_SIZE)
            if next_x == x_right or (next_x <= WIDTH - 1
                                     and not self.grid[y][x].walls['right']
                                     and y_top == y_bottom):
                self.player.rect.x += x_offset
        elif x_offset < 0:  # le joueur va vers la gauche
            next_x = int((self.player.rect.left + x_offset - self.grid_x - 1) // CELL_SIZE)
            if next_x == x_left or (next_x >= 0
                                    and not self.grid[y][x].walls['left']
                                    and y_top == y_bottom):
                self.player.rect.x += x_offset

        #   Collisions Verticales
        y_offset = self.player.vertical_movement * dt
        if y_offset > 0:  # le joueur va vers le bas
            next_y = (self.player.rect.bottom + y_offset - self.grid_y) // CELL_SIZE
            if next_y == y_bottom or (next_y <= (HEIGHT - 1)
                                      and not self.grid[y][x].walls['bottom']
                                      and x_left == x_right):
                self.player.rect.y += y_offset
        elif y_offset < 0:  # le joueur va vers le haut
            next_y = (self.player.rect.top + y_offset - self.grid_y - 1) // CELL_SIZE
            if next_y == y_top or (next_y >= 0
                                   and not self.grid[y][x].walls['top']
                                   and x_right == x_left):
                self.player.rect.y += y_offset

    def run(self, dt, start):
        # Fonction principale qui fait tourner le jeu dans les niveaux

        # Arrière-plan :
        self.display_surface.fill(self.bg_color)

        # Labyrinthe
        self.draw_grid(self.display_surface)

        if self.maze_complete:

            # Actualisation du joueur :
            self.player.get_inputs()

            # Collisions du joueur
            self.player_collision(dt)

            # Affichage du joueur
            self.player.draw(self.display_surface)

        elif start:
            nb_tiles = WIDTH * HEIGHT
            for i in range((nb_tiles // 500) + 1):  # Accélération de la génération pour les labyrinthes plus grands
                self.maze_generation_step()

        # Actualisation de l'écran
        pygame.display.flip()
