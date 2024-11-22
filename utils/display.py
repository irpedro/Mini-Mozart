import pygame
import time
import random
from config import screen, font, small_font, screen_width, screen_height, RED, WHITE, BLUE, GREEN, BEGE, BLACK, YELLOW, PURPLE, ORANGE, PINK, ORANGE_RED, LIME_GREEN
from utils.music_sheet import gerar_partitura_abjad

def draw_buttons(buttons, font):
    for nota, rect in buttons.items():
        # Desenha o retângulo do botão
        pygame.draw.rect(screen, BEGE, rect)
        
        # Renderiza o texto centralizado no botão
        texto_botao = font.render(nota, True, BLACK)
        text_x = rect.x + (rect.width - texto_botao.get_width()) // 2
        text_y = rect.y + (rect.height - texto_botao.get_height()) // 2
        screen.blit(texto_botao, (text_x, text_y))

def carregar_imagem_partitura(caminho_imagem):
    try:
        # Carrega a imagem com suporte à transparência
        partitura_img = pygame.image.load(caminho_imagem)
        
        # Ajusta o retângulo da imagem para centralizar na tela
        partitura_rect = partitura_img.get_rect(center=(screen_width // 2, screen_height // 4))
        
        return partitura_img, partitura_rect
    except pygame.error as e:
        print(f"Erro ao carregar a imagem da partitura: {e}")
        return None, None

def desenhar_interface(screen, background, vidas, feedback, feedback_time, pontuacao, combo, partitura_img, partitura_rect, buttons, close_button, tempo_restante):
    if background:
        screen.blit(background, (0, 0))
    
    # Exibe a partitura
    if partitura_img:
        screen.blit(partitura_img, partitura_rect)

    # Exibe o cronômetro
    tempo_texto = small_font.render(f"Tempo Restante: {int(tempo_restante)}s", True, PINK)
    screen.blit(tempo_texto, (screen_width - 320, 20))

    # Exibe a mensagem de errou/acertou, se houver
    if feedback and time.time() - feedback_time <= 2:  # Mensagem dura 1.5 segundos
        feedback_cor = GREEN if feedback == "Acertou!" else RED  # Cor dinâmica
        feedback_render = font.render(feedback, True, feedback_cor)
        screen.blit(feedback_render, ((screen_width - feedback_render.get_width()) // 2.05, partitura_rect.top - 20))

    # Exibe pontuação
    pontuacao_texto = small_font.render(f"Total de Pontos: {pontuacao}", True, BLUE)
    screen.blit(pontuacao_texto, (20, 20))
    
    # Exibe combo
    combo_texto = small_font.render(f"Combo Atual: x{combo}", True, PURPLE)
    screen.blit(combo_texto, (20, 50))

    # Exibe vidas
    vidas_texto = small_font.render(f"Vidas: {vidas}", True, RED)
    screen.blit(vidas_texto, (20, 80))

    # Exibe botões
    draw_buttons(buttons, font)
    
    # Exibe botão de fechar
    pygame.draw.rect(screen, RED, close_button)
    close_text = small_font.render("X", True, WHITE)
    screen.blit(close_text, (close_button.x + 12, close_button.y + 8))

def atualizar_nota_atual(notas, nota_anterior):
    try:
        nota_atual = random.choice(list(notas.keys()))
        while nota_atual == nota_anterior:  # Garante que a nova nota seja diferente da anterior
            nota_atual = random.choice(list(notas.keys()))

        caminho_imagem_partitura = gerar_partitura_abjad(nota_atual)
        if not caminho_imagem_partitura:
            raise ValueError("Erro ao gerar a partitura")
        
        partitura_img, partitura_rect = carregar_imagem_partitura(caminho_imagem_partitura)
        partitura_rect.centerx = screen_width // 2.065
        partitura_rect.top = 230
        return nota_atual, partitura_img, partitura_rect
    except Exception as e:
        print(f"Erro ao atualizar nota: {e}")
        return random.choice(list(notas.keys())), None, None

def exibir_game_over(screen, font, pontuacao, combo_maximo):
    screen.fill((0, 0, 0))  # Preenche o fundo de preto

    # Mensagem principal de Game Over
    mensagem = font.render("Game Over", True, (255, 255, 255))
    mensagem_rect = mensagem.get_rect(center=(screen_width // 2, screen_height // 2 - 100))
    screen.blit(mensagem, mensagem_rect)

    # Exibir pontuação final
    pontuacao_texto = small_font.render(f"Pontuação Final: {pontuacao}", True, (255, 255, 0))  # Texto em amarelo
    pontuacao_rect = pontuacao_texto.get_rect(center=(screen_width // 2, screen_height // 2 - 30))
    screen.blit(pontuacao_texto, pontuacao_rect)

    # Exibir combo máximo
    combo_texto = small_font.render(f"Combo Máximo: x{combo_maximo}", True, (0, 255, 0))  # Texto em verde
    combo_rect = combo_texto.get_rect(center=(screen_width // 2, screen_height // 2 + 10))
    screen.blit(combo_texto, combo_rect)

    # Mensagem auxiliar
    sub_mensagem = small_font.render("Pressione R para reiniciar", True, (200, 200, 200))
    sub_mensagem_rect = sub_mensagem.get_rect(center=(screen_width // 2, screen_height // 2 + 80))
    screen.blit(sub_mensagem, sub_mensagem_rect)

    pygame.display.flip()



