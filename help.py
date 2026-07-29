
import special_characters

#TO DO - add all
arr = special_characters.arrow

# information about commands
"""
HELP = {
    "hello": {},
    "how are you": {},
    "info": {},
    "voices":{},
    "set voice":{},
    "exit":{},
    "try voice": {}
}
"""

HELP = {
    "hello": {
        "usage": "hello",
        "description": "Greets the assistant."
    },

    "how are you": {
        "usage": "how are you",
        "description": "Shows the assistant status."
    },

    "info": {
        "usage": "info <topic>",
        "description": "Searches Wikipedia for a topic."
    },

    "voices": {
        "usage": "voices",
        "description": "Displays all available voices."
    },

    "set voice": {
        "usage": "set voice <1-2>",
        "description": "Changes the current voice."
    },

    "exit": {
        "usage": "exit",
        "description": "Terminates the assistant."
    },
    "try voice": {
        "usage": "try voice <1-2>",
        "description": "Try voices."
    }
}

def show_all_commands():
    print("\nAvailable commands\n")
    for command, info in HELP.items():
        print(f"{info['usage']}")
        print(f"    {info['description']}\n")

def show (command):
    command = command.lower()
    if command not in HELP:
        return "[INFO]: Unknown command"
    info = HELP[command]
    return (f"Command: {info['usage']}\n"
            f"Description: {info['description']}")

def print_in_history():
    #TO DO
    pass