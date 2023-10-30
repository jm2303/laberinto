from maze_generator import *
import pygame_gui
from datetime import timedelta




def is_collide(x, y):
    tmp_rect = player_rect.move(x, y)
    if tmp_rect.collidelist(walls_collide_list) == -1:
        return False
    return True


def is_game_over():
    global time, score, record, FPS
    #if time < 0:
    #    pygame.time.wait(700)
    #    player_rect.center = TILE // 2, TILE // 2
       # set_record(record, score)
       # record = get_record()
    #    time, score, FPS = 60, 0, 60


def get_record():
    try:
        with open('record') as f:
            return f.readline()
    except FileNotFoundError:
        with open('record', 'w') as f:
            f.write('0')
            return 0


def set_record(record, score):
    rec = max(int(record), score)
    with open('record', 'w') as f:
        f.write(str(rec))


FPS = 60
pygame.init()
game_surface = pygame.Surface(RES)
surface = pygame.display.set_mode((WIDTH + 300, HEIGHT))
clock = pygame.time.Clock()

# images
cheese_image = pygame.image.load(r'images/queso.png').convert_alpha()
cheese_image = pygame.transform.scale(cheese_image,(TILE  *1.2, TILE*1.2))

#UI elements
manager = pygame_gui.UIManager((1600, 900))

# get maze
maze = generate_maze()

# player settings
player_speed = 1
player_img = pygame.image.load(r'images\flecha.png').convert()
player_img.set_colorkey('white') 
player_img = pygame.transform.scale(player_img, ((TILE ) - 8 , TILE -8))
player_rect = player_img.get_rect()
player_rect.center = TILE // 2, TILE // 2
directions = {'a': (-player_speed, 0), 'd': (player_speed, 0), 'w': (0, -player_speed), 's': (0, player_speed)}
player_angles = {'a': 90, 'd': -90, 'w': 0, 's': 180}
keys = {'a': pygame.K_LEFT, 'd': pygame.K_RIGHT, 'w': pygame.K_UP, 's': pygame.K_DOWN}
direction = (0, 0)
game_starting_time = pygame.time.get_ticks()
# food settings

# collision list
walls_collide_list = sum([cell.get_rects() for cell in maze], [])

# timer, score, record
pygame.time.set_timer(pygame.USEREVENT, 1000)
score = 0
game_angle = 0
player_angle = 0
ROTATION_TIMER_SEC = 15
last_rotation = pygame.time.get_ticks()

# fonts
font = pygame.font.SysFont('Impact', 150)
text_font = pygame.font.SysFont('Impact', 60)
small_font = pygame.font.SysFont('Impact', 30)

UI_REFRESH_RATE = clock.tick(60)/1000
slider_input  = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((WIDTH + 50, 330),(200, 50)),
                                                     start_value=15,value_range=(15,40),
                                                     manager=manager,
                                                    object_id='-ROTATION_SLIDER-')

while True:
    #surface.blit(bg, (WIDTH, 0))
    #game_surface.fill('black')
    surface.fill('black')
    game_surface.fill('black')

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    if (event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED and
                event.ui_object_id == '-ROTATION_SLIDER-'):
                ROTATION_TIMER_SEC = int(slider_input.current_value)
            
    manager.process_events(event)
        
    manager.update(UI_REFRESH_RATE)

    # controls and movement
    pressed_key = pygame.key.get_pressed()
    for key, key_value in keys.items():
        if pressed_key[key_value] and not is_collide(*directions[key]):
            direction = directions[key]
            player_angle = player_angles[key]
            player_rect.move_ip(direction)   
            break
            
   # if not is_collide(*direction):
   #     player_rect.move_ip(direction)
    if pressed_key[pygame.K_n]:
        maze = generate_maze()
        player_rect.center = TILE // 2, TILE // 2
        game_starting_time = pygame.time.get_ticks()
    
    if pygame.time.get_ticks() - last_rotation > ROTATION_TIMER_SEC * 1000:
        game_angle = game_angle  +90
        if game_angle > 270:
            game_angle = 0
        last_rotation = pygame.time.get_ticks()
    # draw maze
    for cell in maze:
        cell.draw(game_surface) 

    # gameplay
    
    is_game_over()

    # draw player
    rotated_player = pygame.transform.rotate(player_img,player_angle)
    pygame.draw.rect(game_surface,'black',(0,0,TILE-8,TILE))
    game_surface.blit(rotated_player, player_rect)
    game_surface.blit(cheese_image,(game_surface.get_width()-cheese_image.get_width() - 10,
                                     game_surface.get_height()-cheese_image.get_height()- 10))
    rotated_surface = pygame.transform.rotate(game_surface,game_angle)
    surface.blit(rotated_surface, (2, 2))


     # draw stats
    sec=(  pygame.time.get_ticks() - game_starting_time )/1000
 

    surface.blit(text_font.render('Tiempo', True, pygame.Color('cyan'), True), (WIDTH + 30, 30))
    #surface.blit(font.render(f'{(pygame.time.get_ticks() - last_rotation)//1000}', True, pygame.Color('cyan')), (WIDTH + 70, 130))
    surface.blit(text_font.render(str(timedelta(seconds=sec)), True, pygame.Color('magenta')), (WIDTH + 50, 130))
    surface.blit(text_font.render('Rotación (seg)', True, pygame.Color('cyan')), (WIDTH + 30, 230))
    manager.draw_ui(surface)
    surface.blit(small_font.render(str(ROTATION_TIMER_SEC), True, pygame.Color('magenta')), (WIDTH + 260, 340))


    pygame.display.flip()
    clock.tick(FPS)
    


   

    # print(clock.get_fps())
