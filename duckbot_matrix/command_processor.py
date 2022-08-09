from duckbot_matrix.command_response import CommandResponse, CommandResponseType
from .translation_module import TranslationModule

class CommandProcessor:
    @classmethod
    async def create(cls, config):
        translator = await TranslationModule.create(config)

        return cls(translator)
    
    def __init__(self, translator):
        self.translator = translator

        with open("duckbot_matrix/help_text.md") as file:
            self.help_text = file.read()

        # with open("duckbot_matrix/help_text_formatted.txt") as file:
        #     self.help_text_formatted = file.read()

        self.read_version()
    
    async def parse_command(self, message):
        if not message.startswith("!"):
            return
        
        message_parts = message.split()

        match message_parts[0]:
            case "!tl":
                return await self.translator.translate(message_parts)
            case "!help":
                return self.help_command(message_parts)
            case "!version":
                return self.version_command(message_parts)
    
    def help_command(self, message_parts):
        if message_parts[0] != "!help":
            print(f"ERROR: Help command callback received unknown command ({message_parts[0]}")
        
        response = CommandResponse

        response.type = CommandResponseType.MESSAGE
        response.status = "success"
        response.command_type = "help"
        response.content = self.help_text
        # response.formatted_content = self.help_text_formatted

        return response
    
    def version_command(self, message_parts):
        if message_parts[0] != "!version":
            print(f"ERROR: Version command callback received unknown command ({message_parts[0]}")
        
        response = CommandResponse

        response.type = CommandResponseType.MESSAGE
        response.status = "success"
        response.command_type = "version"
        response.content = self.version

        return response

    def read_version(self):
        with open("pyproject.toml") as file:
            lines = file.readlines()

            for line in lines:
                if line.startswith("version"):
                    parts = line.split("=")
                    
                    if len(parts) != 2:
                        raise Exception("version line in pyproject.toml is not valid")
                    
                    self.version = parts[1].strip().strip("\"")
