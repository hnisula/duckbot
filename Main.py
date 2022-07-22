import asyncio
import MatrixClient
from Config import read_config_file

config = read_config_file("config.yaml")

SERVER_URL = config["server"]["url"]
DEVICE_ID = config["device"]["id"]
DEVICE_NAME = config["device"]["name"]
PW = config["bot"]["password"]
USERNAME = config["bot"]["username"]

async def main_test():
    client = MatrixClient()

    await client.init(SERVER_URL)
    await client.login(USERNAME, PW, DEVICE_ID, DEVICE_NAME)
    await client.sync_loop()

asyncio.run(main_test())