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

from lib.log import *

pygame.init()

class Display:
    pygame.display.set_caption('Terrarium')
    resolution = 800, 480
    #screen = pygame.display.set_mode(resolution,FULLSCREEN)
    screen = pygame.display.set_mode(resolution, 1)
    
    def __init__(self):
        pygame.mouse.set_cursor((8,8), (0,0), (0,0,0,0,0,0,0,0), (0,0,0,0,0,0,0,0))
        self.background = self.load_image("background.jpg")
        self.bulb1 = self.load_image("bulb1.gif")
        self.bulb2 = self.load_image("bulb2.gif")
        self.fan = self.load_image("fan.gif")
        self.dripper = self.load_image("dripper.gif")
        self.sprayer = self.load_image("sprayer.gif")

    def box(self, screen, x, y, w, h, colour):
        pygame.gfxdraw.box(screen, Rect((x,y),(w,h)), colour)

    def draw_rounded_rect(self, surface, rect, colour, cornerRadius):
        if rect.width < 2 * cornerRadius or rect.height < 2 * cornerRadius:
            raise ValueError("Both height (rect.height) and width (rect.width) must be > 2 * corner radius ({cornerRadius})")

        pygame.gfxdraw.aacircle(surface, rect.left+cornerRadius, rect.top+cornerRadius, cornerRadius, colour)
        pygame.gfxdraw.aacircle(surface, rect.right-cornerRadius-1, rect.top+cornerRadius, cornerRadius, colour)
        pygame.gfxdraw.aacircle(surface, rect.left+cornerRadius, rect.bottom-cornerRadius-1, cornerRadius, colour)
        pygame.gfxdraw.aacircle(surface, rect.right-cornerRadius-1, rect.bottom-cornerRadius-1, cornerRadius, colour)

        pygame.gfxdraw.filled_circle(surface, rect.left+cornerRadius, rect.top+cornerRadius, cornerRadius, colour)
        pygame.gfxdraw.filled_circle(surface, rect.right-cornerRadius-1, rect.top+cornerRadius, cornerRadius, colour)
        pygame.gfxdraw.filled_circle(surface, rect.left+cornerRadius, rect.bottom-cornerRadius-1, cornerRadius, colour)
        pygame.gfxdraw.filled_circle(surface, rect.right-cornerRadius-1, rect.bottom-cornerRadius-1, cornerRadius, colour)

        rect_tmp = pygame.Rect(rect)

        rect_tmp.width -= 2 * cornerRadius
        rect_tmp.center = rect.center
        pygame.draw.rect(surface, colour, rect_tmp)

        rect_tmp.width = rect.width
        rect_tmp.height -= 2 * cornerRadius
        rect_tmp.center = rect.center
        pygame.draw.rect(surface, colour, rect_tmp)

    def button(self, surface, rect, colour, borderColor, cornerRadius, borderThickness):
        if cornerRadius < 0:
            raise ValueError("border radius ({cornerRadius}) must be >= 0")

        rect_tmp = pygame.Rect(rect)
        center = rect_tmp.center

        if borderThickness:
            if cornerRadius <= 0:
                pygame.draw.rect(surface, borderColor, rect_tmp)
            else:
                self.draw_rounded_rect(surface, rect_tmp, borderColor, cornerRadius)

            rect_tmp.inflate_ip(-2*borderThickness, -2*borderThickness)
            inner_radius = cornerRadius - borderThickness + 1
        else:
            inner_radius = cornerRadius

        if inner_radius <= 0:
            pygame.draw.rect(surface, colour, rect_tmp)
        else:
            self.draw_rounded_rect(surface, rect_tmp, colour, inner_radius)

    def label(self, screen, text, font, size, x, y, colour, alpha):
        a_sys_font = pygame.font.SysFont(font, size)
        text = a_sys_font.render(text,True, colour)
        text.set_alpha(alpha)
        screen.blit(text, (x, y))
        return text.get_width()

    def label_center(self, screen, text, font, size, x, y, colour, alpha):
        a_sys_font = pygame.font.SysFont(font, size)
        text = a_sys_font.render(text,True, colour)
        text.set_alpha(alpha)
        screen.blit(text, (x-(text.get_width()/2), y))
        return text.get_width()

    def label_with_background(self, screen, text, font, size, x, y, colour, alpha, bgcolour):
        a_sys_font = pygame.font.SysFont(font, size)
        text = a_sys_font.render(text,True, colour)
        text.set_alpha(alpha)
        self.box(screen, x,y,text.get_width()+30,text.get_height(),bgcolour)
        screen.blit(text, (x, y))

    def load_image(self, name):
        main_dir = os.path.split(os.path.abspath(__file__))[0]
        data_dir = os.path.join(main_dir, '../assets/img')
        fullname = os.path.join(data_dir, name)
        try:
            image = pygame.image.load(fullname)
        except pygame.error:
            print ('Cannot load image:', fullname)
            raise SystemExit(str(geterror()))
        image = image.convert()
        return image

    def icons(self, osx ,osy, alpha, nazwa):
        if(nazwa == "background"):
            foto=self.background.convert()
        if(nazwa == "bulb1"):
            foto=self.bulb1.convert()
        if(nazwa == "bulb2"):
            foto=self.bulb2.convert()
        if(nazwa == "fan"):
            foto=self.fan.convert()
        if(nazwa == "dripper"):
            foto=self.dripper.convert()
        if(nazwa == "sprayer"):
            foto=self.sprayer.convert()
        foto.set_alpha(alpha)
        self.screen.blit(foto, (osx, osy))

display = Display()