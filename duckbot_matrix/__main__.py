from .config import read_config_file
from .duckbot import DuckBot
import asyncio

async def main():
    config = read_config_file("config.yaml")
    bot_username = config["bot"]["username"]
    bot_password = config["bot"]["password"]
    bot_display_name = config["bot"]["display_name"]
    device_id = config["device"]["id"]
    device_name = config["device"]["name"]
    
    duckbot = await DuckBot.create(config)

    await duckbot.run(bot_username, bot_password, device_id, device_name, bot_display_name)

asyncio.run(main())
