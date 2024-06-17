import pygame
import random

# Print welcome message in the Python IDLE Shell
print('Welcome to our game "Geometry Dash"!')

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Geometry Dash")

# Clock to control the frame rate
clock = pygame.time.Clock()

# Fonts
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

# Function to display a message
def display_message(message, size, color, y_offset=0):
    text = pygame.font.Font(None, size).render(message, True, color)
    text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + y_offset))
    screen.blit(text, text_rect)

# Welcome screen to get user name
def welcome_screen():
    global name
    name = ""
    input_active = True
    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if name:
                        input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode

        screen.fill(WHITE)
        display_message("Enter your name:", 74, BLACK, -50)
        display_message(name, 74, BLACK)
        pygame.display.flip()
        clock.tick(30)

    return name

# Player properties
player_size = 50
player_x = 50
player_y = SCREEN_HEIGHT - player_size
player_color = GREEN
player_jump = False
player_velocity_y = 0
GRAVITY = 1

# Obstacle properties
obstacle_width = 50
obstacle_height = 50
obstacle_color = RED
obstacle_x = SCREEN_WIDTH
obstacle_y = SCREEN_HEIGHT - obstacle_height
obstacle_speed = 10

# Speed increment properties
frame_count = 0
speed_increment_interval = 120  # Increase speed every 120 frames (approximately every 4 seconds at 30 FPS)
speed_increment_amount = 1

# Score tracking
score = 0

# Welcome the player and get their name
player_name = welcome_screen()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not player_jump:
                player_jump = True
                player_velocity_y = -20

    # Apply gravity
    if player_jump:
        player_velocity_y += GRAVITY
        player_y += player_velocity_y
        if player_y >= SCREEN_HEIGHT - player_size:
            player_y = SCREEN_HEIGHT - player_size
            player_jump = False

    # Move the obstacle
    obstacle_x -= obstacle_speed
    if obstacle_x < 0:
        obstacle_x = SCREEN_WIDTH
        # Randomize obstacle height if desired
        # obstacle_height = random.randint(20, 100)
        score += 1  # Increase score when obstacle is passed

    # Check for collision
    if (player_x < obstacle_x < player_x + player_size or player_x < obstacle_x + obstacle_width < player_x + player_size) and (player_y > obstacle_y - player_size):
        running = False

    # Increment frame count
    frame_count += 1

    # Increase obstacle speed at intervals
    if frame_count % speed_increment_interval == 0:
        obstacle_speed += speed_increment_amount

    # Clear the screen
    screen.fill(WHITE)

    # Draw player
    pygame.draw.rect(screen, player_color, (player_x, player_y, player_size, player_size))

    # Draw obstacle
    pygame.draw.rect(screen, obstacle_color, (obstacle_x, obstacle_y, obstacle_width, obstacle_height))

    # Display score
    score_text = small_font.render("Score: " + str(score), True, BLACK)
    screen.blit(score_text, (10, 10))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30)

# Game over screen
screen.fill(WHITE)
display_message(f"Game Over, {player_name}!", 74, RED, -50)
display_message(f"Your score: {score}", 74, BLACK, 50)
pygame.display.flip()
pygame.time.wait(5000)


pygame.quit()
