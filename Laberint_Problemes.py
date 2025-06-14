import pygame
import random
import requests
import time
from preguntes.preguntes_prog import PreResProg, ResCorProg
from preguntes.preguntes_mat import PreResMat, ResCorMat
from preguntes.preguntes_gen import PreResGen, ResCorGen
from preguntes.preguntes_hist import PreResHist, ResCorHist
from preguntes.preguntes_geo import PreResGeo, ResCorGeo
from preguntes.preguntes_tec import PreResTec, ResCorTec
from preguntes.preguntes_cie import PreResCie, ResCorCie
from preguntes.preguntes_esport import PreResEsport, ResCorEsport
from preguntes.preguntes_arts import PreResArts, ResCorArts

import sys

def log(msg, **vars):
    """Mostra missatges de log amb format i valors de variables."""
    prefix = "[LOG]"
    if vars:
        var_str = " | " + " | ".join(f"{k}={v!r}" for k, v in vars.items())
    else:
        var_str = ""
    print(f"{prefix} {msg}{var_str}")

def log_state():
    """Mostra l'estat de les variables importants."""
    important_vars = {
        "a": a,
        "encertades_seguides": encertades_seguides,
        "encerts_totals": encerts_totals,
        "score": score,
        "num_errors": num_errors,
        "executant": executant,
        "pregunta_actual": preguntesJoc[a][0] if a < len(preguntesJoc) else "N/A"
    }
    print("\n[STATE] " + " | ".join(f"{k}={v!r}" for k, v in important_vars.items()) + "\n")

# Inicialitzem Pygame
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("assets/musicafons.mp3")  # Posa aquí el teu fitxer de música
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)
volum = 0.5

# Constants de la finestra
AMPLADA = 800
ALCADA = 600
finestra = pygame.display.set_mode((AMPLADA, ALCADA))
pygame.display.set_caption("Laberint de problemes")

# Carrega fons i portes (després de set_mode!)
fons = pygame.image.load("assets/fons/fons_retro.png").convert()
porta_imgs = [
    pygame.image.load("assets/portes/porta1.png").convert_alpha(),
    pygame.image.load("assets/portes/porta2.png").convert_alpha(),
    pygame.image.load("assets/portes/porta3.png").convert_alpha(),
    pygame.image.load("assets/portes/porta4.png").convert_alpha(),
]

# Conexió amb servidor
log("Connectant amb el servidor per obtenir seed i game_id...")
resposta = requests.get("https://fun.codelearn.cat/hackathon/game/new")
dades = resposta.json()

seed = dades["seed"]
game_id = dades["game_id"]
log("Seed i game_id rebuts", seed=seed, game_id=game_id)

random.seed(seed)

# Colors (R, G, B)
VERMELL = (255, 0, 0)
VERD = (0, 255, 0)
BLAU = (0, 0, 255)
GROC = (255, 255, 0)
NEGRE = (0, 0, 0)

preguntesJoc = []
respostesJoc = []
preguntes_seleccionades = []
respostes_seleccionades = []

tipus_preguntes = [
    ("Programació", PreResProg, ResCorProg),
    ("Matemàtiques", PreResMat, ResCorMat),
    ("Cultura General", PreResGen, ResCorGen),
    ("Història", PreResHist, ResCorHist),
    ("Geografia", PreResGeo, ResCorGeo),
    ("Tecnologia", PreResTec, ResCorTec),
    ("Ciències", PreResCie, ResCorCie),
    ("Esport", PreResEsport, ResCorEsport),
    ("Arts", PreResArts, ResCorArts),
]
tipus_idx = 0  # Per defecte, programació

