import pygame
import random

# --- Initialization ---
pygame.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)  # Snake color
RED = (255, 0, 0)    # Food color

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Snake Game")

# Game clock for frame rate control
clock = pygame.time.Clock()

# --- Game Variables ---
SNAKE_SIZE = 20  # Size of a single snake segment and food
SNAKE_SPEED = 10 # How many segments the snake moves per second (FPS)

# Snake head initial position and starting direction
snake_x = SCREEN_WIDTH // 2
snake_y = SCREEN_HEIGHT // 2
direction_x = SNAKE_SIZE # Start moving right
direction_y = 0

# Snake segments list - starts with just the head
snake_segments = []
snake_length = 1

# Food initial position (needs to be generated in a good spot)
def generate_food():
    # Ensure food is placed on a grid aligned with the snake size
    food_x = round(random.randrange(0, SCREEN_WIDTH - SNAKE_SIZE) / SNAKE_SIZE) * SNAKE_SIZE
    food_y = round(random.randrange(0, SCREEN_HEIGHT - SNAKE_SIZE) / SNAKE_SIZE) * SNAKE_SIZE
    return food_x, food_y

food_x, food_y = generate_food()

# --- Functions ---

def draw_snake(segments):
    """Draws all segments of the snake."""
    for segment in segments:
        pygame.draw.rect(screen, GREEN, [segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE])

def game_loop():
    global snake_x, snake_y, direction_x, direction_y, snake_segments, snake_length, food_x, food_y

    game_over = False
    game_exit = False

    while not game_exit:
        while game_over == True:
            # Simple game over screen (can be expanded)
            screen.fill(BLACK)
            font = pygame.font.SysFont("monospace", 40)
            text = font.render("Game Over! Press C to Play Again or Q to Quit", True, WHITE)
            screen.blit(text, [SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2])
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit = True
                    game_over = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_exit = True
                        game_over = False
                    if event.key == pygame.K_c:
                        # Reset the game
                        snake_x = SCREEN_WIDTH // 2
                        snake_y = SCREEN_HEIGHT // 2
                        direction_x = SNAKE_SIZE
                        direction_y = 0
                        snake_segments = []
                        snake_length = 1
                        food_x, food_y = generate_food()
                        game_over = False

        # --- Event Handling (User Input) ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            
            if event.type == pygame.KEYDOWN:
                # Change direction, but prevent immediate reversal (e.g., left then instantly right)
                if event.key == pygame.K_LEFT and direction_x == 0:
                    direction_x = -SNAKE_SIZE
                    direction_y = 0
                elif event.key == pygame.K_RIGHT and direction_x == 0:
                    direction_x = SNAKE_SIZE
                    direction_y = 0
                elif event.key == pygame.K_UP and direction_y == 0:
                    direction_y = -SNAKE_SIZE
                    direction_x = 0
                elif event.key == pygame.K_DOWN and direction_y == 0:
                    direction_y = SNAKE_SIZE
                    direction_x = 0

        # --- Game Logic: Movement ---
        snake_x += direction_x
        snake_y += direction_y

        # --- Game Logic: Collisions ---
        
        # 1. Collision with Walls
        if snake_x >= SCREEN_WIDTH or snake_x < 0 or snake_y >= SCREEN_HEIGHT or snake_y < 0:
            game_over = True

        # 2. Collision with Food
        if snake_x == food_x and snake_y == food_y:
            food_x, food_y = generate_food()
            snake_length += 1

        # 3. Collision with Self (Only check if snake is long enough)
        if len(snake_segments) > 1:
            for segment in snake_segments[:-1]: # Check every segment except the head
                if segment[0] == snake_x and segment[1] == snake_y:
                    game_over = True

        # --- Snake Segment Management ---
        
        # Add the new head position to the segment list
        snake_head = [snake_x, snake_y]
        snake_segments.append(snake_head)
        
        # Delete the tail if the snake hasn't eaten (maintains the length)
        if len(snake_segments) > snake_length:
            del snake_segments[0]
        
        # --- Drawing ---
        screen.fill(BLACK) # Clear the screen

        # Draw the Food (Red square)
        pygame.draw.rect(screen, RED, [food_x, food_y, SNAKE_SIZE, SNAKE_SIZE])

        # Draw the Snake
        draw_snake(snake_segments)

        # Update the entire screen
        pygame.display.update()

        # Control the game speed
        clock.tick(SNAKE_SPEED) 

    pygame.quit()
    quit()

# --- Run the Game ---
game_loop()