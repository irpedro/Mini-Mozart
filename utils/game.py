import pygame
import random
import time

# Importa variáveis específicas do módulo config
from config import (
    screen, font, small_font, screen_width, screen_height,
    RED, WHITE, BLUE, GREEN, BEGE,
    VIDAS_INICIAIS, MUSICA_FUNDO_ATIVADA, VOLUME_MAXIMO, 
    TEMPO_HABILITADO, TEMPO_GANHO, TEMPO_PERDIDO, TEMPO_LIMITE
)

# Importa funções específicas do módulo display
from utils.display import (
    draw_buttons, carregar_imagem_partitura, 
    desenhar_interface, atualizar_nota_atual, 
    exibir_game_over
)

# Importa partiruras do módulo music_sheet
from utils.music_sheet import gerar_partitura_abjad

def tocar_nota(nota, notas):
    notas[nota].play()

def configurar_jogo(notas):
    vidas = 3
    feedback = ""
    feedback_time = 0
    pontuacao = 0  # Inicializa a pontuação
    combo = 0  # Inicializa o combo
    
    # Escolhe uma nota aleatória e gera o caminho da imagem
    nota_atual = random.choice(list(notas.keys()))
    caminho_imagem_partitura = gerar_partitura_abjad(nota_atual)
    
    # Carrega a imagem da partitura
    partitura_img, partitura_rect = carregar_imagem_partitura(caminho_imagem_partitura)
    partitura_rect.centerx = screen_width // 2.065  # Centraliza horizontalmente
    partitura_rect.top = 230  # Define um espaço superior desde o início

    # Configura os botões centralizados
    button_width, button_height = 100, 50
    total_width = len(notas) * (button_width + 20) - 20  # Calcula largura total dos botões
    start_x = (screen_width - total_width) // 2  # Define o ponto inicial para centralizar
    buttons = {
        nota: pygame.Rect(start_x + i * (button_width + 20), screen_height - 100, button_width, button_height)
        for i, nota in enumerate(notas.keys())
    }
    
    # Configura o botão de fechar
    close_button = pygame.Rect(screen_width - 50, 10, 40, 40)
    
    return vidas, feedback, feedback_time, pontuacao, combo, nota_atual, partitura_img, partitura_rect, buttons, close_button

def processar_eventos(
    buttons, close_button, nota_atual, notas, feedback,
    feedback_time, vidas, pontuacao, combo, partitura_img,
    partitura_rect, tempo_restante, tempo_ganho, tempo_perdido, tempo_habilitado
):
    rodando = True
    key_to_note = {
        pygame.K_a: 'Do', pygame.K_s: 'Re', pygame.K_d: 'Mi',
        pygame.K_f: 'Fa', pygame.K_j: 'Sol', pygame.K_k: 'La', pygame.K_l: 'Si',
    }

    def avaliar_nota(nota_selecionada, nota_correta):
        #Avalia se a nota tocada está correta e atualiza as variáveis.
        nonlocal nota_atual, partitura_img, partitura_rect
        nonlocal feedback, feedback_time, combo, pontuacao, vidas, tempo_restante
        
        tocar_nota(nota_selecionada, notas)
        if nota_selecionada == nota_correta:
            # Atualiza a nota, partitura e informações relacionadas
            nota_atual, partitura_img, partitura_rect = atualizar_nota_atual(notas, nota_correta)
            feedback = "Acertou!"
            combo += 1
            pontuacao += 100 * combo
            if tempo_habilitado:
                tempo_restante += tempo_ganho
        else:
            feedback = "Errou!"
            combo = 0
            vidas -= 1
            if tempo_habilitado:
                tempo_restante -= tempo_perdido
        feedback_time = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if close_button.collidepoint(event.pos):
                rodando = False
            else:
                for nota, rect in buttons.items():
                    if rect.collidepoint(event.pos):
                        avaliar_nota(nota, nota_atual)
        elif event.type == pygame.KEYDOWN and event.key in key_to_note:
            avaliar_nota(key_to_note[event.key], nota_atual)

    # Limpa o feedback se já passou o tempo
    if feedback and time.time() - feedback_time > 1.5:
        feedback = ""

    # Garante que o tempo não fique negativo
    if tempo_habilitado:
        tempo_restante = max(tempo_restante, 0)

    return (
        rodando, feedback, feedback_time, vidas,
        pontuacao, combo, nota_atual, partitura_img,
        partitura_rect, tempo_restante
    )

def jogo(background, notas):
    if MUSICA_FUNDO_ATIVADA:
        pygame.mixer.music.set_volume(VOLUME_MAXIMO)
        pygame.mixer.music.play(-1)

    vidas = VIDAS_INICIAIS
    feedback = ""
    feedback_time = 0
    pontuacao = 0
    combo = 0
    tempo_restante = 30 if TEMPO_HABILITADO else None  # Apenas inicia o cronômetro se habilitado

    # Configuração inicial do jogo
    vidas, feedback, feedback_time, pontuacao, combo, nota_atual, partitura_img, partitura_rect, buttons, close_button = configurar_jogo(notas)
    game_over = False
    rodando = True
    combo_maximo = 0
    ultimo_tempo = time.time()

    while rodando:
        if not game_over:

            # Atualiza o cronômetro se habilitado
            if TEMPO_HABILITADO:
                tempo_atual = time.time()
                tempo_restante -= tempo_atual - ultimo_tempo
                ultimo_tempo = tempo_atual
                if tempo_restante <= 0:
                    tempo_restante = 0  # Garante que o tempo não fique negativo
                    game_over = True
                elif tempo_restante > TEMPO_LIMITE:
                    tempo_restante = TEMPO_LIMITE  # Limita o tempo ao valor máximo

            # Atualiza o maior combo
            if combo > combo_maximo:
                combo_maximo = combo

            # Desenha a interface
            desenhar_interface(
                screen, background, vidas, feedback, feedback_time, pontuacao, combo,
                partitura_img, partitura_rect, buttons, close_button, tempo_restante
            )

            # Processa eventos
            rodando, feedback, feedback_time, vidas, pontuacao, combo, nota_atual, partitura_img, partitura_rect, tempo_restante = processar_eventos(
                buttons, close_button, nota_atual, notas, feedback, feedback_time,
                vidas, pontuacao, combo, partitura_img, partitura_rect, tempo_restante,
                TEMPO_GANHO, TEMPO_PERDIDO, TEMPO_HABILITADO
            )

            if vidas <= 0:
                game_over = True
        else:
            exibir_game_over(screen, font, pontuacao, combo_maximo)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    rodando = False

                # Reinicia o jogo
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r: 
                    vidas = VIDAS_INICIAIS
                    feedback = ""
                    feedback_time = 0
                    pontuacao = 0
                    combo = 0
                    tempo_restante = 30 if TEMPO_HABILITADO else None
                    game_over = False

        pygame.display.flip()

    pygame.mixer.music.stop()
