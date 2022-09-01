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

class display_CL:
    pygame.display.set_caption('Terrarium')
    resolution = 800, 480
    #screen = pygame.display.set_mode(resolution,FULLSCREEN)
    screen = pygame.display.set_mode(resolution, 1)
    
    def __init__(self):
        pygame.mouse.set_cursor((8,8), (0,0), (0,0,0,0,0,0,0,0), (0,0,0,0,0,0,0,0))
        self.background = self.load_image("tlo.jpg")
        self.bulb1 = self.load_image("zarowka1.gif")
        self.bulb2 = self.load_image("zarowka2.gif")
        self.fan = self.load_image("fan.gif")
        self.dripper = self.load_image("dripper.gif")
        self.sprayer = self.load_image("sprysk.gif")

    def box(self, screen, x, y, w, h, color):
        pygame.gfxdraw.box(screen, Rect((x,y),(w,h)), color)

    def draw_rounded_rect(self, surface, rect, color, corner_radius):
        if rect.width < 2 * corner_radius or rect.height < 2 * corner_radius:
            raise ValueError("Both height (rect.height) and width (rect.width) must be > 2 * corner radius ({corner_radius})")

        pygame.gfxdraw.aacircle(surface, rect.left+corner_radius, rect.top+corner_radius, corner_radius, color)
        pygame.gfxdraw.aacircle(surface, rect.right-corner_radius-1, rect.top+corner_radius, corner_radius, color)
        pygame.gfxdraw.aacircle(surface, rect.left+corner_radius, rect.bottom-corner_radius-1, corner_radius, color)
        pygame.gfxdraw.aacircle(surface, rect.right-corner_radius-1, rect.bottom-corner_radius-1, corner_radius, color)

        pygame.gfxdraw.filled_circle(surface, rect.left+corner_radius, rect.top+corner_radius, corner_radius, color)
        pygame.gfxdraw.filled_circle(surface, rect.right-corner_radius-1, rect.top+corner_radius, corner_radius, color)
        pygame.gfxdraw.filled_circle(surface, rect.left+corner_radius, rect.bottom-corner_radius-1, corner_radius, color)
        pygame.gfxdraw.filled_circle(surface, rect.right-corner_radius-1, rect.bottom-corner_radius-1, corner_radius, color)

        rect_tmp = pygame.Rect(rect)

        rect_tmp.width -= 2 * corner_radius
        rect_tmp.center = rect.center
        pygame.draw.rect(surface, color, rect_tmp)

        rect_tmp.width = rect.width
        rect_tmp.height -= 2 * corner_radius
        rect_tmp.center = rect.center
        pygame.draw.rect(surface, color, rect_tmp)

    def button(self, surface, rect, color, border_color, corner_radius, border_thickness):
        if corner_radius < 0:
            raise ValueError("border radius ({corner_radius}) must be >= 0")

        rect_tmp = pygame.Rect(rect)
        center = rect_tmp.center

        if border_thickness:
            if corner_radius <= 0:
                pygame.draw.rect(surface, border_color, rect_tmp)
            else:
                self.draw_rounded_rect(surface, rect_tmp, border_color, corner_radius)

            rect_tmp.inflate_ip(-2*border_thickness, -2*border_thickness)
            inner_radius = corner_radius - border_thickness + 1
        else:
            inner_radius = corner_radius

        if inner_radius <= 0:
            pygame.draw.rect(surface, color, rect_tmp)
        else:
            self.draw_rounded_rect(surface, rect_tmp, color, inner_radius)

    def label(self, screen, tekst, font, rozmiar, x, y, color, alpha):
        a_sys_font = pygame.font.SysFont(font, rozmiar)
        text = a_sys_font.render(tekst,True, color)
        text.set_alpha(alpha)
        screen.blit(text, (x, y))
        return text.get_width()

    def label_center(self, screen, tekst, font, rozmiar, x, y, color, alpha):
        a_sys_font = pygame.font.SysFont(font, rozmiar)
        text = a_sys_font.render(tekst,True, color)
        text.set_alpha(alpha)
        screen.blit(text, (x-(text.get_width()/2), y))
        return text.get_width()

    def label_with_background(self, screen, tekst, font, rozmiar, x, y, color, alpha, bgcolor):
        a_sys_font = pygame.font.SysFont(font, rozmiar)
        text = a_sys_font.render(tekst,True, color)
        text.set_alpha(alpha)
        self.box(screen, x,y,text.get_width()+30,text.get_height(),bgcolor)
        screen.blit(text, (x, y))

    def load_image(self, name):   # ZALADOWANIE IKONY
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

display = display_CL()