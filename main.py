
import getPlayerInfo
import extractFiles
import createWindow


account_data = []


logins, friends = extractFiles.extractFiles()
for login in logins:
    account_data.append(getPlayerInfo.getPlayerInfo(login))
createWindow.createWindow(logins, account_data)


