import pygame
import sys

from game import Game
from constants import *

# Initialisation de pygame
pygame.init()

#   Création de la fenêtre du jeu
pygame.display.set_caption('Maze Generator')  # titre de la fenêtre
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# gestion de la vitesse de l'actualisation de l'écran
clock = pygame.time.Clock()

game = Game()

# Boucle principale du jeu
start = False
running = True
while running:
    # on limite le jeu à un certain nombre d'images par secondes
    dt = clock.tick(FPS) / 1000

    # récupération des actions grace aux "events" de pygame
    events = pygame.event.get()
    for event in events:

        # fermeture de la fenêtre
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                start = True

    # Fonction principale du jeu
    game.run(dt, start)


# fermeture de pygame lorsqu'on quitte le jeu
pygame.quit()
sys.exit()
