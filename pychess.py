"""
This file is the main file of My-PyChess application.
Run this file to launch the program.

In this file, we handle the main menu which gets displayed at runtime.
"""
import sys  
import pygame

import chess
import menus
from tools.loader import MAIN
from tools import sound

# This is a non-important bit of code. Flush stdout - useful incase external
# programs are calling this application.
sys.stdout.flush()

# Some initialisation
pygame.init()
clock = pygame.time.Clock()

# Initialise display, set the caption and icon. Use SCALED if on pygame 2.
if pygame.version.vernum[0] >= 2:
    win = pygame.display.set_mode((500, 500), pygame.SCALED)
else:
    win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Chessly")
pygame.display.set_icon(MAIN.ICON)

# Coordinates of buttons in rectangle notation.
onln = (200, 200, 120, 40)
pref = (200, 240, 120, 40)
abt =  (200, 280, 120, 40)

# This is the function that displays the main screen.
# "prefs" value is passed, prefs is a list of all the user settings
def showMain(prefs):
    # cnt and image are two global variables, cnt is an integer that is
    # incremented in every frame, when cnt reaches 210, it is setback to zero.
    # img variable denotes the image that is displayed on the screen
    # it can have a value from 0 to 3 (both inclusive)
    global cnt, img

    # First, blit background image (based on the img variable)
    win.blit(MAIN.BG[img], (0, 0))

    # Then we check wether user has enabled background animate feature
    if prefs["slideshow"]:
        # Background animations is a feature that shows a slideshow of images
        # in the background, slow fading of screen is also seen.
        # To achieve this, a frame counter variable "cnt" is incremented
        # every frame. The intended framerate of the game is 30 fps, so
        # after seven seconds, the frame counter reaches 210 after which,
        # it needs to be reset to zero.
        cnt += 1
        if cnt >= 150:
            # If the counter has reached a value of 150 (means 5 seconds have
            # elapsed), then start to slowly fade the image.
            # This is achieved by blitting a surface onto the screen
            # whose transparancy keeps reducing as each frame goes
            s = pygame.Surface((500, 500))
            s.set_alpha((cnt - 150) * 4)
            s.fill((0, 0, 0))
            win.blit(s, (0, 0))

        if cnt == 210:
            cnt = 0
            img = 0 if img == 3 else img + 1
    else:
        # User has disabled screen animations, reset the variables
        cnt = -150
        img = 0

    # Now blit all the texts onto the screen one by one
    win.blit(MAIN.HEADING, (80, 20))
    pygame.draw.line(win, (255, 255, 255), (80, 100), (130, 100), 4)
    pygame.draw.line(win, (255, 255, 255), (165, 100), (340, 100), 4)
    win.blit(MAIN.VERSION, (345, 95))

    win.blit(MAIN.ONLINE, onln[:2])
    win.blit(MAIN.PREF, pref[:2])
    win.blit(MAIN.ABOUT, abt[:2])

# Initialize a few more variables
cnt = 0
img = 0
run = True

# Load the settings of the player
prefs = menus.pref.load()

music = sound.Music()
music.play(prefs)
while run:
    # Start the game loop at 30fps, show the screen every time at first
    clock.tick(30)
    showMain(prefs)

    # We need to get the position of the mouse so that we can blit an image
    # on the text over which the mouse hovers
    x, y = pygame.mouse.get_pos()
    if onln[0] < x < sum(onln[::2]) and onln[1] < y < sum(onln[1::2]):
        win.blit(MAIN.ONLINE_H, onln[:2])
    if pref[0] < x < sum(pref[::2]) and pref[1] < y < sum(pref[1::2]):
        win.blit(MAIN.PREF_H, pref[:2])
    if abt[0] < x < sum(abt[::2]) and abt[1] < y < sum(abt[1::2]):
        win.blit(MAIN.ABOUT_H, abt[:2])
    # Begin pygame event loop to catch all events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # User has clicked somewhere, determine which button and
            # call a function to handle the game into a different window.
            x, y = event.pos

            if onln[0] < x < sum(onln[::2]) and onln[1] < y < sum(onln[1::2]):
                sound.play_click(prefs)
                ret = menus.onlinemenu(win)
                if ret == 0:
                    run = False
                elif ret != 1:
                    run = chess.online(win, ret[0], prefs, ret[1])
            elif pref[0] < x < sum(pref[::2]) and pref[1] < y < sum(pref[1::2]):
                sound.play_click(prefs)
                run = menus.prefmenu(win)
                
                prefs = menus.pref.load()
                if music.is_playing():
                    if not prefs["sounds"]:
                        music.stop()
                else:
                    music.play(prefs)
            elif abt[0] < x < sum(abt[::2]) and abt[1] < y < sum(abt[1::2]):
                sound.play_click(prefs)
                run = menus.aboutmenu(win)

    # Update the screen every frame
    pygame.display.flip()

# Stop music, quit pygame after the loop is done
music.stop()
pygame.quit()
