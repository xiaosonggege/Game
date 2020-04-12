#!/usr/bin/env python
# encoding: utf-8
'''
@author: songyunlong
@license: (C) Copyright 2020-2025.
@contact: 1243049371@qq.com
@software: pycharm
@file: pygameex
@time: 2020/3/16 4:33 下午
'''
import pygame
from pygame.locals import QUIT
import sys
def ex1():
    background_image_filename = '/Users/songyunlong/Desktop/bear.jpeg'
    mouse_cursor = '/Users/songyunlong/Desktop/b.jpeg'

    pygame.init()
    screen = pygame.display.set_mode((1280, 1000), 0, 32)
    pygame.display.set_caption('hello world')
    background = pygame.image.load(background_image_filename)
    mouse_cursor = pygame.image.load(mouse_cursor)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        screen.blit(background, (0, 0))
        x, y = pygame.mouse.get_pos()
        x -= mouse_cursor.get_width() / 2
        y -= mouse_cursor.get_height() / 2

        screen.blit(mouse_cursor, (x, y))

        pygame.display.update()

def run_game():
    pygame.init()
    screen = pygame.display.set_mode(size=(1200, 800))
    bg_color = (100, 100, 100)
    screen.fill(bg_color)
    while True:
        pygame.display.set_caption("Alien Invasion")
        # mouse_x, mouse_y = pygame.mouse.get_pos()
        # print(mouse_x, mouse_y)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_BACKSPACE]:
            print('DELETE')

        pygame.display.flip()


if __name__ == '__main__':
    # ex1()
    run_game()
