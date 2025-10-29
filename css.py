import pygame
import random
import time

# --- Initialization ---
pygame.init()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)       # Snake body color
BRIGHT_GREEN = (0, 255, 0) # Snake head color
RED = (255, 0, 0)         # Food color
YELLOW = (255, 255, 102) # Color for score text

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Snake Game - Custom Look")

# Game clock for frame rate control
clock = pygame.time.Clock()

# --- Game Variables (Defined Globally) ---
SNAKE_SIZE = 20  # Size of a single snake segment and food
SNAKE_SPEED = 10 # How many segments the snake moves per second (FPS)

# Snake head initial position and starting direction
snake_x = SCREEN_WIDTH // 2
snake_y = SCREEN_HEIGHT // 2
direction_x = SNAKE_SIZE # Start moving right
direction_y = 0

# Snake segments list - starts empty but will hold coordinates
snake_segments = []
snake_length = 1

# --- Food Function ---
def generate_food():
    """Generates food coordinates aligned with the snake grid."""
    food_x = round(random.randrange(0, SCREEN_WIDTH - SNAKE_SIZE) / SNAKE_SIZE) * SNAKE_SIZE
    food_y = round(random.randrange(0, SCREEN_HEIGHT - SNAKE_SIZE) / SNAKE_SIZE) * SNAKE_SIZE
    return food_x, food_y

# Generate initial food
food_x, food_y = generate_food()

# --- Drawing Function (Custom Style) ---

def draw_snake(segments):
    """Draws all segments of the snake using circles, with a distinct head color."""
    
    # 1. Draw the body segments (all segments except the last one, which is the head)
    for segment in segments[:-1]:
        center_x = segment[0] + SNAKE_SIZE // 2
        center_y = segment[1] + SNAKE_SIZE // 2
        radius = SNAKE_SIZE // 2 - 1 # Slightly smaller radius for a visible gap
        pygame.draw.circle(screen, GREEN, (center_x, center_y), radius)
        
    # 2. Draw the head (the last segment in the list)
    if segments:
        head = segments[-1]
        head_center_x = head[0] + SNAKE_SIZE // 2
        head_center_y = head[1] + SNAKE_SIZE // 2
        head_radius = SNAKE_SIZE // 2
        
        # Draw the head with a brighter color
        pygame.draw.circle(screen, BRIGHT_GREEN, (head_center_x, head_center_y), head_radius)

# --- Message Function ---

def message(msg, color, y_offset=0):
    """Displays a message on the screen."""
    font_style = pygame.font.SysFont("monospace", 40)
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [SCREEN_WIDTH // 2 - mesg.get_width() // 2, SCREEN_HEIGHT // 2 + y_offset])

# --- Score Display Function (NEW) ---
def display_score(score):
    """Renders and displays the current score in the top left."""
    font = pygame.font.SysFont("monospace", 28)
    # The score is snake_length - 1 (since the starting length is 1)
    value = font.render(f"Score: {score}", True, YELLOW)
    screen.blit(value, [10, 10]) # Positioned at (10, 10) from top left


# --- Main Game Loop ---

def game_loop():
    # VITAL FIX: Declare all global variables used/modified in this function
    global snake_x, snake_y, direction_x, direction_y, snake_segments, snake_length, food_x, food_y 

    game_over = False
    game_exit = False

    while not game_exit:
        while game_over == True:
            # Game over screen
            screen.fill(BLACK)
            message("Game Over!", RED, -50)
            message(f"Final Score: {snake_length - 1}", WHITE, 0)
            message("Press C to Play Again or Q to Quit", WHITE, 50)
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
                        # Reset the game state
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
                # Change direction, preventing immediate 180-degree turns
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
            # Give a little pause when the snake eats
            time.sleep(0.01)

        # 3. Collision with Self
        snake_head = [snake_x, snake_y]
        
        # Must append the new head position AFTER checking for self-collision with the current segments
        if snake_head in snake_segments:
            game_over = True

        # Now update the segments list
        snake_segments.append(snake_head)
        
        # Delete the tail if the snake hasn't eaten
        if len(snake_segments) > snake_length:
            del snake_segments[0]
        
        # --- Drawing ---
        screen.fill(BLACK) # Clear the screen

        # Draw the Food
        pygame.draw.rect(screen, RED, [food_x, food_y, SNAKE_SIZE, SNAKE_SIZE])

        # Draw the Snake (using the custom circular function)
        draw_snake(snake_segments)
        
        # --- Display Live Score (NEW) ---
        # The score is calculated as snake_length - 1
        display_score(snake_length - 1) 

        # Update the entire screen
        pygame.display.update()

        # Control the game speed
        clock.tick(SNAKE_SPEED) 

    pygame.quit()
    quit()

# --- Run the Game ---
game_loop()
