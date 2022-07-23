import asyncio
import psycopg2
from MatrixClient import MatrixClient
from Config import read_config_file
from MatrixClientPgStorage import MatrixClientPgStorage

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
    pg_connection = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USERNAME, password=DB_PASSWORD)
    matrix_client_storage = MatrixClientPgStorage.create(pg_connection)
    client = await MatrixClient.create(SERVER_URL, matrix_client_storage)

    client.add_callback("m.room.message", print_message)

    print(f"Logging in {USERNAME}...")
    await client.login(USERNAME, PW, DEVICE_ID, DEVICE_NAME)
    print("Logged in")
    print("Running sync loop")
    await client.sync_loop()

asyncio.run(main_test())
