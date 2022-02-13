# -*- coding: utf-8 -*-
import math
from threading import Thread

import pygame
# игровые параметры
from pygame.rect import Rect

import conection

connections = conection.get_players(2)

# инициализация pygame и тд.
FPS = 60

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((500, 500))
infoObject = pygame.display.Info()
WIDTH = infoObject.current_w  # эти константы стали известны только после инициализации pygame
HEIGHT = infoObject.current_h

clock = pygame.time.Clock()

pygame.display.set_caption("Server")
pygame.mouse.set_visible(True)
font_name = pygame.font.match_font('arial')

TANK_SPEED = 4
BULLET_SPEED = 10
SHOOT_DELAY = 400
BULLET_DAMAGE = 34

BULLET_IMG = pygame.transform.scale(pygame.image.load('img/bullet.png').convert(), (8, 16))
BULLET_IMG.set_colorkey((0, 0, 0))


def draw_text(surf, text, size, x, y, color=(255, 255, 255)):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


last = 10


def gen_id(obj):
    global last
    last += 1
    all_sprites[last] = obj
    obj.id = last
    return last


a = {
    "self": {
        "pos": (55, 67),
        "rot": 0,
        "t_rot": 147,
    },
    "act": "shoot",
    "obj": {
        "cur": (300, 450),
        "par": {}
    }

}


def shoot(player, obj):
    pass


tool = {
    "shoot": shoot
}


def analyze(player):
    if not player.connection.data:
        return
    inf = player.connection.data.pop()
    player.update(*inf["self"]["pos"], inf["self"]["rot"], inf["self"]["t_rot"])
    f = tool.get(inf.get("act"))
    if f:
        f(**inf["obj"])


class Tank(pygame.sprite.Sprite):
    class Game:
        healf = 100
        damage = {}  # player : hp

        def __init__(self, id, name=None, color=None):
            self.id = id
            if not name:
                self.name = f"Player {id}"
            else:
                self.name = name

    def __init__(self, x, y, connection, *args):
        self.obj = "Player"
        self.id = connection.id
        self.connection = connection
        super().__init__()
        self.game = self.Game(*args)

        self.rect = Rect(0, 0, 64, 64)
        self.tower_rect = Rect(0, 0, 33, 66)

        self.x = self.rect.centerx = self.tower_rect.centerx = x
        self.y = self.rect.centery = self.tower_rect.centery = y

        self.speedx = 0
        self.speedy = 0

        self.angle = 0
        self.tower_angle = 0

        self.last_shot = 0

    def update(self, x, y, rot, t_rot):
        # if (x - self.x) ** 2 + (y - self.y) ** 2 <= TANK_SPEED ** 2 + 0.1:
        self.rect.centerx = self.x = x
        self.rect.centery = self.y = y

        self.angle = rot
        self.tower_angle = t_rot

    def wall(self):
        self.tower_rect.centerx = self.x = self.rect.centerx
        self.tower_rect.centery = self.y = self.rect.centery

    def catit(self):
        mx, my = pygame.mouse.get_pos()
        return mx - self.x, my - self.y

    def shoot(self):
        now = pygame.time.get_ticks()

        if now - self.last_shot > SHOOT_DELAY:
            self.last_shot = now
            angle = math.atan2(*self.catit())
            sx = BULLET_SPEED * math.sin(angle)
            sy = BULLET_SPEED * math.cos(angle)

            sin, cos = math.sin(math.radians(-self.tower_angle)), math.cos(math.radians(-self.tower_angle))
            r = self.rect.width / 2

            return Bullet(
                self.rect.centerx + r * cos,
                self.rect.centery + r * sin, sx, sy, self.tower_angle, self)

    def get_info(self):
        return {
            "pos": self.rect.center,
            "rot": self.angle,
            "t_rot": self.tower_angle,
            "act": ""
        }


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, sx, sy, rot, player, id=0):
        self.obj = "Bullet"
        self.id = id
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.rotate(BULLET_IMG, rot - 90)
        self.rect = self.image.get_rect()
        self.rect.centery = self.y = y
        self.rect.centerx = self.x = x
        self.speedy = sy
        self.speedx = sx
        self.rot = rot

        self.damage = BULLET_DAMAGE
        self.player = player

    def update(self):
        self.y += self.speedy
        self.x += self.speedx
        self.rect.centerx = self.x
        self.rect.centery = self.y
        if self.rect.bottom < 0 or self.rect.top > 850 or self.rect.right < 0 or self.rect.left > 1500:
            self.kill()  # суицид это плохо

    def get_info(self):
        return {
            "pos": self.rect.center,
            "rot": self.rot,
            "act": ""
        }


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, move=(0, 0), id=0):
        super().__init__()
        self.obj = "Wall"
        self.id = id
        self.image = pygame.Surface((w, h))
        self.image.fill(pygame.Color('sienna1'))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.move = move

    def update(self):
        self.rect.x += self.move[0]
        self.rect.y += self.move[1]

    def get_info(self):
        return {
            "pos": self.rect.topleft,
            "wh": (self.rect.width, self.rect.height)
        }


# игровые параметры

all_sprites = {}

bullets = pygame.sprite.Group()
walls = pygame.sprite.Group()
player_group = pygame.sprite.Group()

for w in (
        (0, 0, WIDTH, 20),
        (WIDTH - 20, 0, 20, HEIGHT),
        (0, HEIGHT - 20, WIDTH, 20),
        (0, 0, 20, HEIGHT),
        (100, 100, 20, 150),
        (100, 250, 150, 20),
        (100, 334, 150, 20),
        (250, 334, 20, 200),
        (300, 0, 200, 20, (0, 0)),
        (300, 800, 200, 20, (0, -1)),
        (800, 340, 20, 300, (0, 0)),
        (50, 340, 20, 300, (0, 0)),
):
    _ = Wall(*w)
    walls.add(_)
    gen_id(_)

a = ((200, 200), (400, 400), (550, 550), (700, 750))
for c in connections:
    _ = Tank(*a[c.id], c, c.id, )
    player_group.add(_)
    all_sprites[_.id] = _

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
    screen.fill((255, 255, 255))
    if paused:  # пауза
        pygame.display.flip()
        continue

    '''обновление спрайтов и обработка столкновений_____________________________________________'''
    _buf = []
    for player in player_group.sprites():
        _buf.append(Thread(target=player.connection.collect_data_break))
        _buf[-1].start()
    [_p.join() for _p in _buf]
    for player in player_group.sprites():
        analyze(player)

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
            elif index == 1:
                _tank.rect.left = _wall.rect.right
            elif index == 2:
                _tank.rect.bottom = _wall.rect.top
            elif index == 3:
                _tank.rect.right = _wall.rect.left

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
    stk = {}
    for id, sp in all_sprites.items():
        _ = sp.get_info()
        _["obj"] = sp.obj
        stk[id] = _
    _buf = []
    for player in player_group.sprites():
        _buf.append(Thread(target=player.connection.send_data, args=(stk,)))
        _buf[-1].start()
    [_p.join() for _p in _buf]
    '''отрисовка________________________________________________________________________________'''
    [pygame.draw.rect(screen, (0, 255, 255), _tank.rect) for _tank in player_group.sprites()]
    walls.draw(screen)
    bullets.draw(screen)
    draw_text(screen, f"{pygame.mouse.get_pos()}", 20, 40, 20, 'sienna1')
    draw_text(screen, "fps:" + str(int(clock.get_fps())), 20, WIDTH - 38, 20, 'sienna1')
    '''обновление переменных____________________________________________________________________'''
    pygame.display.flip()

pygame.quit()
