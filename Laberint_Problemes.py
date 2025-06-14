import pygame
import random

# Inicialitzem Pygame
pygame.init()

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

# Taula pregunta respostes
PreRes = [
    ["Una entrada general per un concert costa 15 €, i una entrada VIP costa 25 €. Si s’han venut 4 entrades generals i 2 VIP, quin ha estat l’import total recaptat?", "110 €", "100 €", "120 €", "90 €"],
    ["En Joan té 12 anys més que en Pere. Si la suma de les seves edats és 40, quants anys tenen en Joan i en Pere?", "Joan: 20, Pere: 20", "Joan: 26, Pere: 14", "Joan: 24, Pere: 16", "Joan: 28, Pere: 12"],
    ["La Maria compra pomes a 2 € cadascuna. Si es gasta 18 €, quantes pomes ha comprat?", "8 pomes", "10 pomes", "6 pomes", "9 pomes"],
    ["Un nombre sumat amb 7 dóna 21. Quin és aquest nombre?", "a", "b", "14", "d"],
    ["Una entrada de cinema costa 8 €, i unes crispetes costen 5 €. Si en total s'han gastat 45 € en entrades i crispetes, i s'han comprat 3 entrades, quantes bossetes de crispetes s'han comprat?", "a", "3 bossetes", "c", "d"],
    ["La Carla té el doble de diners que en Marc. Si entre tots dos tenen 72 €, quant té cadascú?", "a", "b", "Carla: 48, Marc: 24", "d"],
    ["Si a un nombre li multipliquem per 4 i li restem 6, obtenim 18. Quin és aquest nombre?", "a", "b", "c", "6"],
    ["Si la meitat d’un nombre menys 3 és igual a 7, quin és el nombre?", "a", "20", "c", "d"],
    ["Una botiga ven llapis a 1 € i bolígrafs a 2 €. Si una persona compra 10 objectes per un total de 15 €, quants llapis i bolígrafs ha comprat?", "5 llapis i 5 bolígrafs", "b", "c", "d"],
    ["En un examen, la puntuació s’obté segons la fórmula 2(x+3)=182(x+3)=18, on x és el nombre de respostes correctes. Quantes respostes correctes ha tingut?", "a", "b", "6", "d"],
]

