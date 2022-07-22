import aiohttp
from aiohttp import web
import json
import yaml
import asyncio

def read_config_file(config_filename):
    with open(config_filename, "r") as config_file:
        return yaml.load(config_file, yaml.FullLoader)

config = read_config_file("config.yaml")

SERVER_URL = config["server"]["url"]
DEVICE_ID = config["device"]["id"]
DEVICE_NAME = config["device"]["name"]
PW = config["bot"]["password"]
USERNAME = config["bot"]["username"]

class matrix_client:
    def __init__(self, server_url):
        self.server_url = server_url
        self.session = aiohttp.ClientSession()
    
    async def register(self, username, password, device_name = None, device_id = None):
        register_request = {
            "device_id": device_id,
            "initial_device_display_name": device_name,
            "password": password,
            "refresh_token": True,
            "username": username
        }

        # This should be extracted into a method for handling the user-interactive auth (but perhaps fail on param requirements)
        auth_response = await self.session.post(f"{self.server_url}/_matrix/client/v3/register", json.dumps(register_request))
        auth_instructions = json.loads(auth_response.text)
        register_request["auth"] = {
            "type": auth_instructions["flows"][0]["stages"][0],
            "session": auth_instructions["session"]
        }
        register_response = await self.session.post(f"{self.server_url}/_matrix/client/v3/register", json.dumps(register_request))

        return json.loads(register_response.text)
    
    async def login(self, username, password):
        login_request = {
            "type": "m.login.password",
            "identifier": {
                "type": "m.id.user",
                "user": username
            },
            "device_id": DEVICE_ID,
            "initial_device_display_name": DEVICE_NAME,
            "password": password
        }
        async with self.session.post(f"{self.server_url}/_matrix/client/v3/login", json=login_request) as response:
            content = json.loads(await response.content.read())

            self.access_token = content.access_token
    
    async def send(self, room_id, message):
        return hej
    
    async def join_room(self):
        return 4

    async def sync_loop(self):
        response = await self.session.post()

async def main_test(client):
    await client.login(USERNAME, PW)
    await client.sync_loop()

client = matrix_client(SERVER_URL)

asyncio.run(main_test(client))