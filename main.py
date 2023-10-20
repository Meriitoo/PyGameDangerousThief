import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up the game window in full-screen mode
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

# Get the actual screen width and height
width, height = screen.get_size()

pygame.display.set_caption("The Dangerous Thief")

# Load player images
player_images = [pygame.image.load("player.png"), pygame.image.load("player2.png")]
player_index = 0
player_image = player_images[player_index]
player_size = player_image.get_rect().size
player_x = width // 2 - player_size[0] // 2
player_y = height - player_size[1] - 10
player_speed = 5

# Create a player sprite group
player_group = pygame.sprite.Group()

# Define the Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Create the player sprite and add it to the player group
player = Player(player_image, player_x, player_y)
player_group.add(player)

# Load the initial item image
item_image = pygame.image.load("item.png")
item_size = item_image.get_rect().size
item_x = random.randint(0, width - item_size[0])
item_y = -item_size[1]
item_speed = 3

# Set up power-up image and group
power_up_image = pygame.image.load("powerup.png")
power_up_size = power_up_image.get_rect().size
power_ups = pygame.sprite.Group()

# Set up obstacle image and group
obstacle_image = pygame.image.load("obstacle.png")
obstacle_size = obstacle_image.get_rect().size
obstacles = pygame.sprite.Group()

# Set up the score and level
score = 0

# Define level labels
level_labels = {
    1: pygame.font.Font(None, 36).render("Easy Level", True, (0, 255, 0)),
    2: pygame.font.Font(None, 36).render("Hard Level", True, (255, 0, 0))
}

# Initialize level text
current_level = 1
level_text = level_labels[current_level]

# Set initial game state
STATE_PLAYING = 1
STATE_GAME_OVER = 2
state = STATE_PLAYING

# Set up game over message
game_over_font = pygame.font.Font(None, 72)
game_over_text = game_over_font.render("Time to go to jail!", True, (255, 0, 0))
game_over_text_pos = (width // 2 - game_over_text.get_width() // 2, height // 2 - game_over_text.get_height() // 2)

# Set up new game button
button_font = pygame.font.Font(None, 56)
button_text = button_font.render("New Game", True, (255, 255, 255))
button_text_pos = (width // 2 - button_text.get_width() // 2, height // 2 + game_over_text.get_height() // 2 + 20)
button_rect = pygame.Rect(button_text_pos[0], button_text_pos[1], button_text.get_width(), button_text.get_height())

# Set up exit button text
exit_button_text = button_font.render("Exit", True, (255, 255, 255))
exit_button_text_pos = (
    width // 2 - exit_button_text.get_width() // 2,
    height // 2 + game_over_text.get_height() // 2 + 80,
)
exit_button_rect = pygame.Rect(
    exit_button_text_pos[0],
    exit_button_text_pos[1],
    exit_button_text.get_width(),
    exit_button_text.get_height(),
)

# Define skipped dollars and the maximum allowed
skipped_dollars = 0
max_skipped_dollars = 5  # You can adjust this threshold as needed

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if state == STATE_GAME_OVER:
                if button_rect.collidepoint(event.pos):
                    # Start a new game
                    state = STATE_PLAYING
                    score = 0
                    item_speed = 3
                    player_speed = 5
                    player.rect.x = width // 2 - player_size[0] // 2
                    item_x = random.randint(0, width - item_size[0])
                    item_y = -item_size[1]
                    power_ups.empty()
                    obstacles.empty()
                    player_index = 0
                    player_image = player_images[player_index]
                    player.image = player_image
                    # Reset skipped dollars
                    skipped_dollars = 0
                    # Set the level back to Easy
                    current_level = 1
                    level_text = level_labels[current_level]
                elif exit_button_rect.collidepoint(event.pos):
                    # Exit the game
                    running = False

    if state == STATE_PLAYING:
        # Move the player
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.rect.x > 0:
            player.rect.x -= player_speed
        if keys[pygame.K_RIGHT] and player.rect.x < width - player_size[0]:
            player.rect.x += player_speed

        # Move the items
        item_y += item_speed

        # Spawn power-ups randomly
        if random.randint(1, 1000) == 1:
            power_up = pygame.sprite.Sprite()
            power_up.image = power_up_image
            power_up.rect = power_up.image.get_rect()
            power_up.rect.x = random.randint(0, width - power_up_size[0])
            power_up.rect.y = -power_up_size[1]
            power_ups.add(power_up)

        # Move power-ups
        for power_up in power_ups:
            power_up.rect.y += item_speed

        # Check for collision with power-ups
        power_up_collisions = pygame.sprite.spritecollide(player, power_ups, True)
        for power_up in power_up_collisions:
            # Apply power-up effects (e.g., increase speed)
            player_speed += 2

        # Spawn obstacles randomly
        if random.randint(1, 100) == 1:
            obstacle = pygame.sprite.Sprite()
            obstacle.image = obstacle_image
            obstacle.rect = obstacle.image.get_rect()
            obstacle.rect.x = random.randint(0, width - obstacle_size[0])
            obstacle.rect.y = -obstacle_size[1]
            obstacles.add(obstacle)

        # Move obstacles
        for obstacle in obstacles:
            obstacle.rect.y += item_speed

        # Check for collision with obstacles
        obstacle_collisions = pygame.sprite.spritecollide(player, obstacles, False)
        for obstacle in obstacle_collisions:
            # Handle obstacle collision (e.g., end the game)
            state = STATE_GAME_OVER

        # Check for collision with items
        if player.rect.x < item_x + item_size[0] and player.rect.x + player_size[0] > item_x and player_y < item_y + item_size[1] and player_y + player_size[1] > item_y:
            score += 1
            if score == 5:
                # Switch the player image after reaching a score of 6
                player_index = 1
                player_image = player_images[player_index]
                player.image = player_image
                current_level = 2
                level_text = level_labels[current_level]
                item_image = pygame.image.load("item2.png")
                item_size = item_image.get_rect().size
            elif score == 10:
                item_image = pygame.image.load("item3.png")
                item_size = item_image.get_rect().size
                current_level = 2
            item_x = random.randint(0, width - item_size[0])
            item_y = -item_size[1]

            # Increase speed after every 5 points
            if score % 5 == 0:
                item_speed += 1

        # Check if item goes off the screen
        if item_y > height:
            # Increment the skipped dollars counter
            skipped_dollars += 1
            # End the game if the threshold is reached
            if skipped_dollars >= max_skipped_dollars:
                state = STATE_GAME_OVER

    # Clear the screen
    screen.fill((255, 255, 255))

    # Draw the player
    player_group.draw(screen)

    # Draw the item
    screen.blit(item_image, (item_x, item_y))

    # Draw power-ups
    power_ups.draw(screen)

    # Draw obstacles
    obstacles.draw(screen)

    # Draw the score
    score_text = pygame.font.Font(None, 36).render(f"My stolen money: {score}00", True, (100, 0, 0))
    screen.blit(score_text, (10, 10))

    # Draw the level label
    screen.blit(level_text, (10, 60))

    if state == STATE_GAME_OVER:
        # Draw the game over message
        screen.blit(game_over_text, game_over_text_pos)

        # Draw the new game button
        pygame.draw.rect(screen, (0, 0, 255), button_rect)
        screen.blit(button_text, button_text_pos)

        # Draw the exit button
        pygame.draw.rect(screen, (0, 0, 255), exit_button_rect)
        screen.blit(exit_button_text, exit_button_text_pos)

    # Update the display
    pygame.display.update()

    # Set the frames per second
    clock.tick(60)

# Quit the game
pygame.quit()
sys.exit()
