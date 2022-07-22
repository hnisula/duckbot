import asyncio
from MatrixClient import MatrixClient
from Config import read_config_file
from PgStorage import PgStorage

config = read_config_file("config.yaml")

DB_HOST = config["storage"]["host"]
DB_NAME = config["storage"]["db_name"]
DB_USERNAME = config["storage"]["username"]
DB_PASSWORD = config["storage"]["password"]

SERVER_URL = config["server"]["url"]
DEVICE_ID = config["device"]["id"]
DEVICE_NAME = config["device"]["name"]
PW = config["bot"]["password"]
USERNAME = config["bot"]["username"]

def print_message(event, room_status):
    print(event["content"]["body"])

async def main_test():
    storage = PgStorage()

    storage.init(DB_HOST, DB_NAME, DB_USERNAME, DB_PASSWORD)
    
    client = MatrixClient(storage)

    await client.init(SERVER_URL)
    client.add_callback("m.room.message", print_message)
    await client.login(USERNAME, PW, DEVICE_ID, DEVICE_NAME)
    await client.sync_loop()

asyncio.run(main_test())