import deepl
from .command_response import CommandResponse, CommandResponseType

class TranslationModule:
    @classmethod
    async def create(cls, config):
        auth_key = config["translator"]["auth_key"]
        deepl_translator = deepl.Translator(auth_key)

        return cls(deepl_translator)
    
    def __init__(self, deepl_translator):
        self.deepl_translator = deepl_translator
    
    async def translate(self, message_parts):
        command = message_parts[0]

        if command != "!tl":
            print(f"ERROR: Translator module received unknown command ({command})")
        
        source_lang = message_parts[1]
        target_lang = message_parts[2]
        text = " ".join(message_parts[3:])

        if source_lang == "." or source_lang == "?":
            source_lang = None

        try:
            translation = self.deepl_translator.translate_text(
                text,
                source_lang=self.__handle_shorthands(source_lang),
                target_lang=self.__handle_shorthands(target_lang))
            
            return self.create_response(
                translation.text,
                source_lang or translation.detected_source_lang,
                target_lang)
        except deepl.DeepLException as ex:
            return self.create_error_response(ex.args)
        except ValueError as ex:
            return self.create_error_response(ex.args)
        except TypeError as ex:
            return self.create_error_response(ex.args)

    # It seems the library does not require this but the API does
    def __handle_shorthands(self, language_tag):
        match language_tag:
            case "en":
                return "en-us"
            case _:
                return language_tag

    def create_response(self, text, source_lang, target_lang):
        response = CommandResponse

        response.type = CommandResponseType.MESSAGE
        response.status = "success"
        response.command_type = "translation"
        response.content = f"Translation [{source_lang.lower()}->{target_lang.lower()}]: {text}"

        return response;
    
    def create_error_response(self, error):
        response = CommandResponse
        
        response.type = CommandResponseType.MESSAGE
        response.status = "error"
        response.command_type = "translation"
        response.content = f"Translation failed: {error}"

        return response
    