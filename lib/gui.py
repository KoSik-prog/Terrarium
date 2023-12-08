#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        GUI
#
# Author:      KoSik
#
# Created:     28.08.2022
# Copyright:   (c) kosik 2022
# -------------------------------------------------------------------------------
try:
    import datetime
    from lib.log import *
    from lib.mainLight import *
    from lib.sensors import *
    from lib.heater import *
    from lib.sprayer import *
    from lib.display import *
    from lib.settings import *
    from lib.fogger import *
    from terrarium import *
except ImportError:
    print("Import error - gui")


class Gui:
    bgcolor = (0, 0, 0, 255)
    activeTab = 0
    touchPointList = []
    menuTimeStamp = None  # menu display time stamp
    menuTime = 30  # how long menu is displayed
    settingsSavedFlag = False
    timeFormat = '%H:%M:%S.%f'

    def __init__(self):
        display.screen.fill(self.bgcolor)
        self.menuTimeStamp = datetime.datetime.now()

    def gui_thread(self):
        tfps = 0.5

        while terrarium.runFlag == True:
            self.touchPointList.clear()
            if (self.activeTab == 0):
                self.main_tab()
            elif (self.activeTab == 1):
                self.menu_main_tab()
            elif (self.activeTab == 2):
                self.menu_sprayer_tab()
            elif (self.activeTab == 3):
                self.menu_terrarium_tab()
            elif (self.activeTab == 4):
                self.menu_lighting_tab()
            elif (self.activeTab == 5):
                self.menu_climate_tab()
            time.sleep(tfps)
            # when idle then return to the home screen
            if ((datetime.datetime.now() - self.menuTimeStamp) > (datetime.timedelta(seconds=self.menuTime))):
                self.activeTab = 0
                if self.settingsSavedFlag == False:
                    settings.save_settings()
                    self.settingsSavedFlag = True

    def touch_thread(self):
        while terrarium.runFlag == True:
            self.touch_event()
            time.sleep(0.01)

    def main_tab(self):
        iconsPosition = 5
        display.icons(0, 0, 255, "background")

        if (gpio.mainLightFlag == True):
            display.icons(10, iconsPosition, 255, "bulb1")
            iconsPosition += 125

        if (gpio.check_heater_flag() == True):
            display.icons(10, iconsPosition, 255, "bulb2")
            dl = display.label_center(display.screen, "{}%".format(gpio.get_heater_pwm(
            )), "Nimbus Sans L", 48, 70, iconsPosition + 65, (235, 0, 69), 255)
            iconsPosition += 125

        if (gpio.check_sprayer_flag() == True):
            display.icons(10, iconsPosition, 255, "sprayer")
            iconsPosition += 125

        dl = display.label(display.screen, "{:.1f}°C".format(
            terrarium.temperatureTop), "Nimbus Sans L", 150, 290, 10, (247, 130, 59), 255)  # (241, 198, 228)
        # display.label(display.screen, "{:.0f}%".format(
        #     terrarium.humidityTop), "Nimbus Sans L", 80, 320+dl, 50, (183, 176, 241), 255)

        dl = display.label(display.screen, "{:.1f}°C".format(
            terrarium.temperatureBottom), "Nimbus Sans L", 150, 290, 370, (110, 254, 192), 255)  # (206, 241, 198)
        display.label(display.screen, "{:.0f}%".format(
            terrarium.humidityBottom), "Nimbus Sans L", 80, 320+dl, 410, (183, 176, 241), 255)

        # display.label(display.screen, "UVI:{:.4f}".format(
        #     terrarium.uvi), "Nimbus Sans L", 70, 430, 180, (253, 201, 77), 255)
        # display.label(display.screen, "UVA: {:.2f} UVB: {:.2f}".format(
        #     terrarium.uva, terrarium.uvb), "Nimbus Sans L", 48, 370, 240, (254, 138, 35), 255)

        display.label(display.screen, "{}".format(datetime.datetime.now().strftime(
            '%H:%M:%S')), "Nimbus Sans L", 60, 30, 420, (200, 240, 200), 255)

        self.touchPointList.append(((0, 0, 400, 480), "menuTab"))
        self.touchPointList.append(((630, 0, 800, 150), "exit"))
        pygame.display.update()

    def menu_main_tab(self):
        end = timer()

        display.icons(0, 0, 255, "background")
        self.touchPointList.append(display.button_with_text("sprayerTab", display.screen, (
            30, 60, 300, 120), (223, 169, 191), (223, 169, 151), 10, 2, "rain", 80, (253, 50, 35)))
        # self.touchPointList.append(display.button_with_text("climateTab", display.screen, (
        #     30, 220, 300, 120), (216, 155, 43), (216, 155, 0), 10, 2, "climate", 80, (253, 50, 35)))
        self.touchPointList.append(display.button_with_text("terrariumTab", display.screen, (
            360, 60, 300, 120), (187, 179, 41), (187, 179, 0), 10, 2, "terrarium", 75, (253, 50, 35)))
        self.touchPointList.append(display.button_with_text("lightingTab", display.screen, (
            360, 220, 300, 120), (213, 0, 88), (213, 0, 38), 10, 2, "light", 75, (253, 50, 35)))
        display.label(display.screen, "runtime:{}".format(str(datetime.timedelta(seconds=round(
            end - terrarium.startTime)))), "Nimbus Sans L", 30, 50, 440, (150, 150, 150), 100)
        self.touchPointList.append(display.button_with_text("back", display.screen, (
            690, 390, 100, 80), (120, 120, 120), (15, 15, 15), 10, 2, "<", 120, (0, 0, 0)))
        pygame.display.update()

    def menu_sprayer_tab(self):
        end = timer()
        display.icons(0, 0, 255, "background")
        buttonMinColour = (180, 180, 180)
        buttonMinBorderColour = (200, 200, 200)

        display.label(display.screen, "Timer 1", "Nimbus Sans L", 60, 30, 40, (253, 180, 165), 255)
        self.touchPointList.append(display.button_with_text("SprayTimer1_H-", display.screen, (200, 60, 80, 50), buttonMinColour, buttonMinBorderColour, 10, 2, "-", 90, (15, 15, 15)))
        self.touchPointList.append(display.button_with_text( "SprayTimer1_H+", display.screen, (200, 10, 80, 50), (80, 80, 80), (50, 50, 50), 10, 2, "+", 80, (220, 220, 220)))
        display.button_with_text("-", display.screen,  (285, 10, 100, 100), (55, 112, 21), (55, 112, 21), 10, 2, "{:02d}".format( sprayer.spraying1.hour), 120, (220, 220, 220))
        display.label(display.screen, ":", "Nimbus Sans L", 120, 382, 15, (220, 220, 220), 255)
        display.button_with_text("-", display.screen,  (400, 10, 100, 100), (55, 112, 21), (55, 112, 21), 10, 2, "{:02d}".format(sprayer.spraying1.minute), 120, (220, 220, 220))
        self.touchPointList.append(display.button_with_text("SprayTimer1_M-", display.screen, (505, 60, 80, 50), buttonMinColour, buttonMinBorderColour, 10, 2, "-", 90, (15, 15, 15)))
        self.touchPointList.append(display.button_with_text("SprayTimer1_M+", display.screen, (505, 10, 80, 50), (80, 80, 80), (50, 50, 50), 10, 2, "+", 80, (220, 220, 220)))

        display.label(display.screen, "Timer 2", "Nimbus Sans L", 60, 30, 170, (253, 180, 165), 255)
        self.touchPointList.append(display.button_with_text("SprayTimer2_H-", display.screen, (200, 190, 80, 50), buttonMinColour, buttonMinBorderColour, 10, 2, "-", 90, (15, 15, 15)))
        self.touchPointList.append(display.button_with_text("SprayTimer2_H+", display.screen, (200, 140, 80, 50), (80, 80, 80), (50, 50, 50), 10, 2, "+", 80, (220, 220, 220)))
        display.button_with_text("-", display.screen,  (285, 140, 100, 100), (55, 112, 21), (55, 112, 21), 10, 2, "{:02d}".format(sprayer.spraying2.hour), 120, (220, 220, 220))
        display.label(display.screen, ":", "Nimbus Sans L", 120, 382, 145, (220, 220, 220), 255)
        display.button_with_text("-", display.screen, (400, 140, 100, 100), (55, 112, 21), (55, 112, 21), 10, 2, "{:02d}".format(sprayer.spraying2.minute), 120, (220, 220, 220))
        self.touchPointList.append(display.button_with_text("SprayTimer2_M-", display.screen, (505, 190, 80, 50), buttonMinColour, buttonMinBorderColour, 10, 2, "-", 90, (15, 15, 15)))
        self.touchPointList.append(display.button_with_text("SprayTimer2_M+", display.screen, (505, 140, 80, 50), (80, 80, 80), (50, 50, 50), 10, 2, "+", 80, (220, 220, 220)))

        display.label(display.screen, "Spray time", "Nimbus Sans L", 60, 30, 290, (253, 180, 165), 255)
        self.touchPointList.append(display.button_with_text("SprayTime_-", display.screen, (420, 270, 80, 80), buttonMinColour, buttonMinBorderColour, 10, 2, "-", 110, (15, 15, 15)))
        display.button_with_text("-", display.screen, (505, 270, 200, 80), (55, 112, 21), (55, 112, 21), 10, 2, "{} s".format(sprayer.sprayingTime), 80, (220, 220, 220))
        self.touchPointList.append(display.button_with_text("SprayTime_+", display.screen, (710, 270, 80, 80), (80, 80, 80), (50, 50, 50), 10, 2, "+", 80, (220, 220, 220)))
        
        display.label(display.screen, "Manually", "Nimbus Sans L", 60, 30, 410, (253, 180, 165), 255)
        self.touchPointList.append(display.button_with_text("SprayTimeManual_-", display.screen, (240, 430, 80, 50), buttonMinColour, buttonMinBorderColour, 10, 2, "-", 90, (15, 15, 15)))
        self.touchPointList.append(display.button_with_text("SprayTimeManual_+", display.screen, (240, 380, 80, 50), (80, 80, 80), (50, 50, 50), 10, 2, "+", 80, (220, 220, 220)))
        display.button_with_text("-", display.screen, (325, 380, 200, 100), (55, 112, 21), (55, 112, 21), 10, 2, "{} s".format(sprayer.sprayingTimeManual), 80, (220, 220, 220))
        self.touchPointList.append(display.button_with_text("SprayManual", display.screen, (530, 380, 80, 100), (199, 134, 51), buttonMinBorderColour, 10, 2, "", 90, (15, 15, 15)))

        display.button(display.screen, (600, 10, 190, 230), (47, 79, 79), (40, 72, 72), 10, 2)
        display.label_center(display.screen, "last spray:", "Nimbus Sans L", 40, 700, 45, (253, 201, 77), 255)
        display.label_center(display.screen, "{}".format(str(datetime.timedelta(seconds=round(end - sprayer.lastSpraying)))), "Nimbus Sans L", 40, 700, 75, (253, 201, 77), 255)
        display.label_center(display.screen, "sprays today:", "Nimbus Sans L", 40, 700, 175, (253, 201, 77), 255)
        display.label_center(display.screen, "{}".format(sprayer.get_spray_counter()), "Nimbus Sans L", 40, 700, 205, (253, 201, 77), 255)

        self.touchPointList.append(display.button_with_text("back", display.screen, (690, 390, 100, 80), (120, 120, 120), (15, 15, 15), 10, 2, "<", 120, (0, 0, 0)))
        pygame.display.update()

    def menu_terrarium_tab(self):
        display.icons(0, 0, 255, "background")

        myTop = 20
        display.label_center(display.screen, "Min humidity ", "Nimbus Sans L", 48, 210, myTop+40, (253, 180, 165), 255)
        self.touchPointList.append(display.button_with_text("MinHumidity_-", display.screen, (410, myTop, 80, 80), (200, 200, 200), (250, 250, 250), 10, 2, "-", 110, (15, 15, 15)))
        display.button(display.screen, (495, myTop, 200, 80), (55, 112, 21), (55, 112, 21), 10, 2)
        display.label_center(display.screen, "{} %".format(terrarium.minimumHumidity), "Nimbus Sans L", 80, 595, myTop+40, (220, 220, 220), 255)
        self.touchPointList.append(display.button_with_text("MinHumidity_+", display.screen, (700, myTop, 80, 80), (200, 200, 200), (250, 250, 250), 10, 2, "+", 80, (15, 15, 15)))

        myTop += 110
        display.label_center(display.screen, "Temp on island", "Nimbus Sans L", 47, 210, myTop+40, (253, 180, 165), 255)
        self.touchPointList.append(display.button_with_text("ReqTemperatureIsland_-", display.screen,  (410, myTop, 80, 80), (200, 200, 200), (250, 250, 250), 10, 2, "-", 110, (15, 15, 15)))
        display.button(display.screen, (495, myTop, 200, 80), (55, 112, 21), (55, 112, 21), 10, 2)
        display.label_center(display.screen, "{}°C".format(terrarium.temperatureRequiredIsland), "Nimbus Sans L", 80, 595, myTop+40, (220, 220, 220), 255)
        self.touchPointList.append(display.button_with_text("ReqTemperatureIsland_+", display.screen, (700, myTop, 80, 80), (200, 200, 200), (250, 250, 250), 10, 2, "+", 80, (15, 15, 15)))

        myTop += 110
        display.label_center(display.screen, "minimal UVI", "Nimbus Sans L", 48, 210, myTop+23, (253, 180, 165), 255)
        display.label_center(display.screen, "for heating ", "Nimbus Sans L", 50, 220, myTop+60, (253, 180, 165), 255)
        self.touchPointList.append(display.button_with_text("minUviForHeating_-", display.screen, (410, myTop, 80, 80), (200, 200, 200), (250, 250, 250), 10, 2, "-", 110, (15, 15, 15)))
        display.button(display.screen, (495, myTop, 200, 80), (55, 112, 21), (55, 112, 21), 10, 2)
        display.label_center(display.screen, "{:.2f}".format(terrarium.minUviForHeating), "Nimbus Sans L", 80, 595, myTop+40, (220, 220, 220), 255)
        self.touchPointList.append(display.button_with_text("minUviForHeating_+", display.screen,  (700, myTop, 80, 80), (200, 200, 200), (250, 250, 250), 10, 2, "+", 80, (15, 15, 15)))

        self.touchPointList.append(display.button_with_text("backToMain", display.screen, (690, 390, 100, 80), (120, 120, 120), (15, 15, 15), 10, 2, "<", 120, (0, 0, 0)))
        pygame.display.update()
        
    def menu_lighting_tab(self):
        buttonMinColour = (180, 180, 180)
        buttonMinBorderColour = (200, 200, 200)
        display.icons(0, 0, 255, "background")

        display.label_center(display.screen, "Main Light", "Nimbus Sans L", 80, 400, 35, (253, 180, 165), 255)
        xPos = 5
        yPos = 75
        self.touchPointList.append(display.button_with_text("MainLightTimer1_H-", display.screen, (xPos, yPos+50, 80, 50), buttonMinColour, buttonMinBorderColour, 10, 2, "-", 90, (15, 15, 15)))
        self.touchPointList.append(display.button_with_text( "MainLightTimer1_H+", display.screen, (xPos, yPos, 80, 50), (80, 80, 80), (50, 50, 50), 10, 2, "+", 80, (220, 220, 220)))
        display.button_with_text("-", display.screen,  (xPos+85, yPos, 100, 100), (55, 112, 21), (55, 112, 21), 10, 2, "{:02d}".format(mainLight.get_timer(0, True)), 120, (220, 220, 220))
        display.label(display.screen, ":", "Nimbus Sans L", 120, xPos+182, yPos+5, (220, 220, 220), 255)
        display.button_with_text("-", display.screen,  (xPos+200, yPos, 100, 100), (55, 112, 21), (55, 112, 21), 10, 2, "{:02d}".format(mainLight.get_timer(0, False)), 120, (220, 220, 220))
        self.touchPointList.append(display.button_with_text("MainLightTimer1_M-", display.screen, (xPos+305, yPos+50, 80, 50), buttonMinColour, buttonMinBorderColour, 10, 2, "-", 90, (15, 15, 15)))
        self.touchPointList.append(display.button_with_text("MainLightTimer1_M+", display.screen, (xPos+305, yPos, 80, 50), (80, 80, 80), (50, 50, 50), 10, 2, "+", 80, (220, 220, 220)))
        xPos = 410
        yPos = 75
        self.touchPointList.append(display.button_with_text("MainLightTimer2_H-", display.screen, (xPos, yPos+50, 80, 50), buttonMinColour, buttonMinBorderColour, 10, 2, "-", 90, (15, 15, 15)))
        self.touchPointList.append(display.button_with_text( "MainLightTimer2_H+", display.screen, (xPos, yPos, 80, 50), (80, 80, 80), (50, 50, 50), 10, 2, "+", 80, (220, 220, 220)))
        display.button_with_text("-", display.screen,  (xPos+85, yPos, 100, 100), (55, 112, 21), (55, 112, 21), 10, 2, "{:02d}".format(mainLight.get_timer(1, True)), 120, (220, 220, 220))
        display.label(display.screen, ":", "Nimbus Sans L", 120, xPos+182, yPos+5, (220, 220, 220), 255)
        display.button_with_text("-", display.screen,  (xPos+200, yPos, 100, 100), (55, 112, 21), (55, 112, 21), 10, 2, "{:02d}".format(mainLight.get_timer(1, False)), 120, (220, 220, 220))
        self.touchPointList.append(display.button_with_text("MainLightTimer2_M-", display.screen, (xPos+305, yPos+50, 80, 50), buttonMinColour, buttonMinBorderColour, 10, 2, "-", 90, (15, 15, 15)))
        self.touchPointList.append(display.button_with_text("MainLightTimer2_M+", display.screen, (xPos+305, yPos, 80, 50), (80, 80, 80), (50, 50, 50), 10, 2, "+", 80, (220, 220, 220)))
        yPos = 145
        btnWidth = 200
        self.touchPointList.append(display.button_with_text("MainLightOff", display.screen, (180-(btnWidth/2), yPos+50, btnWidth, 70), (199, 51, 75), buttonMinBorderColour, 10, 2, "Off", 90, (15, 15, 15)))
        self.touchPointList.append(display.button_with_text("MainLightAuto", display.screen, (400-(btnWidth/2), yPos+50, btnWidth, 70), (199, 134, 51), buttonMinBorderColour, 10, 2, "Auto", 90, (15, 15, 15)))
        self.touchPointList.append(display.button_with_text("MainLightOn", display.screen, (620-(btnWidth/2), yPos+50, btnWidth, 70), (81, 142, 21), buttonMinBorderColour, 10, 2, "On", 90, (15, 15, 15)))
        xPos = 50
        yPos = 390
        display.label(display.screen, "Heater", "Nimbus Sans L", 80, 160, 320, (253, 180, 165), 255)
        self.touchPointList.append(display.button_with_text("HeaterPwmAuto", display.screen, (xPos-20, yPos, 150, 80), (199, 134, 51), buttonMinBorderColour, 10, 2, "Auto", 90, (15, 15, 15)))
        self.touchPointList.append(display.button_with_text("HeaterPwm_-", display.screen, (xPos+140, yPos, 80, 80), buttonMinColour, buttonMinBorderColour, 10, 2, "-", 110, (15, 15, 15)))
        display.button_with_text("-", display.screen, (xPos+225, yPos, 200, 80), (55, 112, 21), (55, 112, 21), 10, 2, "{}%".format(gpio.get_heater_pwm()), 80, (220, 220, 220))
        self.touchPointList.append(display.button_with_text("HeaterPwm_+", display.screen, (xPos+430, yPos, 80, 80), (80, 80, 80), (50, 50, 50), 10, 2, "+", 80, (220, 220, 220)))
        
        self.touchPointList.append(display.button_with_text("backToMain", display.screen, (690, 390, 100, 80), (120, 120, 120), (15, 15, 15), 10, 2, "<", 120, (0, 0, 0)))
        pygame.display.update()
        
    def menu_climate_tab(self):
        buttonMinColour = (180, 180, 180)
        buttonMinBorderColour = (200, 200, 200)
        display.icons(0, 0, 255, "background")

        display.label_center(display.screen, "Fog", "Nimbus Sans L", 80, 400, 45, (253, 180, 165), 255)
        yPos = 60
        btnWidth = 200
        self.touchPointList.append(display.button_with_text("FoggerOff", display.screen, (180-(btnWidth/2), yPos+50, btnWidth, 70), (199, 51, 75), buttonMinBorderColour, 10, 2, "Off", 90, (15, 15, 15)))
        self.touchPointList.append(display.button_with_text("FoggerAuto", display.screen, (400-(btnWidth/2), yPos+50, btnWidth, 70), (199, 134, 51), buttonMinBorderColour, 10, 2, "Auto", 90, (15, 15, 15)))
        self.touchPointList.append(display.button_with_text("FoggerOn", display.screen, (620-(btnWidth/2), yPos+50, btnWidth, 70), (81, 142, 21), buttonMinBorderColour, 10, 2, "On", 90, (15, 15, 15)))
        
        self.touchPointList.append(display.button_with_text("backToMain", display.screen, (690, 390, 100, 80), (120, 120, 120), (15, 15, 15), 10, 2, "<", 120, (0, 0, 0)))
        pygame.display.update()

    def click_event(self, name):
        if name == "menuTab":
            self.activeTab = 1
        elif name == "sprayerTab":
            self.activeTab = 2
            self.settingsSavedFlag = False
        elif name == "terrariumTab":
            self.activeTab = 3
            self.settingsSavedFlag = False
        elif name == "lightingTab":
            self.activeTab = 4
            self.settingsSavedFlag = False
        elif name == "climateTab":
            self.activeTab = 5
            self.settingsSavedFlag = False
        elif name == "SprayTimer1_H-":
            sprayer.spraying1 = self.change_time(sprayer.spraying1, -1, 0)
        elif name == "SprayTimer1_H+":
            sprayer.spraying1 = self.change_time(sprayer.spraying1, 1, 0)
        elif name == "SprayTimer1_M-":
            sprayer.spraying1 = self.change_time(sprayer.spraying1, 0, -1)
        elif name == "SprayTimer1_M+":
            sprayer.spraying1 = self.change_time(sprayer.spraying1, 0, 1)
        elif name == "SprayTimer2_H-":
            sprayer.spraying2 = self.change_time(sprayer.spraying2, -1, 0)
        elif name == "SprayTimer2_H+":
            sprayer.spraying2 = self.change_time(sprayer.spraying2, 1, 0)
        elif name == "SprayTimer2_M-":
            sprayer.spraying2 = self.change_time(sprayer.spraying2, 0, -1)
        elif name == "SprayTimer2_M+":
            sprayer.spraying2 = self.change_time(sprayer.spraying2, 0, 1)
        elif name == "SprayTime_-":
            if sprayer.sprayingTime > 0:
                sprayer.sprayingTime -= 1
            else:
                sprayer.sprayingTime = 99
        elif name == "SprayTime_+":
            if sprayer.sprayingTime < 99:
                sprayer.sprayingTime += 1
            else:
                sprayer.sprayingTime = 0
        elif name == "SprayTimeManual_-":
            if sprayer.sprayingTimeManual > 0:
                sprayer.sprayingTimeManual -= 1
            else:
                sprayer.sprayingTimeManual = 99
        elif name == "SprayTimeManual_+":
            if sprayer.sprayingTimeManual < 99:
                sprayer.sprayingTimeManual += 1
            else:
                sprayer.sprayingTimeManual = 0
        elif name == "SprayManual":
            sprayer.spray_terrarium(sprayer.get_spraying_time_manual()) 
        elif name == "MinHumidity_-":
            if terrarium.minimumHumidity > 0:
                terrarium.minimumHumidity -= 1
            else:
                terrarium.minimumHumidity = 99
        elif name == "MinHumidity_+":
            if terrarium.minimumHumidity < 99:
                terrarium.minimumHumidity += 1
            else:
                terrarium.minimumHumidity = 0
        elif name == "ReqTemperatureIsland_-":
            if terrarium.temperatureRequiredIsland > 0:
                terrarium.temperatureRequiredIsland -= 1
            else:
                terrarium.temperatureRequiredIsland = 99
            heater.update_pid_target()
        elif name == "ReqTemperatureIsland_+":
            if terrarium.temperatureRequiredIsland < 99:
                terrarium.temperatureRequiredIsland += 1
            else:
                terrarium.temperatureRequiredIsland = 0
            heater.update_pid_target()
        elif name == "minUviForHeating_-":
            if terrarium.minUviForHeating > 0:
                terrarium.minUviForHeating -= 0.01
            else:
                terrarium.minUviForHeating = 1.0
        elif name == "minUviForHeating_+":
            if terrarium.minUviForHeating < 1:
                terrarium.minUviForHeating += 0.01
            else:
                terrarium.minUviForHeating = 0
        elif name == "MainLightTimer1_H-":
            self.change_time_mainLight(0, -1, 0)
        elif name == "MainLightTimer1_H+": 
            self.change_time_mainLight(0, +1, 0)
        elif name == "MainLightTimer1_M-": 
            self.change_time_mainLight(0, 0, -1)
        elif name == "MainLightTimer1_M+": 
            self.change_time_mainLight(0, 0, +1)
        elif name == "MainLightTimer2_H-":
            self.change_time_mainLight(1, -1, 0)
        elif name == "MainLightTimer2_H+":
            self.change_time_mainLight(1, +1, 0)
        elif name == "MainLightTimer2_M-": 
            self.change_time_mainLight(1, 0, -1)
        elif name == "MainLightTimer2_M+": 
            self.change_time_mainLight(1, 0, +1)
        elif name == "MainLightOff": 
            mainLight.set_manual_control_flag(True)
            mainLight.turn_light_off()
        elif name == "MainLightOn": 
            mainLight.set_manual_control_flag(True)
            mainLight.turn_light_on()
        elif name == "MainLightAuto": 
            mainLight.set_manual_control_flag(False)
            self.activeTab = 0
        elif name == "HeaterPwm_-": 
            heater.set_manual_control_flag(True)
            heater.set_heat_control_flag(False)
            if(gpio.get_heater_pwm() > 5):
                gpio.set_heater_pwm(gpio.get_heater_pwm() - 5)
            else:
                gpio.set_heater_pwm(0)
        elif name == "HeaterPwm_+": 
            heater.set_manual_control_flag(True)
            heater.set_heat_control_flag(False)
            if(gpio.get_heater_pwm() < 95):
                gpio.set_heater_pwm(gpio.get_heater_pwm() + 5)
            else:
                gpio.set_heater_pwm(100)
        elif name == "HeaterPwmAuto": 
            heater.heat_control_stop() 
            gpio.set_heater_pwm(0)
            heater.set_manual_control_flag(False) 
            self.activeTab = 0      
        elif name == "FoggerOn": 
            fogger.fog_on()
        elif name == "FoggerOff": 
            fogger.fog_off()   
        elif name == "FoggerAuto": 
            fogger.fog_auto_run()
        elif name == "back":
            if self.activeTab > 0:
                self.activeTab -= 1
        elif name == "backToMain":
            if self.activeTab > 0:
                self.activeTab = 0
        elif name == "exit":
            terrarium.runFlag = False
            time.sleep(1)
            pygame.quit()
            sys.exit()
        else:
            print("button: {} not found".format(name))

    def touch_event(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                click_event("exit")
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                px = event.pos[0]
                py = event.pos[1]
                self.menuTimeStamp = datetime.datetime.now()
                for point in self.touchPointList:
                    click = point[0]
                    clickX = click[0]
                    clickY = click[1]
                    clickWidth = click[2]
                    clickHeight = click[3]
                    if (px > clickX and px < (clickX + clickWidth) and py > clickY and py < (clickY + clickHeight)):
                        self.click_event(point[1])
                        pygame.event.clear

    def change_time(self, time, hours, minutes):
        newHour = time.hour + hours
        if newHour < 0:
            newHour += 24
        if newHour > 23:
            newHour -= 24
        newMinutes = time.minute + minutes
        if newMinutes < 0:
            newMinutes += 60
        if newMinutes > 59:
            newMinutes -= 60
        return datetime.time(newHour, newMinutes)
    
    def change_time_mainLight(self, timerNr, hours, minutes):
        convTime = datetime.time(mainLight.get_timer(timerNr, True), mainLight.get_timer(timerNr, False))
        myTime = self.change_time(convTime, hours, minutes)
        mainLight.set_timer(timerNr, myTime.strftime(self.timeFormat))

gui = Gui()