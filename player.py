import pygame
from constants import *


class Player:

    def __init__(self):
        super().__init__()

        # Caractéristiques principales du joueur
        self.width = CELL_SIZE / 2  # Taille proportionnelle à la taille des cases
        self.height = self.width
        self.speed = 5 * CELL_SIZE  # Vitesse proportionnelle à la taille des cases
        self.color = RED

        self.rect = pygame.rect.Rect(0, 0, self.width, self.height)

        # Mouvement
        self.vertical_movement = 0
        self.horizontal_movement = 0

    def get_inputs(self):
        # Fonction qui gère les actions du joueur

        # Réinitialisation de la vitesse
        self.horizontal_movement = 0
        self.vertical_movement = 0

        # récupération des actions du clavier
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.horizontal_movement += self.speed

        elif keys[pygame.K_LEFT] or keys[pygame.K_q]:
            self.horizontal_movement -= self.speed

        elif keys[pygame.K_UP] or keys[pygame.K_z]:
            self.vertical_movement -= self.speed

        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.vertical_movement += self.speed

    def draw(self, surface):

        pygame.draw.rect(surface, self.color, self.rect)
