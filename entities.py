import math

from main import pygame

TANK_SPEED = 4
BULLET_SPEED = 10
SHOOT_DELAY = 300
BULLET_DAMAGE = 34

BULLET_IMG = pygame.transform.scale(pygame.image.load('img/bullet.png').convert(), (8, 16))
BULLET_IMG.set_colorkey((0, 0, 0))

int_0 = lambda x: x if x > 0 else 0


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

    class Animation:
        shoot_d = 0

        def shoot(self, pow):
            self.shoot_d = pow

        def update(self):
            self.shoot_d = int_0(self.shoot_d - 1)

    def __init__(self, *args):
        super().__init__()
        self.game = self.Game(*args)
        _image = pygame.transform.scale(pygame.image.load('img/car.png').convert(), (64, 64))
        _image.set_colorkey((0, 0, 0))
        self.image = self.orig_image = _image
        self.rect = self.image.get_rect()
        self.rect.centerx = 55
        self.rect.centery = 55

        _image = pygame.transform.scale(pygame.image.load('img/tower.png').convert(), (33, 66))
        _image.set_colorkey((0, 0, 0))
        self.tower_image = self.orig_tower_image = _image
        self.tower_rect = self.tower_image.get_rect()
        self.tower_rect.centerx = 55
        self.tower_rect.centery = 55

        self.speedx = 0
        self.speedy = 0

        self.angle = 0
        self.tower_angle = 0

        self.x = self.rect.centerx
        self.y = self.rect.centery

        self.last_shot = 0

        self.animation = self.Animation()

    def update(self):
        keystate = pygame.key.get_pressed()

        self.speedx = int(keystate[pygame.K_d]) * TANK_SPEED + int(keystate[pygame.K_a]) * -TANK_SPEED
        self.speedy = int(keystate[pygame.K_w]) * -TANK_SPEED + int(keystate[pygame.K_s]) * TANK_SPEED

        if self.speedy and self.speedx:
            self.speedx *= 0.7071067811865476
            self.speedy *= 0.7071067811865476

        self.x += self.speedx
        self.y += self.speedy
        self.angle = (180 / math.pi) * -math.atan2(self.speedy, self.speedx)
        self.tower_angle = (180 / math.pi) * math.atan2(*self.catit()) - 90

        self.rotate()

        self.rect.centerx = self.tower_rect.centerx = self.x
        self.rect.centery = self.tower_rect.centery = self.y
        self.tower_rect.center = (
            self.tower_rect.centerx - math.cos(math.radians(-self.tower_angle)) * self.animation.shoot_d,
            self.tower_rect.centery - math.sin(math.radians(-self.tower_angle)) * self.animation.shoot_d
        )

        self.animation.update()

    def rotate(self, deg=False):
        if deg is not False:
            pass
        if self.speedy != 0 or self.speedx != 0:
            self.image = pygame.transform.rotate(self.orig_image, self.angle - 90)

        self.tower_image = pygame.transform.rotate(self.orig_tower_image, self.tower_angle - 90)
        self.tower_rect = self.tower_image.get_rect(center=self.rect.center)

    def wall(self, deg):
        self.tower_rect.centerx = self.x = self.rect.centerx
        self.tower_rect.centery = self.y = self.rect.centery
        self.rotate(deg)

    def catit(self):
        mx, my = pygame.mouse.get_pos()
        return mx - self.x, my - self.y

    def draw_tower(self, surface):
        surface.blit(self.image,
                     (self.rect.x - (self.image.get_width() - self.rect.width) / 2,
                      self.rect.y - (self.image.get_height() - self.rect.height) / 2))
        surface.blit(self.tower_image, self.tower_rect)

    def shoot(self):
        now = pygame.time.get_ticks()

        if now - self.last_shot > SHOOT_DELAY:
            self.last_shot = now
            angle = math.atan2(*self.catit())
            sx = BULLET_SPEED * math.sin(angle)
            sy = BULLET_SPEED * math.cos(angle)

            sin, cos = math.sin(math.radians(-self.tower_angle)), math.cos(math.radians(-self.tower_angle))
            r = self.rect.width / 2

            self.animation.shoot(10)

            return Bullet(
                self.rect.centerx + r * cos,
                self.rect.centery + r * sin, sx, sy, self.tower_angle, self)


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, move=(0, 0)):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(pygame.Color('sienna1'))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.move = move

    def update(self):
        self.rect.x += self.move[0]
        self.rect.y += self.move[1]


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, sx, sy, rot, player):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.rotate(BULLET_IMG, rot - 90)
        self.rect = self.image.get_rect()
        self.rect.centery = self.y = y
        self.rect.centerx = self.x = x
        self.speedy = sy
        self.speedx = sx

        self.damage = BULLET_DAMAGE
        self.player = player

    def update(self):
        self.y += self.speedy
        self.x += self.speedx
        self.rect.centerx = self.x
        self.rect.centery = self.y
        if self.rect.bottom < 0 or self.rect.top > 850 or self.rect.right < 0 or self.rect.left > 1500:
            self.kill()  # суицид это плохо
