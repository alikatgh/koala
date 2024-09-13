import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Squirrel Finder")

# Define colors
BACKGROUND = (20, 20, 40)
TEXT_COLOR = (255, 200, 100)

# Load images
koala = pygame.transform.scale(pygame.image.load("koala.png"), (40, 40))
strawberry = pygame.transform.scale(
    pygame.image.load("strawberry.png"), (40, 40))
squirrel = pygame.transform.scale(pygame.image.load("squirrel.png"), (40, 40))

# Set up the player
player_pos = [WIDTH // 2, HEIGHT // 2]
player_speed = 5

# Set up the strawberry
strawberry_pos = [random.randint(
    0, WIDTH - 40), random.randint(0, HEIGHT - 40)]
strawberry_speed = [random.choice([-3, 3]), random.choice([-3, 3])]

# Set up the squirrel
squirrel_pos = [random.randint(0, WIDTH - 40), random.randint(0, HEIGHT - 40)]
squirrel_speed = [random.choice([-2, 2]), random.choice([-2, 2])]

# Set up the font
font = pygame.font.Font(None, 36)

# Set up the timer
start_time = pygame.time.get_ticks()
game_duration = 0

# Game states
INSTRUCTIONS = 0
PLAYING = 1
WIN = 2
LOSE = 3
game_state = INSTRUCTIONS


def show_instructions():
    screen.fill(BACKGROUND)
    lines = [
        "Squirrel Finder",
        "Use arrow keys to move the koala",
        "Avoid strawberries",
        "Find the squirrel to win",
        "Press any key to start"
    ]
    for i, line in enumerate(lines):
        text = font.render(line, True, TEXT_COLOR)
        screen.blit(text, (WIDTH // 2 - text.get_width() //
                    2, HEIGHT // 2 - 100 + i * 40))
    pygame.display.flip()


def reset_game():
    global player_pos, strawberry_pos, squirrel_pos, start_time
    player_pos = [WIDTH // 2, HEIGHT // 2]
    strawberry_pos = [random.randint(
        0, WIDTH - 40), random.randint(0, HEIGHT - 40)]
    squirrel_pos = [random.randint(
        0, WIDTH - 40), random.randint(0, HEIGHT - 40)]
    start_time = pygame.time.get_ticks()


# Game loop
clock = pygame.time.Clock()
strawberry_timer = 0
squirrel_timer = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and game_state == INSTRUCTIONS:
            game_state = PLAYING
            reset_game()

    if game_state == INSTRUCTIONS:
        show_instructions()
        continue

    if game_state == PLAYING:
        # Move the player
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_pos[0] -= player_speed
        if keys[pygame.K_RIGHT]:
            player_pos[0] += player_speed
        if keys[pygame.K_UP]:
            player_pos[1] -= player_speed
        if keys[pygame.K_DOWN]:
            player_pos[1] += player_speed

        # Keep player on screen
        player_pos[0] = max(0, min(player_pos[0], WIDTH - 40))
        player_pos[1] = max(0, min(player_pos[1], HEIGHT - 40))

        # Move the strawberry
        strawberry_pos[0] += strawberry_speed[0]
        strawberry_pos[1] += strawberry_speed[1]

        # Bounce strawberry off walls
        if strawberry_pos[0] <= 0 or strawberry_pos[0] >= WIDTH - 40:
            strawberry_speed[0] *= -1
        if strawberry_pos[1] <= 0 or strawberry_pos[1] >= HEIGHT - 40:
            strawberry_speed[1] *= -1

        # Move the squirrel (after 3 seconds)
        current_time = pygame.time.get_ticks()
        if current_time - start_time >= 3000:
            squirrel_pos[0] += squirrel_speed[0]
            squirrel_pos[1] += squirrel_speed[1]

            # Bounce squirrel off walls
            if squirrel_pos[0] <= 0 or squirrel_pos[0] >= WIDTH - 40:
                squirrel_speed[0] *= -1
            if squirrel_pos[1] <= 0 or squirrel_pos[1] >= HEIGHT - 40:
                squirrel_speed[1] *= -1

        # Check for collisions
        player_rect = pygame.Rect(player_pos[0], player_pos[1], 40, 40)
        strawberry_rect = pygame.Rect(
            strawberry_pos[0], strawberry_pos[1], 40, 40)
        squirrel_rect = pygame.Rect(squirrel_pos[0], squirrel_pos[1], 40, 40)

        if player_rect.colliderect(strawberry_rect):
            game_state = LOSE

        if player_rect.colliderect(squirrel_rect):
            game_state = WIN

        # Draw everything
        screen.fill(BACKGROUND)
        screen.blit(koala, player_pos)
        screen.blit(strawberry, strawberry_pos)
        if current_time - start_time >= 3000:
            screen.blit(squirrel, squirrel_pos)

        # Draw timer
        game_duration = (current_time - start_time) // 1000
        timer_text = font.render(f"Time: {game_duration}s", True, TEXT_COLOR)
        screen.blit(timer_text, (10, 10))

        # Draw "openai" text
        openai_text = font.render("openai", True, TEXT_COLOR)
        screen.blit(openai_text, (WIDTH // 2 -
                    openai_text.get_width() // 2, HEIGHT - 40))

    elif game_state == WIN:
        screen.fill(BACKGROUND)
        win_text = font.render(
            f"You Win! Time: {game_duration}s", True, TEXT_COLOR)
        screen.blit(
            win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2))
        restart_text = font.render(
            "Press any key to restart", True, TEXT_COLOR)
        screen.blit(restart_text, (WIDTH // 2 -
                    restart_text.get_width() // 2, HEIGHT // 2 + 50))
        if pygame.key.get_pressed():
            game_state = PLAYING
            reset_game()

    elif game_state == LOSE:
        screen.fill(BACKGROUND)
        lose_text = font.render("Game Over!", True, TEXT_COLOR)
        screen.blit(lose_text, (WIDTH // 2 -
                    lose_text.get_width() // 2, HEIGHT // 2))
        restart_text = font.render(
            "Press any key to restart", True, TEXT_COLOR)
        screen.blit(restart_text, (WIDTH // 2 -
                    restart_text.get_width() // 2, HEIGHT // 2 + 50))
        if pygame.key.get_pressed():
            game_state = PLAYING
            reset_game()

    pygame.display.flip()
    clock.tick(60)
