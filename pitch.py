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
import music21

vc = VC.voiceControl()

pygame.init()
pygame.display.set_caption("Pitch.py")
screenWidth, screenHeight = 288, 512
screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()

running = True

titleFont = pygame.font.Font("NotoSansCJKtc-Bold.otf", 34)
textFont = pygame.font.Font("NotoSansMono-ExtraBold.ttf", 30)
noteFont = pygame.font.Font("NotoSansMono-ExtraBold.ttf", 55)

t = Thread(target = vc.getCurrentNote)
t.daemon = True
t.start()

mode = 0
want_pitch=''
centTolerance = 20 
Button1 = Buttons.Button()
Button2 = Buttons.Button()
InputBox1 = InputBox.InputBox(44, 150, 140, 32)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            if event.key == pygame.K_BACKSPACE and mode!=0:
                mode = 0
                continue
        if mode == 2:
            InputBox1.handle_event(event)
    if mode == 0:
        screen.fill((0, 0, 0))
        Button1.create_button(screen, (218,112,214), 44, 150, 200, 70,  0, "隨意模式", (255,255,255),30)
        Button2.create_button(screen, (3,168,153), 44, 250, 200, 70,  0, "特定模式", (255,255,255),30)
        if event.type == pygame.locals.MOUSEBUTTONDOWN :
            if Button1.pressed(pygame.mouse.get_pos()):
                mode = 1
                print("Button1!")
            if Button2.pressed(pygame.mouse.get_pos()):
                print("Button2!")
                mode = 2
    else:
        if mode == 1:
            screen.fill((0, 0, 0))
            # 畫線
            pygame.draw.line(screen, (255, 255, 255), (10, 290), (10, 310))
            pygame.draw.line(screen, (255, 255, 255), (screenWidth - 10, 290), (screenWidth - 10, 310))
            pygame.draw.line(screen, (255, 255, 255), (10, 300), (screenWidth - 10, 300))
            titleText = titleFont.render("唱出想辨識的音~", True, (225, 77, 241))
            screen.blit(titleText, (10,  80))
            if not vc.q.empty():
                b = vc.q.get()
                if b['Cents'] < 15:  #音分
                    pygame.draw.circle(screen, (0, 255, 0), (screenWidth // 2 + (int(b['Cents']) * 2),300), 5)
                else:
                    pygame.draw.circle(screen, (255, 0, 0), (screenWidth // 2 + (int(b['Cents']) * 2),300), 5)
                noteText = noteFont.render(b['Note'], True, (240, 76, 133))
                screen.blit(noteText, (50, 400))
                
        elif mode == 2:
            screen.fill((255, 255, 255))
            InputBox1.draw(screen)
            InputBox1.update()
            if InputBox1.gettext != '':
                print('-->'+InputBox1.gettext)
                want_pitch = music21.pitch.Pitch(InputBox1.gettext)
                InputBox1.gettext=''
            titleText = titleFont.render("輸入想要的音名~", True, (225, 77, 241))
            screen.blit(titleText, (10,  80))
            if not (vc.q.empty() or want_pitch==''):
                b = vc.q.get()
                if b['Pitch'].nameWithOctave == want_pitch.nameWithOctave and b['Cents'] < 25:
                    text = textFont.render('Correct!', True, (240, 76, 133))
                else:
                    if b['Pitch'].frequency > want_pitch.frequency:
                        text = textFont.render('Too High!', True, (240, 76, 133))
                    else:
                        text = textFont.render('Too Low!', True, (240, 76, 133))
                screen.blit(text, (50, 300))
                noteText = noteFont.render(b['Note'], True, (240, 76, 133))
                screen.blit(noteText, (50, 400))
    
        
    pygame.display.flip()
    clock.tick(30)

vc.end = True
pygame.quit()
