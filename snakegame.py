import pygame
import random
import csv
import os
import sys

# Initialize pygame
pygame.init()

# Window dimensions
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800   # Reduced height so it fits on most screens
HEADER_HEIGHT = 60    # Top area for player info

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (50, 150, 255)
GRAY = (50, 50, 50)

# Font setup
font = pygame.font.SysFont('arial', 25, bold=True)
large_font = pygame.font.SysFont('arial', 50, bold=True)

# CSV file setup
csv_file = "snake_scores.csv"
if not os.path.exists(csv_file):
    with open(csv_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Player", "Score"])

# Ask player name before starting
def get_player_name():
    input_box = pygame.Rect(WINDOW_WIDTH//2 - 150, WINDOW_HEIGHT//2 - 25, 300, 50)
    color_inactive = GRAY
    color_active = BLUE
    color = color_inactive
    active = False
    text = ''
    done = False
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Snake Game - Enter Name")

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill(BLACK)
        txt_surface = font.render(text, True, WHITE)
        width = max(300, txt_surface.get_width()+10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x+5, input_box.y+10))
        pygame.draw.rect(screen, color, input_box, 2)
        prompt = large_font.render("Enter Your Name:", True, WHITE)
        screen.blit(prompt, (WINDOW_WIDTH//2 - 200, WINDOW_HEIGHT//2 - 100))
        pygame.display.flip()

    return text if text.strip() else "Player"

# Initialize game function
def start_game(player_name):
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Snake Game")

    clock = pygame.time.Clock()

    # Snake settings
    snake_block = 20
    snake_speed = 15

    # Initial snake position
    snake = [(100, 100)]
    direction = (snake_block, 0)

    # Food position
    food = (random.randrange(0, (WINDOW_WIDTH - snake_block)//snake_block) * snake_block,
            random.randrange(HEADER_HEIGHT//snake_block, (WINDOW_HEIGHT - snake_block)//snake_block) * snake_block)

    score = 0
    game_over = False

    def draw_snake(snake_list):
        for x in snake_list:
            pygame.draw.rect(screen, GREEN, [x[0], x[1], snake_block, snake_block])

    def show_score():
        pygame.draw.rect(screen, GRAY, (0, 0, WINDOW_WIDTH, HEADER_HEIGHT))  # header panel
        player_text = font.render(f"Player: {player_name}", True, WHITE)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(player_text, (20, 15))
        screen.blit(score_text, (WINDOW_WIDTH - 150, 15))

    def save_score():
        with open(csv_file, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([player_name, score])

    def game_over_screen():
        screen.fill(BLACK)
        msg1 = large_font.render("Game Over!", True, RED)
        msg2 = font.render(f"Your Score: {score}", True, WHITE)
        retry_button = pygame.Rect(WINDOW_WIDTH//2 - 120, WINDOW_HEIGHT//2, 100, 50)
        quit_button = pygame.Rect(WINDOW_WIDTH//2 + 20, WINDOW_HEIGHT//2, 100, 50)
        pygame.draw.rect(screen, BLUE, retry_button)
        pygame.draw.rect(screen, BLUE, quit_button)
        screen.blit(msg1, (WINDOW_WIDTH//2 - 130, WINDOW_HEIGHT//2 - 100))
        screen.blit(msg2, (WINDOW_WIDTH//2 - 70, WINDOW_HEIGHT//2 - 40))
        screen.blit(font.render("Retry", True, WHITE), (retry_button.x + 20, retry_button.y + 10))
        screen.blit(font.render("Quit", True, WHITE), (quit_button.x + 30, quit_button.y + 10))
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if retry_button.collidepoint(event.pos):
                        waiting = False
                        start_game(player_name)
                    elif quit_button.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

    # Main loop
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_score()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and direction != (snake_block, 0):
                    direction = (-snake_block, 0)
                elif event.key == pygame.K_RIGHT and direction != (-snake_block, 0):
                    direction = (snake_block, 0)
                elif event.key == pygame.K_UP and direction != (0, snake_block):
                    direction = (0, -snake_block)
                elif event.key == pygame.K_DOWN and direction != (0, -snake_block):
                    direction = (0, snake_block)

        x = snake[-1][0] + direction[0]
        y = snake[-1][1] + direction[1]

        # Game boundaries
        if x < 0 or x >= WINDOW_WIDTH or y < HEADER_HEIGHT or y >= WINDOW_HEIGHT:
            save_score()
            game_over_screen()

        new_head = (x, y)
        snake.append(new_head)

        # Check if snake eats food
        if new_head == food:
            score += 10
            food = (random.randrange(0, (WINDOW_WIDTH - snake_block)//snake_block) * snake_block,
                    random.randrange(HEADER_HEIGHT//snake_block, (WINDOW_HEIGHT - snake_block)//snake_block) * snake_block)
        else:
            snake.pop(0)

        # Check self collision
        if len(snake) != len(set(snake)):
            save_score()
            game_over_screen()

        # Draw everything
        screen.fill(BLACK)
        show_score()
        pygame.draw.rect(screen, RED, [food[0], food[1], snake_block, snake_block])
        draw_snake(snake)
        pygame.display.flip()
        clock.tick(snake_speed)


# Run the game
player_name = get_player_name()
start_game(player_name)
