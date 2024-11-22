import pygame
from config import screen
from assets import load_assets
from utils.game import jogo


def main():
    background, notas = load_assets()
    jogo(background, notas)
    pygame.quit()

if __name__ == "__main__":
    main()
