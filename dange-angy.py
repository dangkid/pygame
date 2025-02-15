import pygame
import sys
import random

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
width, height = 700, 775
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("si pierdo te teletransportas a mi costado, miss u 😞")

# Cargar imágenes y escalarlas
player_image = pygame.image.load("imgs/dange.png")
player_image = pygame.transform.scale(player_image, (80, 80))

bullet_image = pygame.image.load("imgs/corazón.png")
bullet_image = pygame.transform.scale(bullet_image, (50, 50))

enemy_image = pygame.image.load("imgs/angy.png")
enemy_image = pygame.transform.scale(enemy_image, (60, 60))

background_image = pygame.image.load("imgs/fondo-amor.jpeg")
background_image = pygame.transform.scale(background_image, (width, height))

# Jugador
player_rect = player_image.get_rect()
player_rect.topleft = (width // 2 - player_rect.width // 2, height - player_rect.height - 10)
player_speed = 15

# Bala
bullet_speed = 10
bullets = []

# Enemigo
enemy_speed = 5
enemies = []

# Reloj
clock = pygame.time.Clock()

# Mantener registro de teclas presionadas
touch_start = None  # Para almacenar la posición del toque
is_touching = False  # Para saber si se está tocando la pantalla

# Bucle principal del juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Detectar toque en la pantalla
        if event.type == pygame.FINGERDOWN:
            touch_start = (event.x * width, event.y * height)  # Almacenar la posición inicial del toque
            is_touching = True
        elif event.type == pygame.FINGERUP:
            touch_start = None
            is_touching = False
        elif event.type == pygame.FINGERMOTION and is_touching:
            touch_x, touch_y = event.x * width, event.y * height
            player_rect.centerx = touch_x  # Mover al jugador a la posición táctil

            # Crear nuevas balas mientras se mantiene el toque
            if random.randint(0, 100) < 20:  # Disparar balas aleatoriamente mientras el toque se mantenga
                bullet_rect = bullet_image.get_rect()
                bullet = {
                    'rect': pygame.Rect(
                        player_rect.x + player_rect.width // 2 - bullet_rect.width // 2,
                        player_rect.y,
                        bullet_rect.width,
                        bullet_rect.height
                    ),
                    'image': bullet_image
                }
                bullets.append(bullet)

    # Actualizar posición de las balas
    for bullet in bullets[:]:
        bullet['rect'].y -= bullet_speed
        if bullet['rect'].bottom < 0:
            bullets.remove(bullet)  # Eliminar la bala si sale de la pantalla

    # Generar enemigos aleatorios
    if random.randint(0, 100) < 5:
        enemy_rect = enemy_image.get_rect()
        enemy_rect.x = random.randint(0, width - enemy_rect.width)
        enemies.append(enemy_rect.copy())

    # Actualizar posición de los enemigos
    for enemy in enemies:
        enemy.y += enemy_speed

    # Colisiones entre balas y enemigos
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if enemy.colliderect(bullet['rect']):
                bullets.remove(bullet)
                enemies.remove(enemy)

    # Colisiones entre jugador y enemigos
    for enemy in enemies:
        if player_rect.colliderect(enemy):
            pygame.quit()
            sys.exit()

    # Limpiar la pantalla con el fondo
    screen.blit(background_image, (0, 0))

    # Dibujar al jugador
    screen.blit(player_image, player_rect)

    # Dibujar las balas
    for bullet in bullets:
        screen.blit(bullet['image'], bullet['rect'].topleft)

    # Dibujar los enemigos
    for enemy in enemies:
        screen.blit(enemy_image, enemy)

    # Actualizar la pantalla
    pygame.display.flip()

    # Establecer límite de FPS
    clock.tick(30)
