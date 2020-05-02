from pynput.mouse import Button, Controller
from PIL import ImageGrab
from random import seed
from random import randint
import threading, time
import urllib.request
import numpy as np
import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

mouse = Controller()
seed(1)

starttime=time.time() 
# positions of important things (662, 735) - Map Location - (1072, 634) regular monkey
# (1103, 634) - Nail Monkey - (1141, 628) - Bommerang Monkey - (1175, 631) - Catapault Monkey

# top left (565, 545) # Top Right (1200, 545)
# bottom left (565, 1024) # bottom right (1200, 1024)

monkeyProperties = [['Reg Monkey', 210, '1072 634'],['Nail Monkey', 305, '1103 634'],['Boomer Monkey', 440, '1141 628']]
Locations = ['640 618','710 618', '790 618', '850 618', '930 618', '1016 618', '584 673', '745 692', '905 691', '953 786', '693 1000', '976 928', '854 992', '756 995'] #all locations
openLocations = Locations
closedLocations = []

def buy_Monkey(monkeyIndex, money):
    if money > monkeyProperties[monkeyIndex][1]:
        mouse.position = (int(monkeyProperties[monkeyIndex][2][ : monkeyProperties[monkeyIndex][2].index(' ')]), int(monkeyProperties[monkeyIndex][2][monkeyProperties[monkeyIndex][2].index(' ') : ]))
        print(int(monkeyProperties[monkeyIndex][2][ : monkeyProperties[monkeyIndex][2].index(' ')]), int(monkeyProperties[monkeyIndex][2][monkeyProperties[monkeyIndex][2].index(' ') : ]))
        mouse.click(Button.left, 1)
        mousePos = openLocations[randint(0, len(openLocations) - 1)]
        mouse.position = (int(mousePos[ : mousePos.index(' ')]), int(mousePos[mousePos.index(' ') : ]))
        closedLocations.append(mousePos) # adds the mouse position to the closed list since it cant be called anymore
        openLocations.remove(mousePos)
        mouse.click(Button.left, 1)
        time.sleep(0.5)
        return


def mostOptimalMonkey(moneyAmount):
    highestBuyable = 0
    highestIndex = 0
    for i in monkeyProperties:
        if moneyAmount > i[1]:
            if i[1] > highestBuyable:
                    highestBuyable = i[1]
                    highestIndex = monkeyProperties.index(i)
    buy_Monkey(highestIndex, moneyAmount)
    return

def StartRound():
    #1105, 1006 Start Button Locations
    mouse.position = (1105, 1006)
    mouse.click(Button.left, 1)
    return

while True:
    #screen = np.array(ImageGrab.grab(bbox = (565, 545, 1200, 1024))) # how big the # is and where it is located
    screen = np.array(ImageGrab.grab(bbox = (1125, 550, 1190, 570))) # how big the # is and where it is located
    startButton = np.array(ImageGrab.grab(bbox = (1050, 980, 1190, 1024))) # how big the # is and where it is located
    

    cv2.imshow('window', cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))

    print(mouse.position) # shows the mouse location and also
    #time.sleep(1.0 - ((time.time() - starttime) % 1.0))

    # get the money text


    text = pytesseract.image_to_string(screen, config ='--psm 7')
    money = 0
    print(text)
    try:
        money = int(text)
    except:
        print('error but its all right')

    startRound = pytesseract.image_to_string(startButton, config ='--psm 7')
    try:
        if(startRound == 'Start Round'):
            StartRound()
    except:
        print('error but its all right')

    mostOptimalMonkey(money)


    if cv2.waitKey(25) & 0XFF == ord('q'):
        cv2.destroyAllWindows()
        break



# buy function

