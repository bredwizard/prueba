import pygame

#optimizar crear texto (texto, posicion en y, posicion en x)
def drawText(t, x, y):
    text = font.render(t, True, AMARILLO, NEGRO)
    # generar rectangulo de texto
    text_rectangle = text.get_rect()
    # posicion en X y Y del texto
    text_rectangle.topleft = (x, y)
    # poner en pantalla el texto
    screen.blit(text, text_rectangle)

# VARIABLES
# tamaño de pantalla
SCREEN_SIZE = (1000, 560)
# color del fondo de la pantalla
NEGRO = (50, 50, 50)
# colores(red,green,blue)
AMARILLO = (255, 255, 0)

# altura jugador
player_height = 104
# ancho jugador
player_width = 59

#direccion del sprite del jugador
player_direction = "right"

# INICIAR
pygame.init()
# definir pantalla y tamañp
screen = pygame.display.set_mode(SCREEN_SIZE)
# nombre del juego en la ventana de windows
pygame.display.set_caption("Project Team")
# define la tasa de fotogramas por segundo en el juego
clock = pygame.time.Clock()
# variable fuente de escritura por default
font = pygame.font.Font(pygame.font.get_default_font(), 24)

#estado de juego para ganar-perder
game_state = "playing"

# JUGADOR
# invocar el avatar del jugador
player_image = pygame.image.load("assets/personajes/alejo_1.png","assets/personajes/alejo_2.png")

# posicion inicial en x
player_x = 300
print(player_x)

# posicion inicial en y
player_y = 190
# velocidad inicial del jugador
player_speed = 0
# aceleracion del jugador
player_aceleracion = 0.2

# PLATAFORMAS --> hitbox plataforma(posicion x, posicion y, longitud x, longitud y)
plataforma = pygame.image.load("assets/plataforma.png")
plataformas = [
    # plataforma media(izquierda a derecha)
    pygame.Rect(100, 300, 64, 64),
    pygame.Rect(164, 300, 64, 64),
    pygame.Rect(228, 300, 64, 64),
    pygame.Rect(292, 300, 64, 64),
    pygame.Rect(356, 300, 64, 64),
    pygame.Rect(420, 300, 64, 64),
    # plataforma de la izquierda
    pygame.Rect(100, 236, 64, 64),
    # plataforma de la derecha
    pygame.Rect(420, 236, 64, 64),

]

# IMAGEN DE MONEDA COLECCIONABLE
coin = pygame.image.load("assets/objetos/moneda_0.png")
# MONEDAS COLECCIONABLES ---> hitbox moneda(posicion x, posicion y, longitud x, longitud y)
coins = [
    pygame.Rect(110, 185, 46, 46),
    pygame.Rect(430, 185, 46, 46)
]

# puntuacion
score = 0

# IMAGEN ENEMIGOS
enemy = pygame.image.load("assets/personajes/esbirros_1.png")
# lista de enemigos ---> hitbox enemigo(posicion x, posicion y, longitud x, longitud y)
enemies = [
    pygame.Rect(170, 240, 64, 61),
]
# numero inicial de vida
vidas = 3
# imagen vidas
vida_image = pygame.image.load("assets/vida.png")

