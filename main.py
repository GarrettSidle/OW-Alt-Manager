
import getPlayerInfo
import extractFiles
import createWindow



logins= extractFiles.extractFiles()
player_data = (getPlayerInfo.getPlayersInfo(logins))
     
createWindow.createWindow(logins, player_data)


