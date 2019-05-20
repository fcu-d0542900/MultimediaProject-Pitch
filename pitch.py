# -*- coding: utf-8 -*-
"""
Created on Mon May 20 13:07:58 2019

@author: YURU
"""
from threading import Thread
import pygame
import Buttons
import InputBox
import voiceControl as VC

vc = VC.voiceControl()

pygame.init()
pygame.display.set_caption("Pitch.py")
screenWidth, screenHeight = 288, 512
screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()

running = True
first = True

titleFont = pygame.font.Font("NotoSansCJKtc-Bold.otf", 34)
titleText = titleFont.render("唱出想要的音~", True, (225, 77, 241))
noteFont = pygame.font.Font("NotoSansMono-ExtraBold.ttf", 55)

t = Thread(target = vc.getCurrentNote)
t.daemon = True
t.start()

mode = 0

centTolerance = 20 
Button1 = Buttons.Button()
Button2 = Buttons.Button()
InputBox1 = InputBox.InputBox(44, 100, 140, 32)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            running = False
        if mode == 2:
            InputBox1.handle_event(event)
    if first == True:
        Button1.create_button(screen, (218,112,214), 44, 150, 200, 70,  0, "隨意模式", (255,255,255),30)
        Button2.create_button(screen, (3,168,153), 44, 250, 200, 70,  0, "特定模式", (255,255,255),30)
        if event.type == pygame.locals.MOUSEBUTTONDOWN :
            if Button1.pressed(pygame.mouse.get_pos()):
                mode = 1
                print("Button1!")
            if Button2.pressed(pygame.mouse.get_pos()):
                print("Button2!")
                mode = 2
            first = False
    else:
        if mode == 1:
            screen.fill((0, 0, 0))
            # 畫線
            pygame.draw.line(screen, (255, 255, 255), (10, 290), (10, 310))
            pygame.draw.line(screen, (255, 255, 255), (screenWidth - 10, 290), (screenWidth - 10, 310))
            pygame.draw.line(screen, (255, 255, 255), (10, 300), (screenWidth - 10, 300))
            screen.blit(titleText, (10,  80))
            if not vc.q.empty():
                b = vc.q.get()
                if b['Cents'] < 15:  #音分
                    pygame.draw.circle(screen, (0, 255, 0), (screenWidth // 2 + (int(b['Cents']) * 2),300), 5)
                else:
                    pygame.draw.circle(screen, (255, 0, 0), (screenWidth // 2 + (int(b['Cents']) * 2), 300), 5)
                noteText = noteFont.render(b['Note'], True, (240, 76, 133))
                screen.blit(noteText, (50, 400))
                
        elif mode == 2:
            screen.fill((255, 255, 255))
            InputBox1.draw(screen)
            InputBox1.update()
            if InputBox1.text != '':
                print('-->'+InputBox1.text)
            pygame.draw.line(screen, (255, 255, 255), (10, 290), (10, 310))
            pygame.draw.line(screen, (255, 255, 255), (screenWidth - 10, 290), (screenWidth - 10, 310))
            pygame.draw.line(screen, (255, 255, 255), (10, 300), (screenWidth - 10, 300))
            if not vc.q.empty():
                b = vc.q.get()
                if b['Cents'] < 15:  #音分
                    pygame.draw.circle(screen, (0, 255, 0), (screenWidth // 2 + (int(b['Cents']) * 2),300), 5)
                else:
                    pygame.draw.circle(screen, (255, 0, 0), (screenWidth // 2 + (int(b['Cents']) * 2), 300), 5)
                noteText = noteFont.render(b['Note'], True, (240, 76, 133))
                screen.blit(noteText, (50, 400))
    
        
    pygame.display.flip()
    clock.tick(30)

vc.end = True
pygame.quit()
