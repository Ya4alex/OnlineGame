# -*- coding: utf-8 -*-
import pygame

# игровые параметры
FPS = 60
FPS2 = 30

# инициализация pygame и тд.
from conect import Server

server = Server()
g_params = server.init_connect()

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((500, 500))
infoObject = pygame.display.Info()
WIDTH = infoObject.current_w  # эти константы стали известны только после инициализации pygame
HEIGHT = infoObject.current_h

clock = pygame.time.Clock()

pygame.display.set_caption("Client")
pygame.mouse.set_visible(True)
font_name = pygame.font.match_font('arial')