def prepara_preguntes(ultima_pregunta=None):
    global preguntesJoc, respostesJoc, preguntes_seleccionades, respostes_seleccionades, PreRes, ResCor
    log("Preparant preguntes...", ultima_pregunta=ultima_pregunta)
    if not preguntes_seleccionades:
        indexos = random.sample(range(len(PreRes)), 10)
        preguntes_seleccionades = [PreRes[idx] for idx in indexos]
        respostes_seleccionades = [ResCor[idx] for idx in indexos]
        log("Preguntes seleccionades", preguntes_seleccionades=preguntes_seleccionades)
    while True:
        indices_aleatoris = list(range(10))
        random.shuffle(indices_aleatoris)
        if ultima_pregunta is None or preguntes_seleccionades[indices_aleatoris[0]][0] != ultima_pregunta:
            break
    preguntesJoc = [preguntes_seleccionades[i] for i in indices_aleatoris]
    respostesJoc = [respostes_seleccionades[i] for i in indices_aleatoris]
    log("Preguntes barrejades", preguntesJoc=preguntesJoc)

p1 = p2 = p3 = p4 = p5 = p6 = p7 = p8 = p9 = p10 = False

num_errors = 0
# Variables globals per a la pregunta actual i la resposta correcta

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
font = pygame.font.Font("assets/retro_font.ttf", 16)  # Abans 36

default_font_name = "assets/retro_font.ttf"
default_font_size = 22
min_font_size = 10
max_font_size = 22

def get_max_font_size_fit(words, max_width, max_font_size, min_font_size):
    """Troba la mida màxima de font amb què totes les paraules capin en amplada."""
    for font_size in range(max_font_size, min_font_size - 1, -1):
        font = pygame.font.Font(default_font_name, font_size)
        if all(font.render(word, True, NEGRE).get_width() <= max_width for word in words):
            return font
    return pygame.font.Font(default_font_name, min_font_size)

def wrap_text(text, font, max_width):
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + " " + word if current_line else word
        if font.render(test_line, True, NEGRE).get_width() <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines

# Funció colocar portes i pregunta
def render_text_fit(text, font_path, color, max_width, max_height, min_size=10, max_size=22):
    """Renderitza el text ajustant la mida de la font perquè càpiga dins max_width i max_height."""
    size = max_size
    while size >= min_size:
        font = pygame.font.Font(font_path, size)
        text_surface = font.render(text, True, color)
        if text_surface.get_width() <= max_width and text_surface.get_height() <= max_height:
            return text_surface
        size -= 1
    font = pygame.font.Font(font_path, min_size)
    return font.render(text, True, color)

