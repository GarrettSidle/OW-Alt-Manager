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
    

    try:
        isLoggedIn = pyautogui.locateOnScreen('images/BattleNetHome.png')
    except:
        isLoggedIn = False
    
    if(isLoggedIn):
        print("isloggedin")
        for i in range(8):
            pyautogui.press('tab')
        pyautogui.press('enter')
        for i in range(11):
            pyautogui.press('down')
        pyautogui.press('enter')
    time.sleep(5)
    
    
    
    pyautogui.keyDown('shift')
    pyautogui.press('tab')
    pyautogui.keyUp('shift')
    
        
    pyautogui.press('backspace')

    pyautogui.write(login['email'])
    pyautogui.press("tab")

    pyautogui.write(login['password'])
    pyautogui.press("enter")
    time.sleep(5)
    
    for i in range(10):
        pyautogui.press('tab')
    pyautogui.press("enter")
    time.sleep(2)
    for i in range(7):
        pyautogui.press('tab')
    pyautogui.press("enter")
    