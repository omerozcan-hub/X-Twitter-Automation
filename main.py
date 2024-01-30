
import config
from bot import Bot

TwitterBot = Bot(config.email,config.pw,config.username)
TwitterBot.login()
TwitterBot.post_multiple_image(config.images_path, "", config.logInfo_path)
TwitterBot.logout()
