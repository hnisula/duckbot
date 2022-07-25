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
            translation = self.deepl_translator.translate_text(
                text,
                source_lang=source_language,
                target_lang=language_option[-1])
            
            return self.create_result(
                translation.text,
                source_language or translation.detected_source_lang,
                language_option[-1])
        except deepl.DeepLException as ex:
            return self.create_error_result(ex.args)
        except ValueError as ex:
            return self.create_error_result(ex.args)
        except TypeError as ex:
            return self.create_error_result(ex.args)

    def create_result(self, text, source_lang, target_lang):
        return {
                "type": "translation",
                "status": "success",
                "text": text,
                "source_lang": source_lang,
                "target_lang": target_lang,
            }
    
    def create_error_result(self, error):
        return {
                "type": "translation",
                "status": "error",
                "error": error
            }
    