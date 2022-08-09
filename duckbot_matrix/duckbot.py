import psycopg2
from .matrix_client import MatrixClient
from .matrix_client_pg_storage import MatrixClientPgStorage
from .command_processor import CommandProcessor
from .command_response import CommandResponse, CommandResponseType

class DuckBot:
    @classmethod
    async def create(cls, config):
        db_host = config["storage"]["host"]
        db_name = config["storage"]["db_name"]
        db_username = config["storage"]["username"]
        db_password = config["storage"]["password"]
        server_url = config["server"]["url"]
        
        pg_connection = psycopg2.connect(host=db_host, database=db_name, user=db_username, password=db_password)
        matrix_client_storage = MatrixClientPgStorage.create(pg_connection)
        command_processor = await CommandProcessor.create(config)
        matrix_client = await MatrixClient.create(server_url, matrix_client_storage)

        return cls(matrix_client, command_processor)

    def __init__(self, matrix_client, command_processor):
        self.matrix_client = matrix_client
        self.command_processor = command_processor

        matrix_client.add_callback("m.room.message", self.text_callback)
    
    async def run(self, username, password, device_id, device_name, display_name):
        print(f"Logging in {username}...")
        await self.matrix_client.login(username, password, device_id, device_name)
        print("Logged in")
        await self.matrix_client.set_display_name(display_name)
        print("Running sync loop")
        await self.matrix_client.sync_loop()
    
    async def text_callback(self, event, room_info):
        message = event["content"]["body"]

        cmd_result = await self.command_processor.parse_command(message)

        if not cmd_result:
            return

        await self.process_command_response(cmd_result, room_info)
    
    async def process_command_response(self, cmd_result: CommandResponse, room_info):
        match cmd_result.type:
            case CommandResponseType.MESSAGE:
                await self.matrix_client.send_room_message(
                    room_info["room_id"],
                    cmd_result.content,
                    getattr(cmd_result, "formatted_content", None))
