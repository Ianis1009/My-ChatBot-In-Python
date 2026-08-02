
import special_characters

arrow = special_characters.arrow
user_arrow = special_characters.user_arrow

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


#TO DO - add all commands

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
    },
    "mute": {
        "usage" : "mute",
        "description":"The new state is Muted"
    },
    "unmute":{
        "usage":"unmute", 
        "description":"The new state is Voice"
    }, 
    "time": {
        "usage":"time",
        "description" : "Display current time." 
    }, 
    "date": {
        "usage":"date",
        "description" : "Display current date."
    }, 
    "joke" : {
        "usage" : "joke",
        "description" : "Dispaly a random joke."
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


def return_help_prompt():
    text_to_display = "Available commands:\n"
    for command, info in HELP.items():
        text_to_display += arrow 
        text_to_display += " "
        text_to_display += f"Command: {info['usage']}\n"
        text_to_display +=f"    Explication: {info['description']}\n"

    return text_to_display

def print_in_history():
    #TO DO
    pass