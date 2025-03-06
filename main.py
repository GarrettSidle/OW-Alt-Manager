
import getPlayerInfo
import extractFiles
import createWindow

login_data = []


logins= extractFiles.extractFiles()
for login in logins:
    login_data.append(getPlayerInfo.getPlayerInfo(login))
     


createWindow.createWindow(logins, login_data)


