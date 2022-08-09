import enum
import string

class CommandResponseType(enum.Enum):
    MESSAGE = 1

class CommandResponse:
    type: CommandResponseType
    status: string
    command_type: string
    error: string
    content: string
    formatted_content: string