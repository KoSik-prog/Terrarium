#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        display
#
# Author:      KoSik
#
# Created:     28.08.2022
# Copyright:   (c) kosik 2022
#-------------------------------------------------------------------------------
import sys ,os
import pygame, pygame.mixer, pygame.gfxdraw, glob
from pygame.locals import *
from pygame.compat import unichr_, unicode_
from pygame.locals import *
from pygame.compat import geterror

from libraries.log import *

pygame.init()

class display_CL:
    pygame.display.set_caption('Terrarium')
    resolution = 800, 480
    #screen = pygame.display.set_mode(resolution,FULLSCREEN)
    screen = pygame.display.set_mode(resolution, 1)
    
    def __init__(self):
        pygame.mouse.set_cursor((8,8), (0,0), (0,0,0,0,0,0,0,0), (0,0,0,0,0,0,0,0))

display = display_CL()