import abjad
import os
import subprocess
from pdf2image import convert_from_path
from PIL import Image

# Configuração do caminho do LilyPond e do Poppler
abjad.configuration.lilypond_path = r"D:\Faculdade\Trabalhos\EI\lilypond-2.24.4\bin\lilypond.exe"
poppler_path = r"C:\Program Files\poppler\Library\bin"

def tornar_fundo_transparente(imagem_path):
    """Remove o fundo branco da imagem e o torna transparente."""
    img = Image.open(imagem_path).convert("RGBA")
    datas = img.getdata()

    nova_imagem = []
    for item in datas:
        # Converte pixels brancos em transparentes
        if item[0] > 200 and item[1] > 200 and item[2] > 200:
            nova_imagem.append((255, 255, 255, 0))  # Transparente
        else:
            nova_imagem.append(item)
    img.putdata(nova_imagem)
    img.save(imagem_path, "PNG")

def cortar_imagem(imagem_path):
    # Corta a imagem para capturar apenas a partitura.
    img = Image.open(imagem_path)
    largura, altura = img.size

    # Defina as coordenadas do box para cortar (valores podem variar)
    # Exemplo: (esquerda, superior, direita, inferior)
    box = (0, 0, largura // 2, altura // 6)  # Ajuste conforme necessário
    img_cortada = img.crop(box)
    img_cortada.save(imagem_path, "PNG")

def gerar_partitura_abjad(nota):
    """Gera uma partitura com a nota especificada e converte para PNG com fundo transparente."""
    notas_abjad = {'Do': "c'", 'Re': "d'", 'Mi': "e'", 'Fa': "f'", 'Sol': "g'", 'La': "a'", 'Si': "b'"}
    nota_abjad = abjad.Note(notas_abjad[nota], (1, 4))
    pentagrama = abjad.Staff([nota_abjad])
    abjad.attach(abjad.Clef('treble'), pentagrama[0])
    partitura = abjad.Score([pentagrama])

    arquivo_ly = "nota_partitura.ly"
    arquivo_pdf = "nota_partitura.pdf"
    abjad.persist.as_ly(partitura, arquivo_ly)

    # Adiciona configurações para ajustar o tamanho da partitura e fundo transparente
    with open(arquivo_ly, "a") as file:
        file.write("\n\\paper {\n    transparent = ##t\n    #(set-paper-size \"a6\")\n}\n")  # Define o tamanho do papel
        file.write("\n#(set-global-staff-size 26)\n")  # Define o tamanho do pentagrama

    try:
        # Executa o LilyPond para gerar o PDF
        subprocess.run([abjad.configuration.lilypond_path, arquivo_ly], check=True)
    except subprocess.CalledProcessError as e:
        print("Erro ao executar o LilyPond:", e)
        return None

    # Verifica se o PDF foi gerado
    if not os.path.exists(arquivo_pdf):
        return None

    try:
        # Converte o PDF para PNG
        imagens = convert_from_path(arquivo_pdf, dpi=300, poppler_path=poppler_path)
        imagem_partitura = "nota_partitura.png"
        imagens[0].save(imagem_partitura, 'PNG')

        # Torna o fundo branco da imagem transparente
        tornar_fundo_transparente(imagem_partitura)
        cortar_imagem(imagem_partitura)

    except Exception as e:
        print(f"Erro na conversão de PDF para PNG: {e}")
        return None

    # Remove os arquivos intermediários (.ly e .pdf)
    os.remove(arquivo_ly)
    os.remove(arquivo_pdf)

    return imagem_partitura