def portes():
    finestra.blit(fons, (0, 0))
    resposta_max_width = ample_porta - 24

    # Títol de la pregunta a dalt
    lines = wrap_text(preguntesJoc[a][0], font, AMPLADA - 40)
    y_preg = 40
    for line in lines:
        text_surface = font.render(line, True, NEGRE)
        text_rect = text_surface.get_rect(center=(AMPLADA // 2, y_preg))
        finestra.blit(text_surface, text_rect)
        y_preg += text_surface.get_height() + 2

    # Portes i respostes
    for i in range(4):
        x = marge_lateral + i * (ample_porta + espai_entre_portes)
        y = (ALCADA - alt_porta) // 2 - 30

        porta_img = pygame.transform.smoothscale(porta_imgs[i], (ample_porta, alt_porta))
        finestra.blit(porta_img, (x, y))

        resposta_text = preguntesJoc[a][i + 1]
        words = resposta_text.split()
        resposta_font = get_max_font_size_fit(words, resposta_max_width, max_font_size, min_font_size)
        resposta_lines = wrap_text(resposta_text, resposta_font, resposta_max_width)
        resposta_y = y + alt_porta // 2 - (len(resposta_lines) * resposta_font.get_height()) // 2
        for line in resposta_lines:
            resposta_surface = resposta_font.render(line, True, (255, 255, 255))
            resposta_rect = resposta_surface.get_rect(center=(x + ample_porta // 2, resposta_y))
            finestra.blit(resposta_surface, resposta_rect)
            resposta_y += resposta_surface.get_height()

def pantalla_inici():
    global tipus_idx, PreRes, ResCor
    boto_rects = []
    boto_font = pygame.font.Font("assets/retro_font.ttf", 32)
    logo = pygame.image.load("assets/logo.png").convert_alpha()
    logo_rect = logo.get_rect(center=(AMPLADA // 2, 220))
    boto_w, boto_h = 550, 70
    boto_margin = 18  # Espai intern pels costats

    inici = True
    while inici:
        boto_texts = [
            "Comença",
            f"Tipus: {tipus_preguntes[tipus_idx][0]}",
            "Crèdits"
        ]
        # Ara amb separació d'alçada entre botons
        boto_rects = [
            pygame.Rect((AMPLADA - boto_w) // 2, 350, boto_w, boto_h),
            pygame.Rect((AMPLADA - boto_w) // 2, 350 + 80, boto_w, boto_h),
            pygame.Rect((AMPLADA - boto_w) // 2, 350 + 160, boto_w, boto_h)
        ]

        finestra.blit(fons, (0, 0))
        finestra.blit(logo, logo_rect)
        mouse = pygame.mouse.get_pos()
        for i, rect in enumerate(boto_rects):
            color = (255, 0, 128) if rect.collidepoint(mouse) else (0, 0, 0)
            pygame.draw.rect(finestra, color, rect, border_radius=12)
            text = boto_font.render(boto_texts[i], True, (255, 255, 255))
            text_rect = text.get_rect()
            text_rect.center = rect.center
            if text_rect.width > rect.width - 2 * boto_margin:
                shrink_font = pygame.font.Font("assets/retro_font.ttf", 24)
                text = shrink_font.render(boto_texts[i], True, (255, 255, 255))
                text_rect = text.get_rect()
                text_rect.center = rect.center
            finestra.blit(text, text_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if boto_rects[0].collidepoint(event.pos):
                    PreRes, ResCor = tipus_preguntes[tipus_idx][1], tipus_preguntes[tipus_idx][2]
                    preguntes_seleccionades.clear()
                    respostes_seleccionades.clear()
                    prepara_preguntes()
                    inici = False
                elif boto_rects[1].collidepoint(event.pos):
                    tipus_idx = (tipus_idx + 1) % len(tipus_preguntes)
                elif boto_rects[2].collidepoint(event.pos):
                    fade_out(finestra, duracio=0.5)
                    pantalla_credits()
        pygame.display.flip()

def pantalla_credits():
    boto_font = pygame.font.Font("assets/retro_font.ttf", 13)  # 40% més petit que 19
    titol_font = pygame.font.Font("assets/retro_font.ttf", 48)
    petit_font = pygame.font.Font("assets/retro_font.ttf", 22)
    github_color = (0, 102, 204)

    # Logos rectangulars i més amples
    logo_deq = pygame.image.load("assets/deq4future.png").convert_alpha()
    logo_codelearn = pygame.image.load("assets/codelearn.png").convert_alpha()
    logo_deq = pygame.transform.smoothscale(logo_deq, (240, 90))
    logo_codelearn = pygame.transform.smoothscale(logo_codelearn, (240, 90))

    boto_rect = pygame.Rect((AMPLADA - 260) // 2, ALCADA - 90, 260, 40)

    # Zones clicables pels links
    arnau_link_rect = None
    raul_link_rect = None

    credits = True
    while credits:
        finestra.blit(fons, (0, 0))
        # Títol
        titol = titol_font.render("CRÈDITS", True, (0, 0, 0))
        finestra.blit(titol, titol.get_rect(center=(AMPLADA // 2, 70)))

        # Noms i links
        y = 140
        text1 = petit_font.render("Joc fet per:", True, (0, 0, 0))
        finestra.blit(text1, text1.get_rect(center=(AMPLADA // 2, y)))
        y += 36

        # Arnau
        arnau = petit_font.render("Arnau Pons (@arpons)", True, github_color)
        arnau_rect = arnau.get_rect(center=(AMPLADA // 2, y))
        finestra.blit(arnau, arnau_rect)
        arnau_link = petit_font.render("github.com/arpons", True, github_color)
        arnau_link_rect = arnau_link.get_rect(center=(AMPLADA // 2, y + 22))
        finestra.blit(arnau_link, arnau_link_rect)
        y += 50

        # Raül
        raul = petit_font.render("Raül Benito (@rauuul-dev)", True, github_color)
        raul_rect = raul.get_rect(center=(AMPLADA // 2, y))
        finestra.blit(raul, raul_rect)
        raul_link = petit_font.render("github.com/rauuul-dev", True, github_color)
        raul_link_rect = raul_link.get_rect(center=(AMPLADA // 2, y + 22))
        finestra.blit(raul_link, raul_link_rect)
        y += 50

        # Hackathon
        hack = petit_font.render('Per la Hackathon "Hack the Future"', True, (0, 0, 0))
        finestra.blit(hack, hack.get_rect(center=(AMPLADA // 2, y)))
        y += 36

        # Logos més amunt i rectangulars i més amples
        logos_y = y + 40
        finestra.blit(logo_deq, logo_deq.get_rect(center=(AMPLADA // 2 - 140, logos_y)))
        finestra.blit(logo_codelearn, logo_codelearn.get_rect(center=(AMPLADA // 2 + 140, logos_y)))

        # Botó enrere més ample i text més petit
        mouse = pygame.mouse.get_pos()
        color = (255, 0, 128) if boto_rect.collidepoint(mouse) else (0, 0, 0)
        pygame.draw.rect(finestra, color, boto_rect, border_radius=12)
        text = boto_font.render("Torna enrere", True, (255, 255, 255))
        text_rect = text.get_rect(center=boto_rect.center)
        finestra.blit(text, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if boto_rect.collidepoint(event.pos):
                    fade_out(finestra, duracio=0.5)
                    credits = False
                elif arnau_link_rect and arnau_link_rect.collidepoint(event.pos):
                    import webbrowser
                    webbrowser.open("https://github.com/arpons")
                elif raul_link_rect and raul_link_rect.collidepoint(event.pos):
                    import webbrowser
                    webbrowser.open("https://github.com/rauuul-dev")
        pygame.display.flip()

def reset_joc():
    global a, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, cop, respostaCorrecte
    a = 0
    p1 = p2 = p3 = p4 = p5 = p6 = p7 = p8 = p9 = p10 = False
    cop = 0
    respostaCorrecte = False
    log("Joc reiniciat")
    log_state()

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
            "score": score,
            "errors": num_errors,
            "a": a,
            "encertades_seguides": encertades_seguides,
            "encerts_totals": encerts_totals,
            "executant": executant,
            "pregunta_text": preguntesJoc[a][0] if a < len(preguntesJoc) else "N/A"
        }
    }
    log("Enviant estat al servidor", **dades["data"])
    try:
        resposta = requests.post(url, json=dades)
        if resposta.headers.get("Content-Type", "").startswith("application/json"):
            resposta_json = resposta.json()
            log("Resposta del servidor", resposta=resposta_json)
        else:
            log("Resposta no JSON", resposta=resposta.text)
    except Exception as e:
        log("Error enviant estat", error=str(e))
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
    log("Enviant finalització al servidor", encerts=encerts, score=score)
    try:
        resposta = requests.post(url, json=dades)
        if resposta.headers.get("Content-Type", "").startswith("application/json"):
            resposta_json = resposta.json()
            log("Resposta final del servidor", resposta=resposta_json)
        else:
            log("Resposta no JSON", resposta=resposta.text)
    except Exception as e:
        log("Error finalitzant joc", error=str(e))

def pantalla_victoria():
    font_gran = pygame.font.Font("assets/retro_font.ttf", 72)
    text = font_gran.render("🏆 VICTÒRIA! 🏆", True, NEGRE)
    text_rect = text.get_rect(center=(AMPLADA // 2, ALCADA // 2))
    finestra.blit(fons, (0, 0))
    finestra.blit(text, text_rect)
    pygame.display.flip()
    log("PARTIDA GUANYADA! 🏆")
    log_state()
    pygame.time.wait(3000)

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
    global a, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, respostaCorrecte
    a = 0
    p1 = p2 = p3 = p4 = p5 = p6 = p7 = p8 = p9 = p10 = False
    respostaCorrecte = False
    log("Reiniciant partida", ultima_pregunta=ultima_pregunta)
    prepara_preguntes(ultima_pregunta)
    log_state()

def fade_out(finestra, duracio=0.8):
    """Transició de fade a negre sobre la finestra."""
    clock = pygame.time.Clock()
    fade_surface = pygame.Surface((AMPLADA, ALCADA))
    fade_surface.fill((0, 0, 0))
    passos = int(duracio * 60)  # 60 FPS
    for alpha in range(0, 256, max(1, 255 // passos)):
        fade_surface.set_alpha(alpha)
        finestra.blit(fade_surface, (0, 0))
        pygame.display.flip()
        clock.tick(60)

def dibuixa_slider_volum(volum):
    slider_w, slider_h = 120, 16
    slider_x = AMPLADA - slider_w - 30
    slider_y = ALCADA - slider_h - 30
    pygame.draw.rect(finestra, (80, 80, 80), (slider_x, slider_y, slider_w, slider_h), border_radius=8)
    pygame.draw.rect(finestra, (255, 0, 128), (slider_x, slider_y, int(slider_w * volum), slider_h), border_radius=8)
    font_slider = pygame.font.Font(default_font_name, 16)
    # Més cap a l'esquerra (abans era slider_x - 60)
    txt = font_slider.render("Volum", True, (0, 0, 0))
    finestra.blit(txt, (slider_x - 90, slider_y - 2))
    return pygame.Rect(slider_x, slider_y, slider_w, slider_h)

# Pantalla d'inici abans del bucle principal
pantalla_inici()
fade_out(finestra, duracio=0.8)  # <--- Afegit aquí
log("Pantalla d'inici mostrada")

# Prepara preguntes abans de començar el joc!
prepara_preguntes()
log("Preguntes preparades")

# Bucle principal

cop = 0
a = 0
respostaCorrecte = False

encertades_seguides = 0
encerts_totals = 0

executant = True
log("Iniciant bucle principal del joc")
log_state()
while executant:
    slider_rect = dibuixa_slider_volum(volum)
    for esdeveniment in pygame.event.get():
        if esdeveniment.type == pygame.QUIT:
            log("Sortint del joc per esdeveniment QUIT")
            executant = False
        elif esdeveniment.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = esdeveniment.pos
            if slider_rect.collidepoint(mouse_x, mouse_y):
                rel_x = mouse_x - slider_rect.x
                volum = max(0, min(1, rel_x / slider_rect.width))
                pygame.mixer.music.set_volume(volum)
            mouse_x, mouse_y = esdeveniment.pos
            log("Click detectat", mouse_x=mouse_x, mouse_y=mouse_y)
            for i in range(4):
                x = marge_lateral + i * (ample_porta + espai_entre_portes)
                y = (ALCADA - alt_porta) // 2 - 30
                porta_rect = pygame.Rect(x, y, ample_porta, alt_porta)
                if porta_rect.collidepoint(mouse_x, mouse_y):
                    resposta_escollida = preguntesJoc[a][i + 1]
                    resposta_correcta = respostesJoc[a]
                    log("Porta clicada", porta=i+1, resposta_escollida=resposta_escollida, resposta_correcta=resposta_correcta)
                    if resposta_escollida == resposta_correcta:
                        respostaCorrecte = True
                        encertades_seguides += 1
                        encerts_totals += 1
                        log("Resposta correcta!", encertades_seguides=encertades_seguides, encerts_totals=encerts_totals)
                    else:
                        if score > 30:
                            score = max(30, score - 5)
                        log("Resposta incorrecta! Torna a començar.", score=score)
                        reinicia_partida(preguntesJoc[a][0])
                        encertades_seguides = 0
                        num_errors += 1
                        portes()
                        envia_estat_joc(game_id, encertades_seguides, encerts_totals, score, forcat=True)
                        log_state()
                        break
                    a += 1
                    if encertades_seguides == 10:
                        pantalla_victoria()
                        executant = False
                        break
                    if a < 10:
                        portes()
                        respostaCorrecte = False
                        envia_estat_joc(game_id, a, encerts_totals, score)
                        log_state()
    if cop == 0:
        log("Dibuixant portes per primer cop")
        portes()
        cop = 1

    envia_estat_joc(game_id, a, encerts_totals, score)

    pygame.display.flip()

# Tanquem Pygame
log("Tancant Pygame. Joc finalitzat.")
pygame.quit()