import pygame
import random

pygame.init()

WIDTH, HEIGHT = 600, 400
block_size = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game!")

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

snake = [(100, 100), (90, 100), (80, 100)]
direction = "RIGHT"

food = (random.randint(0, (WIDTH // block_size) - 1) * block_size,
        random.randint(0, (HEIGHT // block_size) - 1) * block_size)

score = 0
font = pygame.font.SysFont("arial", 24)
eat_sound = pygame.mixer.Sound("Music/eat.mp3")
game_over_sound = pygame.mixer.Sound("Music/game_over.mp3")

def move_snake(snake_body, snake_dir):
    head_x, head_y = snake_body[-1]
    if snake_dir == "UP":
        new_head = (head_x, head_y - block_size)
    elif snake_dir == "DOWN":
        new_head = (head_x, head_y + block_size)
    elif snake_dir == "LEFT":
        new_head = (head_x - block_size, head_y)
    elif snake_dir == "RIGHT":
        new_head = (head_x + block_size, head_y)
    snake_body.append(new_head)

def draw_snake(snake_body):
    for segment in snake_body:
        pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0], segment[1], block_size, block_size))

def show_score(score):
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def show_game_over(score):
    screen.fill(BLACK)
    game_over_text = font.render("GAME OVER!", True, RED)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    restart_text = font.render("Press R to Restart or Q to Quit", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 1.5))
    pygame.display.flip()

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != "DOWN":
                direction = "UP"
            elif event.key == pygame.K_DOWN and direction != "UP":
                direction = "DOWN"
            elif event.key == pygame.K_LEFT and direction != "RIGHT":
                direction = "LEFT"
            elif event.key == pygame.K_RIGHT and direction != "LEFT":
                direction = "RIGHT"

    move_snake(snake, direction)

    if snake[-1] == food:
        pygame.mixer.Sound.play(eat_sound)
        food = (random.randint(0, (WIDTH // block_size) - 1) * block_size,
                random.randint(0, (HEIGHT // block_size) - 1) * block_size)
        score += 1
    else:
        snake.pop(0)

    head_x, head_y = snake[-1]
    if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT or snake[-1] in snake[:-1]:
        pygame.mixer.Sound.play(game_over_sound)
        show_game_over(score)
        while True:
            event = pygame.event.wait()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # Restart the game
                    snake = [(100, 100), (90, 100), (80, 100)]
                    direction = "RIGHT"
                    food = (random.randint(0, (WIDTH // block_size) - 1) * block_size,
                            random.randint(0, (HEIGHT // block_size) - 1) * block_size)
                    score = 0
                    break
                elif event.key == pygame.K_q:
                    running = False
                    break

    screen.fill(BLACK)
    draw_snake(snake)
    pygame.draw.rect(screen, RED, pygame.Rect(food[0], food[1], block_size, block_size))
    show_score(score)
    pygame.display.flip()

    clock.tick(5 + len(snake) // 5)

pygame.quit()
