import pygame
import random
import time

# pygame
pygame.init()

# windows
window_width = 800
window_height = 600

# Set up the display
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Arcade Ball Game')

# just colors 🤨
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)

# fps
fps = 60
clock = pygame.time.Clock()

# Ball properties
ball_radius = 10
ball_x = window_width // 2
ball_y = window_height // 2
ball_dx = 5
ball_dy = -5  # ball always go up at start

# paddle properties
paddle_width = 100
paddle_height = 10
paddle_x = (window_width - paddle_width) // 2
paddle_y = window_height - paddle_height - 10
paddle_dx = 10

# state
game_over = False
score = 0
start_time = time.time()

# font
font = pygame.font.SysFont(None, 55)
small_font = pygame.font.SysFont(None, 35)

def show_game_over():
    game_over_text = font.render('Game Over', True, red)
    restart_button_text = font.render('Restart', True, green)
    window.blit(game_over_text, (window_width // 2 - game_over_text.get_width() // 2, window_height // 2 - 50))
    restart_button_rect = restart_button_text.get_rect(center=(window_width // 2, window_height // 2 + 50))
    window.blit(restart_button_text, restart_button_rect)
    # Draw an outline for the button
    pygame.draw.rect(window, green, restart_button_rect.inflate(20, 10), 2)
    return restart_button_rect

def restart_game():
    global ball_x, ball_y, ball_dx, ball_dy, paddle_x, game_over, score, start_time
    ball_x = window_width // 2
    ball_y = window_height // 2
    ball_dx = random.choice([-5, 5])
    ball_dy = -5
    paddle_x = (window_width - paddle_width) // 2
    game_over = False
    score = 0
    start_time = time.time()

def draw_score_and_timer():
    elapsed_time = int(time.time() - start_time)
    score_text = small_font.render(f'Score: {score}', True, black)
    timer_text = small_font.render(f'Time: {elapsed_time}s', True, black)
    window.blit(score_text, (10, 10))
    window.blit(timer_text, (10, 50))

# loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and game_over:
            mouse_x, mouse_y = event.pos
            if restart_button_rect.collidepoint(mouse_x, mouse_y):
                restart_game()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle_x > 0:
        paddle_x -= paddle_dx
    if keys[pygame.K_RIGHT] and paddle_x < window_width - paddle_width:
        paddle_x += paddle_dx

    if not game_over:
        # movement of ball
        ball_x += ball_dx
        ball_y += ball_dy

        # ball collision and walls
        if ball_x <= ball_radius or ball_x >= window_width - ball_radius:
            ball_dx = -ball_dx
        if ball_y <= ball_radius:
            ball_dy = -ball_dy

        # ball collision
        if (paddle_y <= ball_y + ball_radius <= paddle_y + paddle_height and
                paddle_x <= ball_x <= paddle_x + paddle_width):
            ball_dy = -ball_dy
            score += 1  # Increment score when ball hits the paddle

        # ball things
        if ball_y >= window_height - ball_radius:
            game_over = True

    # clears the screen
    window.fill(white)

    if game_over:
        restart_button_rect = show_game_over()
    else:
        # ball
        pygame.draw.circle(window, red, (ball_x, ball_y), ball_radius)

        # paddle
        pygame.draw.rect(window, blue, (paddle_x, paddle_y, paddle_width, paddle_height))

        # score and timer
        draw_score_and_timer()

    # Updates the display
    pygame.display.update()

    # Cap for frame rate
    clock.tick(fps)

# Quit
pygame.quit()