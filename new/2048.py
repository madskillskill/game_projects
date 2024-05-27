# %%
import pygame
from pygame.locals import *
pygame.init()
import random

# %%
screen_width = 400
screen_height = 440

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('2-0-4-8')

line_width = 12
clicked = False
pos = []

green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
gray = (200, 200, 200)

colors = {1:[0,0,0],
          2:[236, 111, 134],
          4:[254, 129, 109],
          8:[255, 186, 109],
          16:[255, 221, 117],
          32:[218, 255, 117],
          64:[178, 240, 104],
          128:[159, 243, 195],
          256:[106, 236, 244],
          512:[69, 180, 231],
          1024:[69, 115, 231],
          2048:[126, 105, 255],
          4096:[173, 97, 237],
          8192:[173, 167, 252],
          16384:[209, 135, 239],
          32768:[253, 166, 248],
          65536:[236, 111, 134],
          131072:[254, 129, 109],
          262144:[255, 186, 109],
          524288:[255, 221, 117],
          1048576:[218, 255, 117]
          }

game_over = False

counter = list(range(4))
counter_reverse = list(reversed(list(range(4))))

field = []
flags = []
score = 0
rand_gen = False
run = True
font = pygame.font.SysFont(None, 40)

again_rect = Rect(screen_width // 2 - 80, screen_height // 2, 160, 50)

bg = (205, 193, 180)
grid = (187, 173, 160)
screen.fill(bg)

# %%
# basic grid+field layout
def draw_grid():
    bg = (205, 193, 180)
    grid = (187, 173, 160)
    screen.fill(bg)
    pygame.draw.rect(screen, (187, 173, 160),  (0, 400, 400, 40))
    for x in range(1,4):
        pygame.draw.line(screen, grid, (0, x *100),
                         (screen_width, x * 100), line_width)
        pygame.draw.line(screen, grid, (x * 100, 0),
                         (x * 100, screen_height-20), line_width)
    pygame.draw.line(screen, grid, (0, 0),
                         (0, screen_height-40), 10)
    pygame.draw.line(screen, grid, (400, 0),
                         (400, screen_height-40), 10)
    pygame.draw.line(screen, grid, (0, 0),
                         (screen_width, 0), 10)
    pygame.draw.line(screen, grid, (0, 400),
                         (400, 400), 10)

# %%
def draw_full():
    full_text = 'The board is full!'
    full_img = font.render(full_text, True, blue)
    pygame.draw.rect(screen, green,  (screen_width // 2 - 100, screen_height // 2 - 60, 200, 50))
    screen.blit(full_img, (screen_width // 2 - 100, screen_height // 2 - 50))
    
    again_text = 'Play again?'
    again_img = font.render(again_text, True, blue)
    pygame.draw.rect(screen, green, again_rect)
    screen.blit(again_img, (screen_width // 2 - 80, screen_height // 2 + 10))

# %%
def no_moves_left():
    global field
    global counter
    sum = 1
    for x in field:
        for y in x:
            sum = sum * y
    # print('sum', sum)
    if sum == 0:
        return False
    
    if sum != 0:
        move_detected = False
        
        for x in counter[0:2]:
            for y in counter[0:2]:
                if field[x][y]==field[x+1][y] or field[x][y]==field[x][y+1]:
                    move_detected = True
        if move_detected == True:
            return False
                          
        if field[0][3] == field[1][3] or field[1][3] == field[2][3] or field[2][3] == field[3][3]:
            return False
                
        if field[3][0] == field[3][1] or field[3][1] == field[3][2] or field[3][2] == field[3][3]:
            return False
        
        else: return True

# %%
def empty_field():
    global field
    field = []
    for x in range(4):
        row = [0]*4
        field.append(row)

    starter = []
    start_works = True
    while start_works:
        for i in range(4):
            starter.append(random.randint(0, 3))
        point_1 = [starter[0], starter[1]]
        point_2 = [starter[2], starter[3]]
        if point_1 != point_2:
            n_1 = random.randint(0,9)
            n_2 = random.randint(0,9)
            
            if n_1 == 0:
                point_1.append(4)
            else: point_1.append(2)
            
            if n_2 == 0:
                point_2.append(4)
            else: point_2.append(2)
            
            start_works = False

    field[point_1[0]][point_1[1]] = point_1[2]
    field[point_2[0]][point_2[1]] = point_2[2]

# %%
def clear_flags():
    global flags
    flags = []
    for x in range(4):
        row = [0]*4
        flags.append(row)

# %%
empty_field()
clear_flags()

# %%
def draw_score():        
    score_text = 'SCORE:  ' + str(score)
    score_img = font.render(score_text, True, (0,0,0))
    score_img.set_alpha(180)
    screen.blit(score_img, (50, 410))

def update_score(new_sum):
    global score
    score += new_sum

# %%
last_tile = []
tile_combos = []

def draw_markers():
    global last_tile
    if last_tile != []:
        pygame.draw.rect(screen, (220,220,220),  (last_tile[0]*100-1, last_tile[1]*100-1, 102, 102))
        
    global tile_combos
    if tile_combos != []:
        for i in range(0,int(len(tile_combos)/2)):
            pygame.draw.rect(screen, (0,0,0), (tile_combos[i]*100-10, tile_combos[i+1]*100-10, 105, 105))
    tile_combos = []
    
    x_pos = 0
    for x in field:
        y_pos = 0
        for y in x:
            if y == 0:
                pass
            else:
                # color == 255/color
                color = colors[y]
                tile_img = font.render(str(y), True, (0,0,0))
                tile_img.set_alpha(180)
                pygame.draw.rect(screen, (color),  (x_pos*100+5, y_pos*100+5, 90, 90))
                screen.blit(tile_img, (x_pos*100 + 10, y_pos*100 + 10))
            y_pos += 1
        x_pos += 1

# %%
def place_new():
    global field
    global rand_gen
    global last_tile
    is_any_zero_tiles = False
    zero_tiles = []
    x_pos = 0
    for x in field:
        y_pos = 0
        for y in x:
            if y == 0:
                zero_tiles.append(x_pos)
                zero_tiles.append(y_pos)
                is_any_zero_tiles = True
            y_pos += 1
        x_pos += 1
    if is_any_zero_tiles == False:
        return 0
    elif is_any_zero_tiles == True:
        zero_count = len(zero_tiles)/2
        zero_winner = random.randint(0,zero_count-1)
        x = zero_tiles[zero_winner*2]
        y = zero_tiles[zero_winner*2+1]
        if field[x][y] == 0:
            n = random.randint(0,9)
            if n == 0:
                n = 4
            else: n = 2
            last_tile = [x,y,n]
            field[x][y] = n

# %%
def limit_check(pos, dir):
    if dir == 1:
        if pos > 0:
            return True
    elif dir == -1:
        if pos < 3:
            return True
    else: return False

# %%
def move_anim(movelist):
    if movelist == None or movelist == []:
        pass
    cycles = len(movelist)/4
    for cycle in range(cycles):
        i = cycle*4
        tile_1 = [movelist[0+i]][movelist[1+i]]
        tile_2 = [movelist[2+i]][movelist[3+i]]
        n = field[tile_1[0]][tile_1[1]]
        
        
        
        color = colors[n]
        tile_img = font.render(str(y), True, (0,0,0))
        tile_img.set_alpha(180)
        pygame.draw.rect(screen, (color),  (x_pos*100, y_pos*100, 100, 100))
        screen.blit(tile_img, (x_pos*100 + 10, y_pos*100 + 10))
    

# %%
def move_vert(dir):
    print('move_vert', dir)
    global rand_gen
    global field
    global flags
    
    if dir == -1:
        start_pos = 0
        count = counter_reverse
        end = 3
    else:
        start_pos = 3
        count = counter
        end = 0
    
    for i in range(0,8):
        x_pos = start_pos
        for column in counter:
            y_pos = start_pos
            for row in counter:
                if field[x_pos][y_pos] == 0:
                    if limit_check(y_pos, dir):
                        if field[x_pos][y_pos-dir] != 0:
                            field[x_pos][y_pos] = field[x_pos][y_pos-dir]
                            field[x_pos][y_pos-dir] = 0
                            rand_gen = True
                y_pos -= dir
            x_pos -= dir
    
    x_pos = start_pos
    for column in counter:
        y_pos = start_pos
        for row in count:
            if limit_check(y_pos, dir):
                if field[x_pos][y_pos] != 0:
                    if flags[x_pos][y_pos] == 0:
                        if field[x_pos][y_pos] == field[x_pos][y_pos-dir]:
                            field[x_pos][y_pos] = 2*field[x_pos][y_pos]
                            update_score(2*field[x_pos][y_pos])
                            field[x_pos][y_pos-dir] = 0
                            flags[x_pos][y_pos] = 1
                            tile_combos.append(x_pos)
                            tile_combos.append(y_pos)   
                            rand_gen = True
                                
                elif field[x_pos][y_pos] == 0 and field[x_pos][y_pos-dir] != 0:
                    field[x_pos][y_pos] = field[x_pos][y_pos-dir]
                    field[x_pos][y_pos-dir] = 0
                    rand_gen = True
            y_pos -= dir
        x_pos -= dir
           
    clear_flags() 
    if no_moves_left() == False:
        place_new()
    if no_moves_left() == True:
        pass

# %%
def move_horz(dir):
    print('move_horz', dir)
    global rand_gen
    global field
    global flags
    
    if dir == -1:
        start_pos = 0
        count = counter_reverse
        end = 3
    else:
        start_pos = 3
        count = counter
        end = 0
     
    for i in range(0,8):
        x_pos = start_pos
        for column in counter:
            y_pos = start_pos
            for row in counter:
                if field[x_pos][y_pos] == 0:
                    if limit_check(x_pos, dir):
                        if field[x_pos-dir][y_pos] != 0:
                            field[x_pos][y_pos] = field[x_pos-dir][y_pos]
                            field[x_pos-dir][y_pos] = 0
                            rand_gen = True
                y_pos -= dir
            x_pos -= dir
    
    x_pos = start_pos
    for column in counter:
        y_pos = start_pos
        for row in count:
            if limit_check(x_pos, dir):
                if field[x_pos][y_pos] != 0:
                    if flags[x_pos][y_pos] == 0:
                        if field[x_pos][y_pos] == field[x_pos-dir][y_pos]:
                            field[x_pos][y_pos] = 2*field[x_pos][y_pos]
                            update_score(2*field[x_pos][y_pos])
                            field[x_pos-dir][y_pos] = 0
                            flags[x_pos][y_pos] = 1
                            tile_combos.append(x_pos)
                            tile_combos.append(y_pos)   
                            rand_gen = True
                                
                elif field[x_pos][y_pos] == 0 and field[x_pos-dir][y_pos] != 0:
                    field[x_pos][y_pos] = field[x_pos-dir][y_pos]
                    field[x_pos-dir][y_pos] = 0
                    # flags[x_pos][y_pos] = 0
                    rand_gen = True
            y_pos -= dir
        x_pos -= dir
        
    clear_flags()
    if no_moves_left() == False:
        place_new()
    if no_moves_left() == True:
        pass

# %%
def refresh():
    draw_grid()
    draw_markers()
    draw_score()
    pygame.display.update()
refresh()

# %%
while run:
    # pygame.time.delay(100)
    refresh()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                move_horz(+1)

            if event.key == pygame.K_a or event.key == pygame.K_LEFT:    
                move_horz(-1)

            
            if event.key == pygame.K_w or event.key == pygame.K_UP:   
                move_vert(-1)

            
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:   
                move_vert(+1)

            if event.key == pygame.K_r:
                empty_field()
            
    

pygame.quit()