# Taula de respostes correctes
ResCor = [
    "110 €",
    "Joan: 26, Pere: 14",
    "9 pomes",
    "14",
    "3 bossetes",
    "Carla: 48, Marc: 24",
    "6",
    "20",
    "5 llapis i 5 bolígrafs",
    "6",
]

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

    # Dibuixem les quatre portes centrades amb text
    for i in range(4):
        x = marge_lateral + i * (ample_porta + espai_entre_portes)
        y = (ALCADA - alt_porta) // 2 - 30
        pygame.draw.rect(finestra, colors_portes[i], (x, y, ample_porta, alt_porta))
        
        lines = wrap_text(PreRes[a][i + 1], font, ample_porta - 2)

        # Dibuixar línia per línia
        for line in lines:
            text_surface = font.render(line, True, NEGRE)
            text_rect = text_surface.get_rect(center=(x + ample_porta // 2, y + alt_porta // 2))
            finestra.blit(text_surface, text_rect)
            y += text_surface.get_height() + 5  # Espai entre línies

    y = (ALCADA - alt_porta) // 2 - 30
    lines = wrap_text(PreRes[a][0], font, AMPLADA - 20)

    # Dibuixar línia per línia
    for line in lines:
        text_surface = font.render(line, True, NEGRE)
        text_rect = text_surface.get_rect(center=(AMPLADA // 2, y + alt_porta + 40))
        finestra.blit(text_surface, text_rect)
        y += text_surface.get_height() + 5  # Espai entre línies



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



# Bucle principal
cop = 0
#a = random.randint(0, 9)
a = 0
respostaCorrecte = False

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
                    print(PreRes[a][i + 1])
                    print(ResCor[a])
                    if PreRes[a][i + 1] == ResCor[a]:
                        respostaCorrecte = True 
                    if a == 0 and respostaCorrecte:
                        p1 = True
                        a = 1
                    elif a == 0 and not(respostaCorrecte):
                        list = [a + 2, a + 3, a + 4]
                        for j in range(4):
                            if PreRes[a][j + 1] != ResCor[a]:
                                if PreRes[a][j + 1] == PreRes[a][i + 1]:
                                    a = list[0]
                                else:
                                    del list[0]          
                    elif a == 1 and respostaCorrecte:
                        p2 = True
                        a = 2
                    elif a == 1 and not(respostaCorrecte):
                        list = [a + 2, a + 3, a + 4]
                        for j in range(4):
                            if PreRes[a][j + 1] != ResCor[a]:
                                if PreRes[a][j + 1] == PreRes[a][i + 1]:
                                    a = list[0]
                                else:
                                    del list[0]
                    elif a == 2 and respostaCorrecte:
                        p3 = True
                        a = 3
                    elif a == 2 and not(respostaCorrecte):
                        list = [a + 2, a + 3, a + 4]
                        for j in range(4):
                            if PreRes[a][j + 1] != ResCor[a]:
                                if PreRes[a][j + 1] == PreRes[a][i + 1]:
                                    a = list[0]
                                else:
                                    del list[0]
                    elif a == 3 and respostaCorrecte:
                        p4 = True
                        a = 4
                    elif a == 3 and not(respostaCorrecte):
                        list = [a + 2, a + 3, a + 4]
                        for j in range(4):
                            if PreRes[a][j + 1] != ResCor[a]:
                                if PreRes[a][j + 1] == PreRes[a][i + 1]:
                                    a = list[0]
                                else:
                                    del list[0]
                    elif a == 4 and respostaCorrecte:
                        p5 = True
                        a = 5
                    elif a == 4 and not(respostaCorrecte):
                        list = [a + 2, a + 3, a + 4]
                        for j in range(4):
                            if PreRes[a][j + 1] != ResCor[a]:
                                if PreRes[a][j + 1] == PreRes[a][i + 1]:
                                    a = list[0]
                                else:
                                    del list[0]
                    elif a == 5 and respostaCorrecte:
                        p6 = True
                        a = 6
                    elif a == 5 and not(respostaCorrecte):
                        list = [a + 2, a + 3, a + 4]
                        for j in range(4):
                            if PreRes[a][j + 1] != ResCor[a]:
                                if PreRes[a][j + 1] == PreRes[a][i + 1]:
                                    a = list[0]
                                else:
                                    del list[0]
                    elif a == 6 and respostaCorrecte:
                        p7 = True
                        a = 7
                    elif a == 6 and not(respostaCorrecte):
                        list = [a + 2, a + 3, 0]
                        for j in range(4):
                            if PreRes[a][j + 1] != ResCor[a]:
                                if PreRes[a][j + 1] == PreRes[a][i + 1]:
                                    a = list[0]
                                else:
                                    del list[0]
                    elif a == 7 and respostaCorrecte:
                        p8 = True
                        a = 8
                    elif a == 7 and not(respostaCorrecte):
                        list = [a + 2, 0, 1]
                        for j in range(4):
                            if PreRes[a][j + 1] != ResCor[a]:
                                if PreRes[a][j + 1] == PreRes[a][i + 1]:
                                    a = list[0]
                                else:
                                    del list[0]
                    elif a == 8 and respostaCorrecte:
                        p9 = True
                        a = 9
                    elif a == 8 and not(respostaCorrecte):
                        list = [ 0, 1, 2]
                        for j in range(4):
                            if PreRes[a][j + 1] != ResCor[a]:
                                if PreRes[a][j + 1] == PreRes[a][i + 1]:
                                    a = list[0]
                                else:
                                    del list[0]
                    elif a == 9 and respostaCorrecte:
                        p10 = True
                        #Comprovacions de totes correctes i guanyar o no
                    elif a == 9 and not(respostaCorrecte):
                        list = [2, 3, 4]
                        for j in range(4):
                            if PreRes[a][j + 1] != ResCor[a]:
                                if PreRes[a][j + 1] == PreRes[a][i + 1]:
                                    a = list[0]
                                else:
                                    del list[0]
                    portes()
                    respostaCorrecte = False
    
    if cop == 0:
        portes()
        cop = 1

    # Actualitzem la pantalla
    pygame.display.flip()

# Tanquem Pygame
pygame.quit()