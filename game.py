import pygame  # 1. Import the Pygame library

# 2. Initialization
pygame.init()

# 3. Setup the screen/display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Simple Movement") # Optional: Set window title

# Initial variables
x, y = 100, 100
speed = 5
running = True # 4. Make sure 'running' is defined

# Game Loop
while running:
    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Key Press Handling
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x -= speed
    if keys[pygame.K_RIGHT]:
        x += speed

    # Drawing/Rendering
    screen.fill((0, 0, 0))  # Fill the screen with black
    # Draw a red square (rect) at (x, y) with a width/height of 50
    pygame.draw.rect(screen, (255, 0, 0), (x, y, 50, 50))
    
    # Update the display
    pygame.display.update()

# 5. Quit Pygame
pygame.quit()