import pygame
import random
import requests
import time
from preguntes import PreRes, ResCor

# Inicialitzem Pygame
pygame.init()

# Conexió amb servidor
resposta = requests.get("https://fun.codelearn.cat/hackathon/game/new")
dades = resposta.json()

seed = dades["seed"]
print(seed)
game_id = dades["game_id"]
print(game_id)

random.seed(seed)

# Constants de la finestra
AMPLADA = 800
ALCADA = 600
finestra = pygame.display.set_mode((AMPLADA, ALCADA))
pygame.display.set_caption("Laberint de problemes")

# Colors (R, G, B)
VERMELL = (255, 0, 0)
VERD = (0, 255, 0)
BLAU = (0, 0, 255)
GROC = (255, 255, 0)
NEGRE = (0, 0, 0)

preguntesJoc = []
respostesJoc = []

def prepara_preguntes(ultima_pregunta=None):
    global preguntesJoc, respostesJoc
    while True:
        preguntesJoc = []
        respostesJoc = []
        indexos = random.sample(range(len(PreRes)), 10)
        if ultima_pregunta is not None:
            # Comprova que la primera pregunta no sigui la mateixa que l'última vista
            if PreRes[indexos[0]][0] == ultima_pregunta:
                continue
        for idx in indexos:
            preguntesJoc.append(PreRes[idx])
            respostesJoc.append(ResCor[idx])
        break

p1 = p2 = p3 = p4 = p5 = p6 = p7 = p8 = p9 = p10 = False

# Dimensions de les portes
ample_porta = 160
alt_porta = 350
espai_entre_portes = 20

# Llista de colors per a les portes
colors_portes = [VERMELL, VERD, BLAU, GROC]

# Càlcul per centrar les portes
total_amplada_portes = 4 * ample_porta + 3 * espai_entre_portes
marge_lateral = (AMPLADA - total_amplada_portes) // 2

# Font per al text
font = pygame.font.SysFont(None, 36)

