import pyautogui
import mss
import numpy as np
from PIL import Image
import time
import psutil
import pygetwindow as gw
import win32gui
import win32con
import win32api

def is_battlenet_open():
    for process in psutil.process_iter(attrs=['pid', 'name']):
        if "Battle.net.exe" in process.info['name']:
            return True
    return False

def move_to_main_monitor():
    windows = [win for win in gw.getWindowsWithTitle("Battle.net") if win.isActive or win.isMaximized or win.isMinimized]
    if(not windows):
        print("empty")
        return 
    
    
    #Get the window
    battlenet_window = windows[0]
    if battlenet_window.isMinimized:
        battlenet_window.restore()
        time.sleep(1)
    battlenet_window.maximize()
    
    #bring it to the front
    hwnd = battlenet_window._hWnd 
    print(hwnd)
    win32gui.SetForegroundWindow(hwnd)
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    
    # Get the primary monitor's resolution
    monitor_info = win32api.GetMonitorInfo(win32api.MonitorFromPoint((0, 0)))
    left, top, right, bottom = monitor_info["Monitor"]
    screen_width = right - left
    screen_height = bottom - top

    # Get current Battle.net window size
    rect = win32gui.GetWindowRect(hwnd)
    win_width = rect[2] - rect[0]
    win_height = rect[3] - rect[1]

    # Calculate new position to center the window
    new_x = left + (screen_width - win_width) // 2
    new_y = top + (screen_height - win_height) // 2

    # Move the window to the center of the main monitor (without resizing)
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, new_x, new_y, 0, 0, 
                        win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW)
    battlenet_window.maximize()

    print("Battle.net moved to the main monitor.")

def wait_for_image(image, attemptLimit):
    attemptCounter = 0
    location = None
    while(not location):
        
        
        try:
            location = pyautogui.locateCenterOnScreen(f'images/{image}.png', confidence=0.8)
            print(F'----------------------FOUND {image.upper()}----------------------')
            return location
        except:
            print(f"Cannot Find {image}")
        
        time.sleep(attemptCounter * .1)
        attemptCounter += 1
    
        if attemptCounter > attemptLimit:
            return None
        

def launchGame(login):
    # Open Battle.net app
    pyautogui.press("win")
    time.sleep(.5)
    pyautogui.write("Battle.net")
    pyautogui.press("enter")
    time.sleep(.5)

    while(not is_battlenet_open()):
        print("Waiting for Battlenet Task")
        time.sleep(0.1)
    print("battlenet has opened")
    
    location = None
    attemptCounter = 0
    while(not location):
        
        move_to_main_monitor()
    
        try:
            location = pyautogui.locateCenterOnScreen('images/BattleNetLoginLogo.png', confidence=0.8)
            isLoggedIn = False
            break
        except:
            print("Cannot Find Login Screen")
        
        try:
            location = pyautogui.locateCenterOnScreen('images/BattleNetHomeLogo.png', confidence=0.8)
            isLoggedIn = True
            break
        except:
            print("Cannot Find Home Screen")
        time.sleep(attemptCounter * .1)
        attemptCounter += 1
        if attemptCounter > 15:
            return
        print("waiting for opening")
    
    prefix = "" if isLoggedIn else "NOT "
    print(f"Account is {prefix}Logged In")
    
    
    #If we are logged in
    if(isLoggedIn):
        #Log out

        #find the area beneath account
        location = wait_for_image('BelowAccount', 10)
        if(not location):
            return
        new_x, new_y = location[0], location[1] - 50
        #click account
        pyautogui.click(new_x, new_y)
    
        
        #logout
        location = wait_for_image('LogOut', 10)
        if(not location):
            return
        
        pyautogui.click(location)

        #Wait for the login screen to appear
        location = wait_for_image('BattleNetLoginLogo', 25)
        if(not location):
            return
        
    
    #tab to the email feild
    pyautogui.hotkey('shift', 'tab')
    
    #delete any existing email
    pyautogui.press('backspace')

    #write account email 
    pyautogui.write(login['email'])
    
    #tab to the password feild
    pyautogui.press("tab")

    pyautogui.write(login['password'])
    pyautogui.press("enter")
    
    time.sleep(5)
    move_to_main_monitor()
    time.sleep(.3)
    
    #Wait for the Home screen to appear
    location = wait_for_image('BattleNetHomeLogo', 25)
    if(not location):
        return
        

    #find the overwatch button
    location = wait_for_image('OverwatchLogo', 10)
    if(not location):
        return
    pyautogui.click(location)
    
    #find the play button
    location = wait_for_image('Play', 10)
    if(not location):
        return
    #pyautogui.click(location)

    windows = [win for win in gw.getWindowsWithTitle("Battle.net") if win.isActive or win.isMaximized or win.isMinimized]
    hwnd = windows[0]._hWnd
    win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
    print("Battle.net window closed.")
    