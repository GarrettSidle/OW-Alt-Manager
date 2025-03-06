import pyautogui
import time


def launchGame(login):
    # Open Battle.net app
    pyautogui.press("win")
    time.sleep(1)
    pyautogui.write("Battle.net")
    pyautogui.press("enter")

    # Wait for app to open
    time.sleep(3)
    
    pyautogui.keyDown('win')
    pyautogui.press('up')
    pyautogui.keyUp('win')
    
    pyautogui.keyDown('win')
    pyautogui.keyDown('shift')
    pyautogui.press('right')
    pyautogui.keyUp('win')
    pyautogui.keyUp('shift')
    
    try:
        isLoggedIn = pyautogui.locateOnScreen('images/BattleNetHome.png')
    except:
        isLoggedIn = False
    
    if(isLoggedIn):
        print("isloggedin")
        for i in range(8):
            pyautogui.press('tab')
        pyautogui.press('enter')
        time.sleep(1)
        logout_location = pyautogui.locateOnScreen('images/LogOut.png')
        logout_center = pyautogui.center(logout_location)
        pyautogui.click(logout_center)
    
    for i in range(15):
        pyautogui.press('tab')
        
    pyautogui.press('backspace')

    pyautogui.write(login['email'])
    pyautogui.press("tab")

    pyautogui.write(login['password'])
    pyautogui.press("enter")
    time.sleep(5)
    
    for i in range(10):
        pyautogui.press('tab')
    pyautogui.press("enter")
    time.sleep(1)
    
    play_location = pyautogui.locateOnScreen('images/Play.png')
    play_center = pyautogui.center(play_location)
    pyautogui.click(play_center)