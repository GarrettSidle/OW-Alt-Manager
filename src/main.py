
import getPlayerInfo
import extractFiles
import createWindow



logins, config = extractFiles.extractFiles()
player_data = (getPlayerInfo.getPlayersInfo(logins, config))
     
createWindow.createWindow(logins, player_data, config)


