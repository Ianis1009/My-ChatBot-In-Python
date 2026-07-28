from datetime import datetime

start_time = datetime.now()

user_messages = 0
bot_messages = 0

wiki_searches = 0

voice_changes = 0

commands = []

#TODO

def add_command(command):
    commands.append(command)

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

def get_report():
    #TODO
    pass