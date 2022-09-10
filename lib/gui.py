#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        GUI
#
# Author:      KoSik
#
# Created:     28.08.2022
# Copyright:   (c) kosik 2022
#-------------------------------------------------------------------------------
try:
    from lib.log import *
    from lib.mainLight import *
    from lib.sensors import *
    from lib.heater import *
    from lib.sprayer import *
    from lib.display import *
    from lib.settings import *
    from terrarium import *
except ImportError:
    print("Import error - gui")

class Gui:
    bgcolor=(0, 0, 0, 255)
    activeTab = 0
    touchPointList = []
    menuTimeStamp = None #menu display time stamp
    menuTime = 30 #how long menu is displayed
    settingsSavedFlag = False

    def __init__(self):
        display.screen.fill(self.bgcolor)
        self.menuTimeStamp = datetime.datetime.now()

    def gui_thread(self):
        tfps=0.5

        while(terrarium.runFlag == True):
            self.touchPointList.clear()
            if(self.activeTab == 0):
                self.main_tab()
            elif(self.activeTab == 1):
                self.menu_main()
            elif(self.activeTab == 2):
                self.menu_sprayer()
            elif(self.activeTab == 3):
                self.menu_terrarium()
            time.sleep(tfps)  
            if((datetime.datetime.now() - self.menuTimeStamp) > (datetime.timedelta(seconds=self.menuTime))): #when idle then return to the home screen
                self.activeTab = 0 
                if self.settingsSavedFlag == False:
                    settings.save_settings()
                    self.settingsSavedFlag = True

    def touch_thread(self):
        while(terrarium.runFlag == True):
            self.touch_event()
            time.sleep(0.01) 

    def main_tab(self):
        iconsPosition=5
        display.icons(0, 0, 255, "background")

        if(gpio.mainLightFlag == True):
            display.icons(10, iconsPosition, 255, "bulb1")
            iconsPosition += 125

        if(gpio.check_heater_flag() == True):
            display.icons(10, iconsPosition, 255, "bulb2")
            dl=display.label_center(display.screen, "{}%".format(gpio.read_heater_pwm()), "Nimbus Sans L", 48, 70, iconsPosition + 65, (235, 0, 69), 255)
            iconsPosition += 125

        if(gpio.check_sprayer_flag() == True):
            display.icons(10, iconsPosition, 255, "sprayer")
            iconsPosition += 125

        dl=display.label(display.screen, "{:.1f}°C".format(terrarium.temperatureTop), "Nimbus Sans L", 150, 290, 10, (247, 130, 59), 255) #(241, 198, 228)
        display.label(display.screen, "{:.0f}%".format(terrarium.humidityTop), "Nimbus Sans L", 80, 320+dl, 50, (183, 176, 241), 255)

        dl=display.label(display.screen, "{:.1f}°C".format(terrarium.temperatureBottom), "Nimbus Sans L", 150, 290, 370, (110, 254, 192), 255) #(206, 241, 198)
        display.label(display.screen, "{:.0f}%".format(terrarium.humidityBottom), "Nimbus Sans L", 80, 320+dl, 410, (183, 176, 241), 255)

        display.label(display.screen, "UVI:{:.4f}".format(terrarium.uvi), "Nimbus Sans L", 70, 430, 180, (253, 201, 77), 255)
        display.label(display.screen, "UVA: {:.2f} UVB: {:.2f}".format(terrarium.uva, terrarium.uvb), "Nimbus Sans L", 48, 370, 240, (254, 138, 35), 255)

        display.label(display.screen, "{}".format(datetime.datetime.now().strftime('%H:%M:%S')), "Nimbus Sans L", 60, 30, 420, (200, 240, 200), 255)

        self.touchPointList.append(((0, 0, 400, 480), "menu"))
        self.touchPointList.append(((630, 0, 800, 150), "exit"))
        pygame.display.update()

    def menu_main(self):
        end = timer()

        display.icons(0, 0, 255, "background")
        self.touchPointList.append(display.button_with_text("sprayer", display.screen, (30, 60, 300, 120), (223, 169, 191), (223, 169, 151), 10, 2, "deszcz", 80, (253, 50, 35)))
        self.touchPointList.append(display.button_with_text("dripper", display.screen, (30, 220, 300, 120), (216, 155, 43), (216, 155, 0), 10, 2, "dripper", 80, (253, 50, 35)))
        self.touchPointList.append(display.button_with_text("terrarium", display.screen, (360, 60, 300, 120), (187, 179, 41), (187, 179, 0), 10, 2, "terrarium", 75, (253, 50, 35)))
        self.touchPointList.append(display.button_with_text("ventilation", display.screen, (360, 220, 300, 120), (213, 0, 88), (213, 0, 38), 10, 2, "wentylacja", 75, (253, 50, 35)))
        display.label(display.screen, "czas pracy:{}".format(str(datetime.timedelta(seconds = round(end - terrarium.startTime)))), "Nimbus Sans L", 30, 50, 440, (150, 150, 150), 100)
        self.touchPointList.append(display.button_with_text("back", display.screen, (690, 390, 100, 80), (120, 120, 120), (15, 15, 15), 10, 2, "<", 120, (0, 0, 0)))
        pygame.display.update()

    def menu_sprayer(self):
        end = timer()
        display.icons(0, 0, 255, "background")

        display.label(display.screen, "Timer 1: ", "Nimbus Sans L", 60, 30, 40, (253,180,165), 255)
        self.touchPointList.append(display.button_with_text("SprayTimer1_H-", display.screen, (200,10,80,50), (200, 200, 200), (250, 250, 250), 10, 2, "-", 90, (15, 15, 15)))
        self.touchPointList.append(display.button_with_text("SprayTimer1_H+", display.screen, (200,60,80,50), (80, 80, 80), (50, 50, 50), 10, 2, "+", 80, (220, 220, 220)))
        display.button(display.screen, (285,10,100,100),(55,112,21), (55,112,21), 10, 2)
        display.label(display.screen, "{:02d}".format(sprayer.spraying1.hour), "Nimbus Sans L", 120, 290, 17, (220, 220, 220), 255)
        display.label(display.screen, ":", "Nimbus Sans L", 120, 382, 15, (220, 220, 220), 255)
        display.button(display.screen, (400, 10, 100, 100), (55, 112, 21), (55, 112, 21), 10, 2)
        display.label(display.screen, "{:02d}".format(sprayer.spraying1.minute), "Nimbus Sans L", 120, 405, 17, (220, 220, 220), 255)
        self.touchPointList.append(display.button_with_text("SprayTimer1_M-", display.screen, (505, 10, 80, 50), (200, 200, 200), (250, 250, 250), 10, 2, "-", 90, (15, 15, 15)))
        self.touchPointList.append(display.button_with_text("SprayTimer1_M+", display.screen, (505, 60, 80, 50), (80, 80, 80), (50, 50, 50), 10, 2, "+", 80, (220, 220, 220)))

        display.label(display.screen, "Timer 2: ", "Nimbus Sans L", 60, 30, 170, (253,180,165), 255)
        self.touchPointList.append(display.button_with_text("SprayTimer2_H-", display.screen, (200, 140, 80, 50), (200, 200, 200), (250, 250, 250), 10, 2, "-", 90, (15, 15, 15)))
        self.touchPointList.append(display.button_with_text("SprayTimer2_H+", display.screen, (200, 190, 80, 50), (80, 80, 80), (50, 50, 50), 10, 2, "+", 80, (220, 220, 220)))
        display.button(display.screen, (285, 140, 100, 100), (55, 112, 21), (55, 112, 21), 10, 2)
        display.label(display.screen, "{:02d}".format(sprayer.spraying2.hour), "Nimbus Sans L", 120, 290, 147, (220, 220, 220), 255)
        display.label(display.screen, ":", "Nimbus Sans L", 120, 382, 145, (220, 220, 220), 255)
        display.button(display.screen, (400, 140, 100, 100), (55, 112, 21), (55, 112, 21), 10, 2)
        display.label(display.screen, "{:02d}".format(sprayer.spraying2.minute), "Nimbus Sans L", 120, 405, 147, (220, 220, 220), 255)
        self.touchPointList.append(display.button_with_text("SprayTimer2_M-", display.screen, (505, 140, 80, 50), (200, 200, 200), (250, 250, 250), 10, 2, "-", 90, (15, 15, 15)))
        self.touchPointList.append(display.button_with_text("SprayTimer2_M+", display.screen, (505, 190, 80, 50), (80, 80, 80), (50, 50, 50), 10, 2, "+", 80, (220, 220, 220)))

        display.label(display.screen, "Czas spryskiwania: ", "Nimbus Sans L", 60, 30, 290, (253, 180, 165), 255)
        self.touchPointList.append(display.button_with_text("SprayTime_-", display.screen, (420, 270, 80, 80), (200, 200, 200), (250, 250, 250), 10, 2, "-", 110, (15, 15, 15)))
        display.button(display.screen, (505, 270, 200, 80), (55, 112, 21), (55, 112, 21), 10, 2)
        display.label(display.screen, "{} s".format(sprayer.sprayingTime), "Nimbus Sans L", 80, 535, 280, (15, 15, 15), 255)
        self.touchPointList.append(display.button_with_text("SprayTime_+", display.screen, (710, 270, 80, 80), (200, 200, 200), (250, 250, 250), 10, 2, "+", 80, (15, 15, 15)))

        display.label(display.screen, "Manualne: ", "Nimbus Sans L", 60, 30, 410, (253, 180, 165), 255)
        self.touchPointList.append(display.button_with_text("SprayTimeManual_-", display.screen, (240, 380, 80, 50), (200, 200, 200), (250, 250, 250), 10, 2, "-", 90, (15, 15, 15)))
        self.touchPointList.append(display.button_with_text("SprayTimeManual_+", display.screen, (240, 430, 80, 50), (80, 80, 80), (50, 50, 50), 10, 2, "+", 80, (220, 220, 220)))
        display.button(display.screen, (325, 380, 200, 100), (55, 112, 21), (55, 112, 21), 10, 2)
        display.label(display.screen, "{} s".format(sprayer.sprayingTimeManual), "Nimbus Sans L", 80, 350, 400, (220, 220, 220), 255)
        display.button(display.screen, (530, 380, 80, 100), (20, 192, 21), (30, 220, 21), 10, 2)

        display.label(display.screen, "ostatnie:", "Nimbus Sans L", 40, 670, 20, (253, 201, 77), 255)
        display.label(display.screen, "{}".format(str(datetime.timedelta(seconds=round(end - sprayer.lastSpraying)))), "Nimbus Sans L", 40, 670, 60, (253, 201, 77), 255)

        self.touchPointList.append(display.button_with_text("back", display.screen, (690, 390, 100, 80), (120, 120, 120), (15, 15, 15), 10, 2, "<", 120, (0, 0, 0)))
        pygame.display.update()

    def menu_terrarium(self):
        end = timer()
        display.icons(0, 0, 255, "background")

        myTop = 20
        display.label(display.screen, "Min wilgotność: ", "Nimbus Sans L", 48, 110, myTop+20, (253, 180, 165), 255)
        self.touchPointList.append(display.button_with_text("MinHumidity_-", display.screen, (410, myTop, 80, 80), (200, 200, 200), (250, 250, 250), 10, 2, "-", 110, (15, 15, 15)))
        display.button(display.screen, (495, myTop, 200, 80), (55, 112, 21), (55, 112, 21), 10, 2)
        display.label(display.screen, "{} %".format(terrarium.minimumHumidity), "Nimbus Sans L", 80, 525, myTop+10, (220, 220, 220), 255)
        self.touchPointList.append(display.button_with_text("MinHumidity_+", display.screen, (700, myTop, 80, 80), (200, 200, 200), (250, 250, 250), 10, 2, "+", 80, (15, 15, 15)))

        myTop += 110
        display.label(display.screen, "Temperatura na wyspie: ", "Nimbus Sans L", 45, 30, myTop+20, (253, 180, 165), 255)
        self.touchPointList.append(display.button_with_text("ReqTemperatureIsland_-", display.screen, (410, myTop, 80, 80), (200, 200, 200), (250, 250, 250), 10, 2, "-", 110, (15, 15, 15)))
        display.button(display.screen, (495, myTop, 200, 80), (55, 112, 21), (55, 112, 21), 10, 2)
        display.label(display.screen, "{}*C".format(terrarium.temperatureRequiredIsland), "Nimbus Sans L", 80, 520, myTop+10, (220, 220, 220), 255)
        self.touchPointList.append(display.button_with_text("ReqTemperatureIsland_+", display.screen, (700, myTop, 80, 80), (200, 200, 200), (250, 250, 250), 10, 2, "+", 80, (15, 15, 15)))

        myTop += 110
        display.label(display.screen, "minimalne UVI", "Nimbus Sans L", 48, 110, myTop+3, (253, 180, 165), 255)
        display.label(display.screen, "dla ogrzewania: ", "Nimbus Sans L", 50, 110, myTop+40, (253, 180, 165), 255)
        self.touchPointList.append(display.button_with_text("minUviForHeating_-", display.screen, (410, myTop, 80, 80), (200, 200, 200), (250, 250, 250), 10, 2, "-", 110, (15, 15, 15)))
        display.button(display.screen, (495, myTop, 200, 80), (55, 112, 21), (55, 112, 21), 10, 2)
        display.label(display.screen, "{}°C".format(terrarium.minUviForHeating), "Nimbus Sans L", 80, 520, myTop+10, (220, 220, 220), 255)
        self.touchPointList.append(display.button_with_text("minUviForHeating_+", display.screen, (700, myTop, 80, 80), (200, 200, 200), (250, 250, 250), 10, 2, "+", 80, (15, 15, 15)))
        
        self.touchPointList.append(display.button_with_text("backToMain", display.screen, (690, 390, 100, 80), (120, 120, 120), (15, 15, 15), 10, 2, "<", 120, (0, 0, 0)))

        pygame.display.update()

    def click_event(self, name):
        if name == "menu":
            self.activeTab = 1
        elif name == "sprayer":
            self.activeTab = 2
            settingsSavedFlag = False
        elif name == "terrarium":
            self.activeTab = 3
            settingsSavedFlag = False
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
        elif name == "ReqTemperatureIsland_+":
            if terrarium.temperatureRequiredIsland < 99:
                terrarium.temperatureRequiredIsland += 1
            else:
                terrarium.temperatureRequiredIsland = 0
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
                px=event.pos[0]
                py=event.pos[1]
                self.menuTimeStamp = datetime.datetime.now()
                for point in  self.touchPointList:
                    click = point[0]
                    clickX = click[0]
                    clickY = click[1]
                    clickWidth = click[2]
                    clickHeight = click[3]
                    if(px > clickX and px < (clickX + clickWidth) and py > clickY and py < (clickY + clickHeight)):
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

gui = Gui()