# Funció colocar portes i pregunta
def portes():
    # Pintem el fons de blanc
    finestra.fill((255, 255, 255))

    # Dibuixem la puntuació a la cantonada superior dreta
    puntuacio_text = font.render(f"Punts: {score}", True, (0, 0, 0))
    finestra.blit(puntuacio_text, (AMPLADA - 200, 20))

    # Dibuixem les quatre portes centrades amb text
    for i in range(4):
        x = marge_lateral + i * (ample_porta + espai_entre_portes)
        y = (ALCADA - alt_porta) // 2 - 30
        pygame.draw.rect(finestra, colors_portes[i], (x, y, ample_porta, alt_porta))
        
        lines = wrap_text(preguntesJoc[a][i + 1], font, ample_porta - 2)

        # Dibuixar línia per línia
        for line in lines:
            text_surface = font.render(line, True, NEGRE)
            text_rect = text_surface.get_rect(center=(x + ample_porta // 2, y + alt_porta // 2))
            finestra.blit(text_surface, text_rect)
            y += text_surface.get_height() + 5  # Espai entre línies

    y = (ALCADA - alt_porta) // 2 - 30
    lines = wrap_text(preguntesJoc[a][0], font, AMPLADA - 20)

    # Dibuixar línia per línia
    for line in lines:
        text_surface = font.render(line, True, NEGRE)
        text_rect = text_surface.get_rect(center=(AMPLADA // 2, y + alt_porta + 40))
        finestra.blit(text_surface, text_rect)
        y += text_surface.get_height() + 5  # Espai entre línies

def pantalla_inici():
    a = 0
    p1 = p2 = p3 = p4 = p5 = p6 = p7 = p8 = p9 = p10 = False
    boto_amplada = 200
    boto_alcada = 60
    boto_color = (0, 200, 0)
    boto_color_hover = (0, 255, 0)
    titol_font = pygame.font.SysFont(None, 72)
    boto_font = pygame.font.SysFont(None, 48)
    titol = titol_font.render("Laberint de problemes", True, (0, 0, 128))
    titol_rect = titol.get_rect(center=(AMPLADA // 2, ALCADA // 2 - 100))
    boto_rect = pygame.Rect((AMPLADA - boto_amplada) // 2, (ALCADA - boto_alcada) // 2 + 50, boto_amplada, boto_alcada)
    boto_text = boto_font.render("Start", True, (255, 255, 255))
    boto_text_rect = boto_text.get_rect(center=boto_rect.center)

    inici = True
    while inici:
        finestra.fill((255, 255, 255))
        finestra.blit(titol, titol_rect)

        mouse = pygame.mouse.get_pos()
        if boto_rect.collidepoint(mouse):
            color = boto_color_hover
        else:
            color = boto_color

        pygame.draw.rect(finestra, color, boto_rect, border_radius=10)
        finestra.blit(boto_text, boto_text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if boto_rect.collidepoint(event.pos):
                    inici = False

        pygame.display.flip()


def wrap_text(text, font, max_width):
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + " " + word if current_line else word
        text_surface = font.render(test_line, True, NEGRE)
        if text_surface.get_width() <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines

def reset_joc():
    global a, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, cop, respostaCorrecte
    a = 0
    p1 = p2 = p3 = p4 = p5 = p6 = p7 = p8 = p9 = p10 = False
    cop = 0
    respostaCorrecte = False

score = 100  # Puntuació inicial

# Nova variable per controlar la freqüència d'enviament (en segons)
ENVIAMENT_INTERVAL = 10
ultim_enviament = time.time()

def envia_estat_joc(game_id, pregunta_actual, encerts, score, forcat=False):
    global ultim_enviament
    ara = time.time()
    if not forcat and ara - ultim_enviament < ENVIAMENT_INTERVAL:
        return  # No enviïs encara
    url = "https://fun.codelearn.cat/hackathon/game/store_progress"
    dades = {
        "game_id": game_id,
        "data": {
            "pregunta_actual": pregunta_actual,
            "encerts": encerts,
            "score": score
        }
    }
    try:
        resposta = requests.post(url, json=dades)
        if resposta.headers.get("Content-Type", "").startswith("application/json"):
            resposta_json = resposta.json()
            print("Resposta servidor:", resposta_json)
        else:
            print("Resposta no JSON:", resposta.text)
    except Exception as e:
        print("Error enviant estat:", e)
    ultim_enviament = ara

def envia_final_joc(game_id, encerts, score):
    url = "https://fun.codelearn.cat/hackathon/game/finalize"
    dades = {
        "game_id": game_id,
        "data": {
            "encerts": encerts
        },
        "score": score
    }
    try:
        resposta = requests.post(url, json=dades)
        if resposta.headers.get("Content-Type", "").startswith("application/json"):
            resposta_json = resposta.json()
            print("Finalització servidor:", resposta_json)
        else:
            print("Resposta no JSON:", resposta.text)
    except Exception as e:
        print("Error finalitzant joc:", e)

def pantalla_victoria():
    finestra.fill((255, 255, 255))
    font_gran = pygame.font.SysFont(None, 72)
    text = font_gran.render("Has sortit del laberint!", True, (0, 128, 0))
    text_rect = text.get_rect(center=(AMPLADA // 2, ALCADA // 2))
    finestra.blit(text, text_rect)
    pygame.display.flip()
    envia_final_joc(game_id, sum([p1, p2, p3, p4, p5, p6, p7, p8, p9, p10]), score)
    pygame.time.wait(3000)  # Espera 3 segons

def comprovacio():
    if p1:
        if p2:
            if p3:
                if p4:
                    if p5:
                        if p6:
                            if p7:
                                if p8:
                                    if p9:
                                        if p10:
                                            print("Has sortit del laberint")
                                            pantalla_victoria()
                                            executant = False
                                    else:
                                        a = 8
                                else:
                                    a = 7
                            else:
                                a = 6
                        else:
                            a = 5
                    else:
                        a = 4
                else:
                    a = 3
            else:
                a = 2
        else:
            a = 1
    else:
        a = 0

def reinicia_partida(ultima_pregunta=None):
    global a, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, respostaCorrecte, preguntesJoc, respostesJoc
    a = 0
    p1 = p2 = p3 = p4 = p5 = p6 = p7 = p8 = p9 = p10 = False
    respostaCorrecte = False
    prepara_preguntes(ultima_pregunta)

# Pantalla d'inici abans del bucle principal
pantalla_inici()

# Prepara preguntes abans de començar el joc!
prepara_preguntes()

# Bucle principal

cop = 0
a = 0
respostaCorrecte = False

# Variable per controlar si s'han encertat totes
encertades_seguides = 0

executant = True
while executant:
    for esdeveniment in pygame.event.get():
        if esdeveniment.type == pygame.QUIT:
            executant = False
        elif esdeveniment.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = esdeveniment.pos
            for i in range(4):
                x = marge_lateral + i * (ample_porta + espai_entre_portes)
                y = (ALCADA - alt_porta) // 2 - 30
                porta_rect = pygame.Rect(x, y, ample_porta, alt_porta)
                if porta_rect.collidepoint(mouse_x, mouse_y):
                    print("Resposta escollida:", preguntesJoc[a][i + 1])
                    print("Resposta correcta:", respostesJoc[a])
                    if preguntesJoc[a][i + 1] == respostesJoc[a]:
                        respostaCorrecte = True
                        encertades_seguides += 1
                    else:
                        if score > 30:
                            score = max(30, score - 5)
                        print("Has fallat! Torna a començar.")
                        reinicia_partida(preguntesJoc[a][0])
                        encertades_seguides = 0
                        portes()
                        envia_estat_joc(game_id, a, 0, score, forcat=True)
                        break
                    a += 1
                    if encertades_seguides == 10:
                        pantalla_victoria()
                        executant = False
                        break
                    if a < 10:
                        portes()
                        respostaCorrecte = False
                        # Ara només envia si han passat 10 segons
                        envia_estat_joc(game_id, a, encertades_seguides, score)
    if cop == 0:
        portes()
        cop = 1

    # També envia l'estat cada 10 segons encara que no hi hagi resposta nova
    envia_estat_joc(game_id, a, encertades_seguides, score)

    pygame.display.flip()

# Tanquem Pygame
pygame.quit()