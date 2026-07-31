# from datetime import datetime

# start_time = datetime.now()

# user_messages = 0
# bot_messages = 0

# wiki_searches = 0

# voice_changes = 0

# commands = []

from datetime import datetime


chat_start = datetime.now()

total_commands = 0

total_responses = 0

wikipedia_searches = 0

voice_changes = 0

mute_changes = 0

#TODO

# def add_command(command):
#     commands.append(command)

def add_user():
    global user_messages
    user_messages += 1

def add_bot():

    global bot_messages

    bot_messages += 1

def add_wiki():

    global wiki_searches

    wiki_searches += 1

def add_voice_change():

    global voice_changes

    voice_changes += 1


def add_command():

    global total_commands

    total_commands += 1

def get_statistics():

    duration = (datetime.now() - chat_start)

    return (
        "CHAT STATISTICS\n\n"
        f"Duration: {duration}\n"
        f"Commands: {total_commands}\n"
        f"Bot responses: {total_responses}\n"
        f"Wikipedia searches: "
        f"{wikipedia_searches}\n"
        f"Voice changes: "
        f"{voice_changes}\n"
        f"Mute changes: "
        f"{mute_changes}" )