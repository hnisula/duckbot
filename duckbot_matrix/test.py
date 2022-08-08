import asyncio
import yaml
from nio import AsyncClient, MatrixRoom, RoomMessageText, InviteEvent, Event

DEVICE_ID = "UAXKBVAPUI"

def read_config_file(config_filename):
    with open(config_filename, "r") as config_file:
        return yaml.load(config_file, yaml.FullLoader)

config = read_config_file("config.yaml")
client = AsyncClient(config["server_url"])
client.user_id = config["bot_username"]
client.access_token = config["access_token"]
client.device_id = config["old_device_id"]
client.room_id = config["room_id"]

async def message_callback(room: MatrixRoom, event: Event) -> None:
    print(event)

async def invite_callback(room: MatrixRoom, event: InviteEvent):
    await client.join(room.room_id)

async def main() -> None:
    client.add_event_callback(message_callback, Event)
    client.add_event_callback(invite_callback, InviteEvent)

    t = await client.room_send(client.room_id, "m.room.message", {"msgtype": "m.text", "body": "hejsan"})
    r = await client.encrypt(client.room_id, "m.room.message", {"msgtype": "m.text", "body": "hejsan (encrypted)"})

    await client.sync_forever(timeout=30000)

    await client.close()

asyncio.get_event_loop().run_until_complete(main())