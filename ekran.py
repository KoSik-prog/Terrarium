# -*- coding: utf-8 -*-
try:
    import select, time, datetime
except ImportError:
    print ("Blad importu")

import sys ,os
import pygame, pygame.mixer, pygame.gfxdraw, glob
from pygame.locals import *
from pygame.compat import unichr_, unicode_
from pygame.locals import *
from pygame.compat import geterror
from time import sleep

pygame.init()
resolution = 800,480
screen = pygame.display.set_mode(resolution,FULLSCREEN)

def box(screen, x,y,w,h,color):
    pygame.gfxdraw.box(screen, Rect((x,y),(w,h)), color)

def draw_rounded_rect(surface, rect, color, corner_radius):
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

def przycisk(surface, rect, color, border_color, corner_radius, border_thickness):
    if corner_radius < 0:
        raise ValueError("border radius ({corner_radius}) must be >= 0")

    rect_tmp = pygame.Rect(rect)
    center = rect_tmp.center

    if border_thickness:
        if corner_radius <= 0:
            pygame.draw.rect(surface, border_color, rect_tmp)
        else:
            draw_rounded_rect(surface, rect_tmp, border_color, corner_radius)

        rect_tmp.inflate_ip(-2*border_thickness, -2*border_thickness)
        inner_radius = corner_radius - border_thickness + 1
    else:
        inner_radius = corner_radius

    if inner_radius <= 0:
        pygame.draw.rect(surface, color, rect_tmp)
    else:
        draw_rounded_rect(surface, rect_tmp, color, inner_radius)

def napis(screen, tekst, font, rozmiar, x, y, color, alpha):
    a_sys_font = pygame.font.SysFont(font, rozmiar)
    text = a_sys_font.render(tekst,True, color)
    text.set_alpha(alpha)
    screen.blit(text, (x, y))
    return text.get_width()

def napis_centralny(screen, tekst, font, rozmiar, x, y, color, alpha):
    a_sys_font = pygame.font.SysFont(font, rozmiar)
    text = a_sys_font.render(tekst,True, color)
    text.set_alpha(alpha)
    screen.blit(text, (x-(text.get_width()/2), y))
    return text.get_width()

def napis_tlo(screen, tekst, font, rozmiar, x, y, color, alpha,bgcolor):
    a_sys_font = pygame.font.SysFont(font, rozmiar)
    text = a_sys_font.render(tekst,True, color)
    text.set_alpha(alpha)
    box(screen, x,y,text.get_width()+30,text.get_height(),bgcolor)
    screen.blit(text, (x, y))

def load_image(name):   # ZALADOWANIE IKONY
    main_dir = os.path.split(os.path.abspath(__file__))[0]
    data_dir = os.path.join(main_dir, 'pic')
    fullname = os.path.join(data_dir, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print ('Cannot load image:', fullname)
        raise SystemExit(str(geterror()))
    image = image.convert()
    return image

def icons(osx ,osy, alpha, nazwa):
    if(nazwa == "tlo"):
        foto=ikona.Tlo.convert()
    if(nazwa == "zarowka1"):
        foto=ikona.zarowka1.convert()
    if(nazwa == "zarowka2"):
        foto=ikona.zarowka2.convert()
    if(nazwa == "wentylator"):
        foto=ikona.wentylator.convert()
    if(nazwa == "dripper"):
        foto=ikona.dripper.convert()
    if(nazwa == "spryskiwacz"):
        foto=ikona.sprysk.convert()
    foto.set_alpha(alpha)
    screen.blit(foto, (osx, osy))

class Ikony(object):
    def __init__(self):
        self.Tlo = load_image("tlo.jpg")
        self.zarowka1 = load_image("zarowka1.gif")
        self.zarowka2 = load_image("zarowka2.gif")
        self.wentylator = load_image("fan.gif")
        self.dripper = load_image("dripper.gif")
        self.sprysk = load_image("sprysk.gif")
ikona = Ikony()