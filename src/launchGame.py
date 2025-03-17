import pyautogui
import time
import psutil
import pygetwindow as gw
import win32gui
import win32con
import win32api

#checks if battlenet is a running task
def is_battlenet_open():
    for process in psutil.process_iter(attrs=['pid', 'name']):
        if "Battle.net.exe" in process.info['name']:
            return True
    return False

#moves the battlenet window to the main monitor 
def move_to_main_monitor():
    
    #get battle.net window
    windows = [win for win in gw.getWindowsWithTitle("Battle.net") if win.isActive or win.isMaximized or win.isMinimized]
    if(not windows):
        print("empty")
        return 
    
    
    #ensure the window is maximized
    battlenet_window = windows[0]
    if battlenet_window.isMinimized:
        battlenet_window.restore()
        time.sleep(1)
    battlenet_window.maximize()
    
    #bring it to the front
    hwnd = battlenet_window._hWnd 
    print(hwnd)
    
    # Check if Battle.net is already the focused window
    if hwnd == win32gui.GetForegroundWindow():
        print("Battle.net is already focused.")
        print(hwnd)
        
        # Get current window position
        rect = win32gui.GetWindowRect(hwnd)
        win_x, win_y, win_right, win_bottom = rect
        win_width = win_right - win_x
        win_height = win_bottom - win_y

        # Get primary monitor dimensions
        monitor_info = win32api.GetMonitorInfo(win32api.MonitorFromPoint((0, 0)))
        left, top, right, bottom = monitor_info["Monitor"]
        screen_width = right - left
        screen_height = bottom - top

        # Check if the window is already centered on the main monitor
        expected_x = left + (screen_width - win_width) // 2
        expected_y = top + (screen_height - win_height) // 2

        if abs(win_x - expected_x) < 400 and abs(win_y - expected_y) < 400:  # Allow small margin of error
            print("Battle.net is already on the main monitor.")
            return  # No need to move it
    
    
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

#attempts to locate an image on the screen 
def wait_for_image(image, attemptLimit):
    attemptCounter = 0
    location = None
    while(not location):
        try:
            #attempt to find the image
            location = pyautogui.locateCenterOnScreen(f'images/search/{image}.png', confidence=0.8)
            print(F'----------------------FOUND {image.upper()}----------------------')
            return location
        except:
            print(f"Cannot Find {image}")
        
        #slowly back off to reduce overhead
        time.sleep(attemptCounter * .1)
        attemptCounter += 1
    
        #if not found in the alloted attempts, stop
        if attemptCounter > attemptLimit:
            return None
        
def attemptFind(image):
    location = None
    try:
        location = pyautogui.locateCenterOnScreen(f'images/search/{image}.png', confidence=0.8)
        print(f"Found {image}")
    except:
        print(f"Cannot Find {image}")
    return location


def closeBattleNet():
    # Close out of Battle.net or Battle.net Login
    valid_titles = ["Battle.net", "Battle.net Login"]
    
    # Find all matching windows
    windows = [win for win in gw.getAllWindows() if win.title in valid_titles]
    
    if not windows:
        print("No Battle.net window found.")
        return
    
    # Close the first found window
    win32gui.PostMessage(windows[0]._hWnd, win32con.WM_CLOSE, 0, 0)
    print(f"{windows[0].title} window closed.")
    
        

def launchGame(login, config):
    PRIMARY_DELAY   = config["PrimaryDelay"]
    SECONDARY_DELAY = config["SecondaryDelay"]
    
    closeBattleNet()
    
    if win32api.GetKeyState(win32con.VK_CAPITAL):  # If Caps Lock is ON
        pyautogui.press('capslock')  # Toggle it OFF
        print("Caps Lock was ON. Turning it OFF.")
    
    # Open Battle.net app
    pyautogui.press("win")
    time.sleep(.5)
    pyautogui.write("Battle.net")
    pyautogui.press("enter")
    time.sleep(.5)

    #wait for battle net to open
    while(not is_battlenet_open()):
        print("Waiting for Battlenet Task")
        time.sleep(0.1)
    print("battlenet has opened")
    
    location = None
    attemptCounter = 0
    wasLoading = False
    
    move_to_main_monitor()
    while(not location):
        #slowly back off to reduce overhead
        time.sleep(attemptCounter * .1)
        attemptCounter += 1
        
        #if not found in the alloted attempts, stop
        if attemptCounter > PRIMARY_DELAY:
            return
           
        if(attemptFind("BattleNetLoginLogo")):
            wasLoading = True
            if(attemptFind("BattleNetLoginButton")):
                isLoggedIn = False
                break
        elif(wasLoading):
            if(attemptFind("BattleNetHomeLogo")):
                isLoggedIn = True
                break
            else:
                move_to_main_monitor()
        elif(attemptFind("BattleNetHomeLogo")):
            isLoggedIn = True
            break
    
    
    prefix = "" if isLoggedIn else "NOT "
    print(f"Account is {prefix}Logged In")
    
    
    #If we are logged in, log out
    if(isLoggedIn):

        #find the area beneath account
        location = wait_for_image('BelowAccount', SECONDARY_DELAY)
        if(not location):
            return
        #find account button and click it
        new_x, new_y = location[0], location[1] - 50
        pyautogui.click(new_x, new_y)
    
        #logout
        location = wait_for_image('LogOut', SECONDARY_DELAY)
        if(not location):
            return
        pyautogui.click(location)

        #Wait for the login screen to appear
        location = wait_for_image('BattleNetLoginLogo', PRIMARY_DELAY)
        if(not location):
            return
        
        time.sleep(.5)
    time.sleep(.5)
    
    #tab to the email feild
    pyautogui.hotkey('shift', 'tab')
    
    #delete any existing email
    pyautogui.press('backspace')

    #write account email 
    pyautogui.write(login['email'])
    
    #tab to the password feild
    pyautogui.press("tab")

    pyautogui.write(login['password'])
    time.sleep(.1)
    pyautogui.press("enter")
    
    time.sleep(5)
    move_to_main_monitor()
    time.sleep(.3)
    
    #Wait for the Home screen to appear
    location = wait_for_image('BattleNetHomeLogo', PRIMARY_DELAY)
    if(not location):
        return
        

    #find the overwatch button
    location = wait_for_image('OverwatchLogo', SECONDARY_DELAY)
    if(not location):
        return
    pyautogui.click(location)
    
    #find the play button
    location = wait_for_image('Play', SECONDARY_DELAY)
    if(not location):
        return
    pyautogui.click(location)
    
    time.sleep(3)

    closeBattleNet()
    
    