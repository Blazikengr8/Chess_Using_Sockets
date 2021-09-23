'''
This file is a part of My-PyChess application.
In this file, we manage the online menu which is called when user clicks
online button on main menu.
'''

import pygame
from ext.pyBox import TextBox
from tools.loader import ONLINEMENU, BACK, FONT
from tools.utils import rounded_rect

# This shows the screen
def showScreen(win, sel):
    win.fill((0, 0, 0))
    
    rounded_rect(win, (255, 255, 255), (120, 10, 260, 70), 20, 4)
    rounded_rect(win, (255, 255, 255), (20, 90, 460, 400), 14, 4)
    win.blit(ONLINEMENU.HEAD, (175, 15))
    win.blit(BACK, (460, 0))
    
    for cnt, i in enumerate(ONLINEMENU.TEXT):
        win.blit(i, (40, 100 + cnt*18))
    
    rounded_rect(win, (255, 255, 255), (150, 230, 110, 30), 10, 3)
    win.blit(ONLINEMENU.CONNECT, (150, 230))
    
    rounded_rect(win, (255, 255, 255), (300, 350, 110, 30), 10, 3)
    win.blit(ONLINEMENU.CONNECT, (300, 350))
    
    pygame.draw.rect(win, (255, 255, 255), (130 + sel*160, 460, 40, 20), 3)
    
    
# This is the main function, called from main menu
def main(win):
    clock = pygame.time.Clock()
    sel = 0
    
    box = TextBox(FONT, (0, 0, 0), (65, 350, 200, 35))
    while True:
        clock.tick(24)
        showScreen(win, sel)

        pygame.draw.rect(win, (255, 255, 255), (63, 348, 204, 39))
        box.draw(win)
            
        for event in pygame.event.get():
            box.push(event)
                
            if event.type == pygame.QUIT:
                return 0
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 460 < x < 500 and 0 < y < 50:
                    return 1
                
                if 460 < y < 480:
                    if 130 < x < 170:
                        sel = 0
                    
                    if 290 < x < 320:
                        sel = 1
                
                if 150 < x < 260 and 230 < y < 260:
                    return "my-pychess.tk", True
                
                if 300 < x < 410 and 350 < y < 380:
                    return box.text, bool(sel)      
        pygame.display.update()
