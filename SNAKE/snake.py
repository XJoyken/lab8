import pygame
import random

#Initialization
pygame.init()
clock = pygame.time.Clock()
WIDTH, HEIGHT = 700,700
screen = pygame.display.set_mode((WIDTH, HEIGHT))

#Colors
DARK_GREEN = (0, 111, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

#Fonts
font = pygame.font.SysFont("Verdana", 20)
font_large = pygame.font.SysFont("Verdana", 50)
font_medium = pygame.font.SysFont("Verdana", 30)

#Variables
snake = [
    [10, 10],
    [20, 10],
    [30, 10]
]

fruit = []
dir = "right"
new_dir = "right"
head = snake[-1]
FPS = 5
fruit_eaten = False
score = 0
level = 1
initial_moves = 0
running = True

#Function for game ending
def game_over(score, level):
    game_over_text = font_large.render("GAME OVER", True, BLACK)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
    end1_text = font_medium.render("Your score is: " + str(score), True, BLACK)
    end2_text = font_medium.render("Your level is: " + str(level), True, BLACK)
    screen.blit(end1_text, (WIDTH // 2 - end1_text.get_width() // 2, HEIGHT // 2 + game_over_text.get_height() // 2 + 20))
    screen.blit(end2_text,
                (WIDTH // 2 - end2_text.get_width() // 2, HEIGHT // 2 + game_over_text.get_height() // 2 + end1_text.get_height() + 40))
    pygame.display.update()
    pygame.time.delay(5000)

#Main loop
while running:
    #Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                new_dir = "down"
            if event.key == pygame.K_UP:
                new_dir = "up"
            if event.key == pygame.K_RIGHT:
                new_dir = "right"
            if event.key == pygame.K_LEFT:
                new_dir = "left"

    #Changing direction
    if new_dir == "right" and dir != "left":
        dir = "right"
    if new_dir == "left" and dir != "right":
        dir = "left"
    if new_dir == "up" and dir != "down":
        dir = "up"
    if new_dir == "down" and dir != "up":
        dir = "down"

    #Setting the coordinates of fruit
    while len(fruit) == 0:
        fruit_x = random.randint(0, WIDTH // 10 - 10) * 10
        fruit_y = random.randint(0, HEIGHT // 10 - 10) * 10
        fruit.append(fruit_x)
        fruit.append(fruit_y)
        fruit_rect = pygame.Rect(fruit[0], fruit[1], 10, 10)
        check_collision = True
        for body in snake:
            body_rect = pygame.Rect(body[0], body[1], 10, 10)
            if fruit_rect.colliderect(body_rect):
                check_collision = False
                break
        if check_collision:
            fruit_eaten = False
            break
        else: fruit.clear()

    screen.fill(WHITE)

    #Draw the circle if the fruit has not been eaten
    if fruit_eaten == False: pygame.draw.circle(screen, RED, (fruit[0] + 5, fruit[1] + 5), 5)

    #Draw the snake
    end = snake[-1]
    for body in snake:
        if body[0] == end[0] and body[1] == end[1]:
            pygame.draw.rect(screen, DARK_GREEN, pygame.Rect(body[0], body[1], 10, 10))
        else: pygame.draw.rect(screen, GREEN, pygame.Rect(body[0], body[1], 10, 10))

    # Score and level
    score_text = font.render("Score: " + str(score), True, BLACK)
    level_text = font.render("Level: " + str(level), True, BLACK)
    screen.blit(score_text, (WIDTH - score_text.get_width() - 10, 10))
    screen.blit(level_text, (WIDTH - level_text.get_width() - 10, score_text.get_height() + 10))

    #Move the snake
    if dir == "down":
        head[1] += 10
    if dir == "up":
        head[1] -= 10
    if dir == "right":
        head[0] += 10
    if dir == "left":
        head[0] -= 10

    #Operations to add a body to a snake
    new_head = [head[0], head[1]]
    snake.append(new_head)
    snake.pop(0)
    new_head_rect = pygame.Rect(new_head[0], new_head[1], 10, 10)

    tail = snake[0]

    #Checking if fruit has been eaten and adding to score
    if new_head_rect.colliderect(fruit_rect):
        fruit_eaten = True
        fruit.clear()
        score += 1
        #Every 4 fruits speeding up
        if score % 4 == 0:
            level += 1
            FPS += 2
        #Adding the tail
        if dir == "down":
            snake.insert(0, [tail[0], tail[1] - 10])
        if dir == "up":
            snake.insert(0, [tail[0], tail[1] + 10])
        if dir == "right":
            snake.insert(0, [tail[0] - 10, tail[1]])
        if dir == "left":
            snake.insert(0, [tail[0] + 10, tail[1]])

    #Checking if the game has been ended
    head_check = snake[-1]
    if head_check[0] < 0 or head_check[0] >= WIDTH or head_check[1] < 0 or head_check[1] >= HEIGHT:
        running = False

    if initial_moves >= 2:
        for body in snake[:-1]:
            if body[0] == head_check[0] and body[1] == head_check[1]:
                running = False
    else:
        initial_moves += 1

    pygame.display.flip()
    clock.tick(FPS)

    #Show the final screen
    if not running:
        game_over(score, level)
pygame.quit()

