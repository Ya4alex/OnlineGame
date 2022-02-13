# -*- coding: utf-8 -*-
from threading import Thread

from entities import Tank, create_tool
from main import pygame, screen, WIDTH, clock, font_name, FPS, g_params, server


# игровые параметры
def gen_id(obj):
    global last
    last += 1
    all_sprites[last] = obj
    obj.id = last
    return last


def draw_text(surf, text, size, x, y, color=(255, 255, 255)):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


'''Выгрузка всех картинок:----------------------------------------------------------------------'''
'''Выгрузка музыки и звуков:--------------------------------------------------------------------'''
'''Переменные игрового цикла:----------------------------------------------------------------   '''
all_sprites = {}

bullets = pygame.sprite.Group()
walls = pygame.sprite.Group()
player_group = pygame.sprite.Group()

player = Tank(g_params["id"])
player_group.add(player)
all_sprites[player.id] = player

game_over = True
running = True
paused = False

'''игровой цикл---------------------------------------------------------------------------------'''
while running:
    if game_over:
        pass

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE:
                paused = not paused
                pygame.mouse.set_visible(paused)
    mous_state = pygame.mouse.get_pressed()
    if mous_state[0] and False:
        b = player.shoot()
        if b:
            bullets.add(b)

    screen.fill((255, 255, 255))
    if paused:  # пауза
        continue

    '''обновление спрайтов и обработка столкновений_____________________________________________'''
    player.self_update()
    hits = pygame.sprite.spritecollide(player, walls, False)
    for _wall in hits:
        r = (_wall.rect.bottom - player.rect.top, _wall.rect.right - player.rect.left,
             _wall.rect.top - player.rect.bottom, _wall.rect.left - player.rect.right,)

        index, val = min(enumerate(r), key=lambda x: abs(x[1]))
        if index == 0:
            player.rect.top = _wall.rect.bottom
        elif index == 1:
            player.rect.left = _wall.rect.right
        elif index == 2:
            player.rect.bottom = _wall.rect.top
        elif index == 3:
            player.rect.right = _wall.rect.left
        player.x, player.y = player.rect.center

    Thread(target=server.send_data, args=(player.get_info(),)).start()
    target = server.get_data()
    for id, spr_data in server.get_data_res.items():
        if int(id) == player.id:
            continue
        spr = all_sprites.get(int(id))
        if spr:
            spr.update(spr_data)
        else:
            spr = create_tool[spr_data["obj"]](int(id), spr_data)
            all_sprites[int(id)] = spr
            if spr.obj == "Wall":
                walls.add(spr)

    '''отрисовка________________________________________________________________________________'''
    # player_group.draw(screen)
    [pygame.draw.rect(screen, (0, 255, 255), _tank.rect, 1) for _tank in player_group.sprites()]

    for spr in all_sprites.values():
        if spr.obj == "Player":
            spr.draw_tower(screen)
        else:
            screen.blit(spr.image, spr.rect)
    draw_text(screen, f"{pygame.mouse.get_pos()}", 20, 80, 20, 'sienna1')
    draw_text(screen, "fps:" + str(int(clock.get_fps())), 20, WIDTH - 38, 20, 'sienna1')
    '''обновление переменных____________________________________________________________________'''
    pygame.display.flip()

pygame.quit()
