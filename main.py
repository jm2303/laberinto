from maze_generator import *


def is_collide(x, y):
    tmp_rect = player_rect.move(x, y)
    if tmp_rect.collidelist(walls_collide_list) == -1:
        return False
    return True


def is_game_over():
    global time, score, record, FPS
    if time < 0:
        pygame.time.wait(700)
        player_rect.center = TILE // 2, TILE // 2
       # set_record(record, score)
       # record = get_record()
        time, score, FPS = 60, 0, 60


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
surface = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# images
#bg_game = pygame.image.load('img/bg_1.jpg').convert()
#bg = pygame.image.load('img/bg_main.jpg').convert()

# get maze
maze = generate_maze()

# player settings
player_speed = 5
player_img = pygame.image.load(r'images\raton.jpg').convert_alpha()
player_img = pygame.transform.scale(player_img, (TILE - 2 * maze[0].thickness, TILE - 2 * maze[0].thickness))
player_rect = player_img.get_rect()
player_rect.center = TILE // 2, TILE // 2
directions = {'a': (-player_speed, 0), 'd': (player_speed, 0), 'w': (0, -player_speed), 's': (0, player_speed)}
keys = {'a': pygame.K_a, 'd': pygame.K_d, 'w': pygame.K_w, 's': pygame.K_s}
direction = (0, 0)

# food settings

# collision list
walls_collide_list = sum([cell.get_rects() for cell in maze], [])

# timer, score, record
pygame.time.set_timer(pygame.USEREVENT, 1000)
time = 60
score = 0

# fonts
font = pygame.font.SysFont('Impact', 150)
text_font = pygame.font.SysFont('Impact', 80)

while True:
    #surface.blit(bg, (WIDTH, 0))
    #game_surface.fill('black')
    surface.fill('black')
    surface.blit(game_surface, (0, 0))
    game_surface.fill('black')

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.USEREVENT:
            time -= 1

    # controls and movement
    pressed_key = pygame.key.get_pressed()
    for key, key_value in keys.items():
        if pressed_key[key_value] and not is_collide(*directions[key]):
            direction = directions[key]
            break
    if not is_collide(*direction):
        player_rect.move_ip(direction)

    # draw maze
    for cell in maze:
        cell.draw(game_surface) 

    # gameplay
    
    is_game_over()

    # draw player
    
    game_surface.blit(player_img, player_rect)
    pygame.display.flip()
    clock.tick(FPS)


    # draw stats

    # print(clock.get_fps())
