# -*- coding: utf-8 -*-
import pygame

# игровые параметры
FPS = 60
FPS2 = 30

# инициализация pygame и тд.
from conect import Server

server = Server()

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1500, 850))
infoObject = pygame.display.Info()
WIDTH = infoObject.current_w  # эти константы стали известны только после инициализации pygame
HEIGHT = infoObject.current_h

clock = pygame.time.Clock()

pygame.display.set_caption("TanKs xuy")
pygame.mouse.set_visible(True)
font_name = pygame.font.match_font('arial')
