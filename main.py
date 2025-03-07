
import getPlayerInfo
import extractFiles
import createWindow



logins= extractFiles.extractFiles()
login_data = (getPlayerInfo.getPlayersInfo(logins))
     
createWindow.createWindow(logins, login_data)


