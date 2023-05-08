import pygame
from random import randrange


WINDOW = 700
TILE_SIZE = 50
RANGE = (TILE_SIZE // 2, WINDOW - (TILE_SIZE // 2), TILE_SIZE)
get_random_position = lambda: [randrange(*RANGE), randrange(*RANGE)]

# define snake
snake = pygame.rect.Rect(0, 0, TILE_SIZE - 2, TILE_SIZE - 2)
snake.center = get_random_position()
length = 1
segments = [snake.copy()]
snake_dir = (0, 0)

# define food
food = snake.copy()
food.center = get_random_position()

time, time_step = 0, 110

pygame.init()
screen = pygame.display.set_mode([WINDOW] * 2)
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                if length > 1 and snake_dir[1] > 0:
                    # if try to move in opposite direction, kill snake
                    snake.center, food.center = get_random_position(), get_random_position()
                    length = 1
                    snake_dir = (0, 0)
                    segments = [snake.copy()]
                else:
                    snake_dir = (0, -TILE_SIZE)
            if event.key == pygame.K_s:
                if length > 1 and snake_dir[1] < 0:
                    snake.center, food.center = get_random_position(), get_random_position()
                    length = 1
                    snake_dir = (0, 0)
                    segments = [snake.copy()]
                else:
                    snake_dir = (0, TILE_SIZE)
            if event.key == pygame.K_a:
                if length > 1 and snake_dir[0] > 0:
                    snake.center, food.center = get_random_position(), get_random_position()
                    length = 1
                    snake_dir = (0, 0)
                    segments = [snake.copy()]
                else:
                    snake_dir = (-TILE_SIZE, 0)
            if event.key == pygame.K_d:
                if length > 1 and snake_dir[0] < 0:
                    snake.center, food.center = get_random_position(), get_random_position()
                    length = 1
                    snake_dir = (0, 0)
                    segments = [snake.copy()]
                else:
                    snake_dir = (TILE_SIZE, 0)
        
    screen.fill("black")
        
    # check for death conditions (borders and self-eating)
    self_eating = pygame.Rect.collidelist(snake, segments[:-1]) != -1
    if snake.left < 0 or snake.right > WINDOW or snake.top < 0 or snake.bottom > WINDOW or self_eating:
        # if dead, reset snake and food
        snake.center, food.center = get_random_position(), get_random_position()
        length = 1
        snake_dir = (0, 0)
        segments = [snake.copy()]

    # draw food
    pygame.draw.rect(screen, 'red', food)
    
    # draw snake
    for segment in segments:
        pygame.draw.rect(screen, 'green', segment)
    
    # eat food
    if snake.center == food.center:        
        food.center = get_random_position()
        
        # regenerate food if generated inside snake
        while pygame.Rect.collidelist(food, segments[:]) != -1:
            food.center = get_random_position()
            
        length += 1
    
    # move snake
    time_now = pygame.time.get_ticks()
    if time_now - time > time_step:
        time = time_now
        
        snake.move_ip(snake_dir)
        segments.append(snake.copy())
        segments = segments[-length:]
    
    pygame.display.flip()
    clock.tick(60)