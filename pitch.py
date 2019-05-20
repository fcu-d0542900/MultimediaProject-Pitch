# -*- coding: utf-8 -*-
"""
Created on Mon May 20 13:07:58 2019

@author: YURU
"""
from threading import Thread
import pygame
from voiceControl import q, getCurrentNote

pygame.init()
screenWidth, screenHeight = 288, 512
screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()

running = True

titleFont = pygame.font.Font("NotoSansMono-ExtraBold.ttf", 34)
titleText = titleFont.render("Sing ", True, (225, 77, 241))
titleCurr = titleFont.render("Your Note", True, (225, 77, 241))

noteFont = pygame.font.Font("NotoSansMono-ExtraBold.ttf", 55)

t = Thread(target=getCurrentNote)
t.daemon = True
t.start()

centTolerance = 20 

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            running = False
    screen.fill((0, 0, 0))
    # 畫線
    pygame.draw.line(screen, (255, 255, 255), (10, 290), (10, 310))
    pygame.draw.line(screen, (255, 255, 255), (screenWidth - 10, 290), (screenWidth - 10, 310))
    pygame.draw.line(screen, (255, 255, 255), (10, 300), (screenWidth - 10, 300))

    if not q.empty():
        b = q.get()
        if b['Cents'] < 15:  #音分
            pygame.draw.circle(screen, (0, 255, 0), (screenWidth // 2 + (int(b['Cents']) * 2),300), 5)
        else:
            pygame.draw.circle(screen, (255, 0, 0), (screenWidth // 2 + (int(b['Cents']) * 2), 300), 5)
        noteText = noteFont.render(b['Note'], True, (240, 76, 133))
        screen.blit(noteText, (50, 400))

    screen.blit(titleText, (10,  80))
    screen.blit(titleCurr, (10, 120))
    pygame.display.flip()
    clock.tick(30)

pygame.quit()