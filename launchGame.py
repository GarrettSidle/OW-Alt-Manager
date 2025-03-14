import pyautogui
import mss
import numpy as np
from PIL import Image
import time
from screeninfo import get_monitors


def launchGame(login):
    # Open Battle.net app
    pyautogui.press("win")
    time.sleep(1)
    pyautogui.write("Battle.net")
    pyautogui.press("enter")

    # Wait for app to open
    time.sleep(3)
    
    pyautogui.hotkey('win', 'up')
    
    monitors_resolution = []
    leftMost = 0
    for monitor in get_monitors():
        print(monitor)
        monitors_resolution.append(monitor)
        leftMost = min(leftMost, monitor.x)
        
    print(leftMost)
    
    
    with mss.mss() as sct:
        monitor_screenshot = sct.grab(sct.monitors[0])  
        img = Image.frombytes("RGB", monitor_screenshot.size, monitor_screenshot.rgb)
        img.save("multi_monitor_screenshot.png") 
        
    img = Image.frombytes("RGB", monitor_screenshot.size, monitor_screenshot.rgb)
    
    location = None
    try:
        location = pyautogui.locate('images/BattleNetLogin.png', img, confidence=0.8)
    except:
        print("Cannot Find Login Screen")
    
    try:
        location = pyautogui.locate('images/BattleNetHomeLogo.png', img, confidence=0.8)
    except:
        print("Cannot Find Home Screen")
        
    if(not location):
        print("Cannot find application")
        return
    
    print(location)
    location = location._replace(left=location.left + leftMost)
    print(location)
    pyautogui.click(location)    
    

    # try:
    #     isLoggedIn = not (pyautogui.locateOnScreen('images/BattleNetLogin.png'))
    # except:
    #     isLoggedIn = False
    
    # if(isLoggedIn):
    #     print("isloggedin")
    #     for i in range(9):
    #         pyautogui.press('tab')
    #     pyautogui.press('enter')
    #     for i in range(11):
    #         pyautogui.press('down')
    #     pyautogui.press('enter')
    # time.sleep(5)
    
    # pyautogui.hotkey('shift', 'tab')
    
        
    # pyautogui.press('backspace')

    # pyautogui.write(login['email'])
    # pyautogui.press("tab")

    # pyautogui.write(login['password'])
    # pyautogui.press("enter")
    # time.sleep(5)
    
    # for i in range(10):
    #     pyautogui.press('tab')
    # pyautogui.press("enter")
    # time.sleep(2)
    # for i in range(7):
    #     pyautogui.press('tab')
    # pyautogui.press("enter")
    