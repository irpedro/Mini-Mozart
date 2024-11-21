import pygame

def load_assets():
    # Carregar e redimensionar imagem de fundo
    try:
        background = pygame.image.load('assets/images/background.jpg').convert()
        background = pygame.transform.scale(background, (1024, 1024))  # Redimensionar conforme necessário
    except pygame.error as e:
        print(f"Erro ao carregar a imagem de fundo: {e}")
        background = None

    # Carregar sons das notas
    notas = {
        'Do': pygame.mixer.Sound('assets/sounds/nota_C.wav'),
        'Re': pygame.mixer.Sound('assets/sounds/nota_D.wav'),
        'Mi': pygame.mixer.Sound('assets/sounds/nota_E.wav'),
        'Fa': pygame.mixer.Sound('assets/sounds/nota_F.wav'),
        'Sol': pygame.mixer.Sound('assets/sounds/nota_G.wav'),
        'La': pygame.mixer.Sound('assets/sounds/nota_A.wav'),
        'Si': pygame.mixer.Sound('assets/sounds/nota_B.wav')
    }

    # Carregar música de fundo
    try:
        pygame.mixer.music.load('assets/sounds/The Green Orbs - Jigsaw Puzzle (Bright).mp3')  # Substitua pelo caminho correto
    except pygame.error as e:
        print(f"Erro ao carregar a música de fundo: {e}")

    return background, notas