# LOOP
running = True
while running:

    # ------
    # INPUTS
    # ------

    # ver. salir (si le damos a la x de windows salimos del juego)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if game_state  == "playing":

        # nuevas posiciones de personaje en X y Y (movimiento)
        new_player_x = player_x
        new_player_y = player_y

        # movimiento del jugador
        # variable para "tecla presionada"
        teclas = pygame.key.get_pressed()
        # ir a la izquierda = tecla A
        if teclas[pygame.K_a]:
            # velocidad traslacion izquierda
            new_player_x -= 2
            #direccion del sprite izquierda
            player_direction = "left"
        # ir a la derecha = tecla D
        if teclas[pygame.K_d]:
            # velocidad traslacion derecha
            new_player_x += 2
            #direccion del sprite derecha
            player_direction = "right"
        # salto  = W (si esta en el suelo)
        if teclas[pygame.K_w] and player_on_ground:
            # velocidad salto
            player_speed = -7

    # ------
    # UPDATE
    # ------

    # si estamos jugando...
    if game_state == "playing":

        # movimiento horizontal y colision (pocicion en x, posicion en y, longitud colision en x, longitud colision en y)
        new_player_rect = pygame.Rect(new_player_x, player_y, player_width, player_height)
        # variable colisiones en x
        x_colision = False

        # verificar colision horizontal en la lista de plataformas
        for p in plataformas:
            # "si colisiona con la hitbox del jugador en x..."
            if p.colliderect(new_player_rect):
                x_colision = True
                break

        # fin de la colision o no colision en x
        if x_colision == False:
            player_x = new_player_x

        # movimiento vertical
        # "la velocidad aumenta a la tasa de la aceleracion en y"
        player_speed += player_aceleracion
        # la posicion aumenta a la tasa de la velocidad en y"
        new_player_y += player_speed

        # movimiento vertical y colision (pocicion en x, posicion en y, longitud colision en x, longitud colision en y)
        new_player_rect = pygame.Rect(player_x, new_player_y, player_width, player_height)
        # variable colision en y
        y_colision = False
        player_on_ground = False

        # verificar colision vertical en la lista de plataformas
        for p in plataformas:
            # "si colisiona con la hitbox del jugador en x..."
            if p.colliderect(new_player_rect):
                y_colision = True
                player_speed = 0
                # "si la plataforma esta debajo del jugador"
                if p[1] > new_player_y:
                    # mantener el jugador en la plataforma
                    player_y = p[1] - player_height
                    player_on_ground = True
                break

        # fin de la colision o no colision en y
        if y_colision == False:
            player_y = new_player_y

        # verificar si una moneda fue recolectada en las posiciones (posicion en x del jugador, posicion en y del jugador, ancho del jugador, altura del jugador)
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        # "algo en la lista de monedas colisiona con el jugador..."
        for c in coins:
            if c.colliderect(player_rect):
                # "...entonces quitar la moneda..."
                coins.remove(c)
                # "...y sumar 1 al marcador"
                score += 1
                # ganar si la puntuacion es 2
                if score >= 2:
                    game_state = "win"

        # verificar si el jugador choco con el enemigo (posicion en x del jugador, posicion en y del jugador, ancho del jugador, altura del jugador)
        # "si el jugador choca con el enemigo..."
        for e in enemies:
            if e.colliderect(player_rect):
                # "restablecer posicion"
                player_x = 300
                player_y = 190
                player_speed = 0
                # "...restar una vida"
                vidas -= 1
                # cambiar el estado del juego si no quedan vidas
                if vidas <= 0:
                    #si nos quedamos sin vidas el estado del juego es "perder"
                    game_state = "lose"


    # ----
    # DRAW
    # ----

    # background y color
    screen.fill(NEGRO)

    # dibujar plataforma (pantalla, variable color, lista de plataformas)
    for p in plataformas:
        screen.blit(plataforma, (p.x, p.y))

    # COINS
    for c in coins:
        screen.blit(coin, (c.x, c.y))

    # ENEMIGOS
    for e in enemies:
        screen.blit(enemy, (e.x, e.y))

    # JUGADOR
    #direccion sprite
    #si miramos a la izquierda...
    if player_direction == "left":
        #...dibujar normal
        screen.blit(player_image, (player_x, player_y))
    #si miramos a la derecha...
    elif player_direction == "right":
        #dibujar reflejado en el eje x -> true, pero no en el eje y -> false
        screen.blit(pygame.transform.flip(player_image, True, False), (player_x, player_y))

    # informacion del jugador en pantalla
    # puntaje
    # imagen de score "misma de coin"
    screen.blit(coin, (10, 10))
    drawText(str(score), 65, 35)

    # vidas
    for l in range(vidas):
        # poner vidas en pantalla en X + repeticion cuantas vidas hayan, y
        screen.blit(vida_image, (10 + (l * 20), 65))

    # si ganamos o perdemos mostrar en pantalla:
    # si ganamos
    if game_state == "win":
        # texto de victoria
        drawText("¡YOU WIN, CONGRATULATIONS!", 400, 50)
    # si perdemos
    if game_state == "lose":
        # texto de derrota
        drawText("GAME OVER", 400, 50)


    # pantalla actual
    pygame.display.flip()

    # limitadortasa de fotogramas por segundos (60 fps)
    clock.tick(60)

# salir del programa
pygame.quit()

# coin sprite por DasBilligeAlien
# https://opengameart.org/content/rotating-coin-0

# sprite corazon por BenBushnell
# https://pixabay.com/es/illustrations/pixel-corazón-corazón-píxeles-2779422/