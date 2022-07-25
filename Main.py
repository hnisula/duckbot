import asyncio
from Config import read_config_file
from DuckBot import DuckBot

async def main():
    config = read_config_file("config.yaml")
    bot_username = config["bot"]["username"]
    bot_password = config["bot"]["password"]
    device_id = config["device"]["id"]
    device_name = config["device"]["name"]
    
    duckbot = await DuckBot.create(config)

    await duckbot.run(bot_username, bot_password, device_id, device_name)

asyncio.run(main())
