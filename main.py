import pygame
from random import randint

pygame.init()
pygame.mixer.init()

screen_width = 1200
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird")

clock = pygame.time.Clock()

background = pygame.image.load("images/background.png").convert_alpha()
background = pygame.transform.rotozoom(background, 0, 1.5)
background_rect = background.get_frect(center = (screen_width / 2, 250))

floor = pygame.image.load("images/floor.png").convert_alpha()
floor = pygame.transform.rotozoom(floor, 0, 3.6)
floor_rect = background.get_frect(center = (675, 965))

bird_x_pos = 300
bird_y_pos = 200
gravity = 2.5
jump_strength = 65

bird_animation = [
    pygame.transform.rotozoom(pygame.image.load("images/bird_up.png").convert_alpha(), 0, 2),
    pygame.transform.rotozoom(pygame.image.load("images/bird.png").convert_alpha(), 0, 2),
    pygame.transform.rotozoom(pygame.image.load("images/bird_down.png").convert_alpha(), 0, 2)
]

bird_index = 0
bird = bird_animation[bird_index]
bird_rect = bird.get_frect(center=(bird_x_pos, bird_y_pos))

pipe_x_pos = screen_width

pipe_1 = pygame.image.load("images/pipe_1.png").convert_alpha()
pipe_1 = pygame.transform.rotozoom(pipe_1, 0 , 2)
pipe_1_y_pos = -200
pipe_1_rect = pipe_1.get_frect(center = (pipe_x_pos, pipe_1_y_pos))

pipe_2 = pygame.image.load("images/pipe_2.png").convert_alpha()
pipe_2 = pygame.transform.rotozoom(pipe_2, 0 , 2)
pipe_2_y_pos = 700
pipe_2_rect = pipe_2.get_frect(center = (pipe_x_pos, pipe_2_y_pos))

pipe_list = []

def create_pipe():
    pipe_x = screen_width + 100
    gap = randint(0, 55)

    top_pipe_rect = pipe_1.get_frect(center=(pipe_x, pipe_1_y_pos + gap))
    bottom_pipe_rect = pipe_2.get_frect(center=(pipe_x, pipe_2_y_pos - gap))

    return (top_pipe_rect, bottom_pipe_rect)

pipe_spawn = pygame.USEREVENT
pygame.time.set_timer(pipe_spawn, randint(500,2500))

wing_sound = pygame.mixer.Sound("audio/wing.wav")
wing_sound.set_volume(0.2)
death_sound = pygame.mixer.Sound("audio/death.wav")
death_sound.set_volume(0.2)
hit_sound = pygame.mixer.Sound("audio/hit.wav")
hit_sound.set_volume(0.2)
point_sound = pygame.mixer.Sound("audio/point.wav")
point_sound.set_volume(0.2)
swoosh_sound = pygame.mixer.Sound("audio/swoosh.wav")
swoosh_sound.set_volume(0.2)

game_active = True

bird_animation_timer = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pipe_spawn:
            pipe_list.append(create_pipe())
            pygame.time.set_timer(pipe_spawn, randint(500, 2500))

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_active:
                    bird_y_pos -= jump_strength
                    bird_rect = bird.get_rect(center = (bird_x_pos, bird_y_pos))
                    wing_sound.play()

                else:
                    bird_y_pos = 200
                    bird_rect = bird.get_rect(center=(bird_x_pos, bird_y_pos))
                    pipe_list.clear()
                    game_active = True

    if game_active == True:

        screen.blit(background, background_rect)

        bird_animation_timer += 1

        if bird_animation_timer > 5:
            bird_animation_timer = 0
            bird_index += 1
            if bird_index >= len(bird_animation):
                bird_index = 0

        bird = bird_animation[bird_index]
        bird_rect = bird.get_frect(center=(bird_x_pos, bird_y_pos))

        screen.blit(bird, bird_rect)

        for top_pipe, bottom_pipe in pipe_list:
            top_pipe.centerx -= 5
            bottom_pipe.centerx -= 5

            screen.blit(pipe_1, top_pipe)
            screen.blit(pipe_2, bottom_pipe)

        for top_pipe, bottom_pipe in pipe_list:
            if bird_rect.colliderect(top_pipe) or bird_rect.colliderect(bottom_pipe):
                game_active = False
                hit_sound.play()
                death_sound.play()

        pipe_list = [pair for pair in pipe_list if pair[0].right > -50]

        screen.blit(floor, floor_rect)

        bird_y_pos += gravity
        bird_rect = bird.get_rect(center=(bird_x_pos, bird_y_pos))

        if bird_rect.bottom >= floor_rect.top or bird_rect.top <= 0:
            game_active = False
            hit_sound.play()
            death_sound.play()

    if not game_active:
        death_font = pygame.font.Font(None, 50)
        death_text = death_font.render(f"Game over! Press Space to try again!", True, "red")
        death_text_rect = death_text.get_frect(center=(screen_width / 2, screen_height / 2))

        screen.blit(floor, floor_rect)

        screen.blit(bird, bird_rect)
        screen.blit(death_text, death_text_rect)

    pygame.display.update()
    clock.tick(60)

