import pygame
import os

# Inicializar pygame e mixer
pygame.init()
pygame.mixer.init()

# Configurações da tela
screen_width, screen_height = 1024, 1024
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Mini Mozart")

# Cores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (65, 105, 225)
GREEN = (81,224,130)
BLACK = (0, 0, 0)
BEGE = (255, 220, 180)
YELLOW = (255, 223, 0)
PURPLE = (128, 0, 128) 
ORANGE = (255, 165, 0) 
PINK = (255, 105, 180)
ORANGE_RED = (255, 69, 0)  # Vermelho-alaranjado vibrante
LIME_GREEN = (50, 205, 50)  # Verde-limão vibrante

# Configurações do jogo
TEMPO_HABILITADO = True      # Habilita ou desabilita o cronômetro
VIDAS_INICIAIS = 3          # Quantidade inicial de vidas
MUSICA_FUNDO_ATIVADA = True # Habilita ou desabilita a música de fundo
VOLUME_MAXIMO = 0.5         # Volume máximo do jogo (0.0 a 1.0)

# Valores de tempo
TEMPO_GANHO = 8             # Segundos ganhos ao acertar
TEMPO_PERDIDO = 3           # Segundos perdidos ao errar
TEMPO_LIMITE = 30           # Tempo limite em segundos

# Carregar uma fonte personalizada .otf com pygame.font.Font
font = pygame.font.Font('assets/fonts/LapsusPro-Bold.otf', 40)
small_font = pygame.font.Font('assets/fonts/LapsusPro-Bold.otf', 30)

