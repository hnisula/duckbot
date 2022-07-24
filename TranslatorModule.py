from multiprocessing.sharedctypes import Value
import deepl

class TranslatorModule:
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
        
        language_option = message_parts[1].split("-")
        text = " ".join(message_parts[2:])
        source_language = None

        if len(language_option) > 1:
            source_language = language_option[0]
        
        try:
            response = self.deepl_translator.translate_text(
                text,
                source_lang=source_language,
                target_lang=language_option[-1])
            
            print(response)
        except deepl.DeepLException as ex:
            print(ex.args)
        except ValueError as ex:
            print(ex.args)
        except TypeError as ex:
            print(ex.args)
