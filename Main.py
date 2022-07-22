import asyncio
from MatrixClient import MatrixClient
from Config import read_config_file

config = read_config_file("config.yaml")

SERVER_URL = config["server"]["url"]
DEVICE_ID = config["device"]["id"]
DEVICE_NAME = config["device"]["name"]
PW = config["bot"]["password"]
USERNAME = config["bot"]["username"]

def print_message(event, room_status):
    print(event["content"]["body"])

async def main_test():
    client = MatrixClient()

    await client.init(SERVER_URL)
    client.add_callback("m.room.message", print_message)
    await client.login(USERNAME, PW, DEVICE_ID, DEVICE_NAME)
    await client.sync_loop()

asyncio.run(main_test())