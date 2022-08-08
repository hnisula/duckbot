from .translation_module import TranslationModule

class CommandProcessor:
    @classmethod
    async def create(cls, config):
        translator = await TranslationModule.create(config)

        return cls(translator)
    
    def __init__(self, translator):
        self.translator = translator
    
    async def parse_command(self, message):
        if not message.startswith("!"):
            return
        
        message_parts = message.split()

        match message_parts[0]:
            case "!tl":
                return await self.translator.translate(message_parts)
