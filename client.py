# -*- coding: utf-8 -*-
from main import pygame, screen, WIDTH, clock, font_name, FPS


# игровые параметры


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
    if mous_state[0]:
        b = tank.shoot()
        if b:
            bullets.add(b)

    screen.fill((255, 255, 255))
    if paused:  # пауза
        continue

    '''обновление спрайтов и обработка столкновений_____________________________________________'''
    player_group.update()
    walls.update()
    bullets.update()

    hits = pygame.sprite.groupcollide(player_group, walls, False, False)
    for _tank, _walls in hits.items():
        for _wall in _walls:
            r = (_wall.rect.bottom - _tank.rect.top, _wall.rect.right - _tank.rect.left,
                 _wall.rect.top - _tank.rect.bottom, _wall.rect.left - _tank.rect.right,)

            index, val = min(enumerate(r), key=lambda x: abs(x[1]))

            if index == 0:
                _tank.rect.top = _wall.rect.bottom
                _tank.wall(0)
            elif index == 1:
                _tank.rect.left = _wall.rect.right
                _tank.wall(90)
            elif index == 2:
                _tank.rect.bottom = _wall.rect.top
                _tank.wall(180)
            elif index == 3:
                _tank.rect.right = _wall.rect.left
                _tank.wall(270)

    hits = pygame.sprite.groupcollide(player_group, bullets, False, False)
    for _tank, _bullets in hits.items():
        for _bullet in _bullets:
            if _bullet.player != _tank:
                _tank.game.healf -= _bullet.damage
                _r = _bullet.player.game.damage.get(_tank.game.id)
                if _r:
                    _bullet.player.game.damage[_tank.game.id] += 34
                else:
                    _bullet.player.game.damage[_tank.game.id] = 34
                print("headshot")

    hits = pygame.sprite.groupcollide(bullets, walls, False, False)
    for _bullet, _walls in hits.items():
        for _wall in _walls:
            r = (_wall.rect.bottom - _bullet.rect.top, _wall.rect.right - _bullet.rect.left,
                 _wall.rect.top - _bullet.rect.bottom, _wall.rect.left - _bullet.rect.right,)

            index, val = min(enumerate(r), key=lambda x: abs(x[1]))

            if index == 0:
                _bullet.rect.top = _wall.rect.bottom
                _bullet.speedy = -_bullet.speedy
            elif index == 1:
                _bullet.rect.left = _wall.rect.right
                _bullet.speedx = -_bullet.speedx
            elif index == 2:
                _bullet.rect.bottom = _wall.rect.top
                _bullet.speedy = -_bullet.speedy
            elif index == 3:
                _bullet.rect.right = _wall.rect.left
                _bullet.speedx = -_bullet.speedx

    '''отрисовка________________________________________________________________________________'''
    # player_group.draw(screen)
    [_tank.draw_tower(screen) for _tank in player_group.sprites()]
    walls.draw(screen)
    bullets.draw(screen)
    draw_text(screen, f"{pygame.mouse.get_pos()}", 20, 80, 20, 'sienna1')
    draw_text(screen, "fps:" + str(int(clock.get_fps())), 20, WIDTH - 38, 20, 'sienna1')
    '''обновление переменных____________________________________________________________________'''
    pygame.display.flip()

pygame.quit()
