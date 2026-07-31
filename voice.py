import subprocess
import wikipedia
import requests

import jokes
import help # help.py
from datetime import datetime

wikipedia.set_lang("en")

voice_enabled = True # mute / unmute
current_voice = 2 # set by default
try_message1 = "This is a simple test for my voice"
try_message2 = "If you want to switch to this voice, you must use command set voice"

# some special characters that I use in UI

arrow = "\u27A4"
user_arrow = "\u276F"
date_icon = "\U0001F4C5"
time_icon = "\u231A" #clock
bar = "\u2500"
bot_icon = "\U0001F916"
usr_icon = "\U0001F464"
msg_icon = "\U0001F4AC"

# Voices by default, Microsoft
VOICES = {
    1: "Microsoft David Desktop",
    2: "Microsoft Zira Desktop",
}

#TODO refactor the code

def speak(text, voice=2):

    if not voice_enabled:
        return # mute mode
    # else 
    voice_name = VOICES.get(voice, VOICES[1]) 
    text = text.replace('"', '`"') #to avoid some errors 
    cmd = f'''Add-Type -AssemblyName System.Speech
    $s = New-Object System.Speech.Synthesis.SpeechSynthesizer
    $s.SelectVoice("{voice_name}")
    $s.Speak("{text}")
    '''
    subprocess.run(["powershell.exe", "-Command", cmd])


def save_message(author, message):

    with open("history.txt", "a", encoding="utf-8") as f:
        if author == "Bot":
            f.write(f"{bot_icon} {author}: {message}\n")
        else:
            f.write(f"{usr_icon} {author}: {message}\n")



def init_history():
    now = datetime.now()
    # print(bot_icon, "Bot started.")
    # print("Date:", now.strftime("%d/%m/%Y"))
    # print("Time:", now.strftime("%H:%M:%S"))
    date = now.strftime("%d/%m/%Y")
    time = now.strftime("%H:%M:%S")

    with open("history.txt", "w", encoding="utf-8") as f:
        initial_message = bot_icon + "  Bot started.\n"
        f.write(initial_message)
        f.write(f"{msg_icon}    New chat at: {date}, {time}\n")
        f.write(bar * 60)
        f.write("\n\n")
        
def get_wikipedia_info(topic):

    url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + topic.replace(" ", "_")
    try:
        response = requests.get(url,headers={"User-Agent": "PythonBot/1.0"},timeout=5)

        if response.status_code != 200:
            return "I couldn't find information about that topic."

        data = response.json()

        return data.get("extract", "No summary available.")

    except Exception as e:
        return "Error: " + str(e)


def process_command(command):

    global current_voice
    global voice_enabled
    command = command.strip()

    if command.lower() == "hello":
        return "Hello! How can I help you?"

    elif command.lower() == "how are you":
        return "I'm doing great! Thanks for asking."
    elif command.lower() == "mute":
        voice_enabled = False
        return "[INFO]: Voice output is muted."
    elif command.lower() == "unmute":
        voice_enabled = True
        return "[INFO]: Voice output is enabled."
    elif command.lower() == "voices":
        #print("Available voices:")
        text_to_display_voices = "Available voices:\n"
        for number, name in VOICES.items():
            #print(f"{number} <--> {name}")
            text_to_display_voices += f"{number}. {name}\n"
        text_to_display_voices += "[INFO]: you must select one number from that list in order to switch my voice. Use command 'set voice' to do that"
        return text_to_display_voices 
    elif command.lower().startswith("set voice"):
        parts = command.split()
        if  len (parts) != 3:
            return "[INFO]: set voice <1-2>"
        try:
            voice = int(parts[2])
            
            if voice not in VOICES:
                return "Invalid voice number!"
            #global current_voice # from outside
            current_voice = voice 
            return f"[INFO]: Voice changed to {VOICES[voice]}!"
        except ValueError:
            return "[INFO]: Voice number must be an integer!"

    elif command.lower().startswith("info "):
        
        topic = command[5:].strip()
        if topic == "":
            return "[INFO]: Please specify a topic."

        return get_wikipedia_info(topic)
    elif command.lower().startswith("try voice"):
        parts = command.split()
        if len(parts) != 3:
            return "[INFO]: try voice <1-2>"
        try:
            try_voc = int(parts[2])
            if try_voc not in VOICES:
                return "[INFO]: Invalid voice number."
            speak(try_message1, try_voc)
            speak(try_message2, try_voc)
            return f"[INFO]: Tried voice number {try_voc}"
        except ValueError:
            return f"[INFO]: Voice number must be in <1-2>."
    elif command == "help":
        help.show_all_commands()
        help.print_in_history()
        final_message_prompt = help.return_help_prompt()
        final_message_prompt += "[INFO]: Use help <command> for more details."
        print(final_message_prompt)
        return final_message_prompt
    
    elif command.startswith("help "):
        return help.show(command[5: ]) #rest of the command
    elif command.lower() == "joke":
        return jokes.get_joke() # random joke from jokes.py
    else:
        return "[INFO]: Sorry, I don't recognize that command."


#TODO add more features

def print_commands():
    print("Available commands: ")
    print(arrow, "  hello")
    print(arrow, "  how are you")
    print(arrow, "  info <topic>")
    print(arrow, "  voices")
    print(arrow, "  set voice <voice_number>")
    print(arrow, "  try voice <voice_number>") #TO DO
    print(arrow, "  help")
    print(arrow, "  exit")


help_command = False

def main():

    init_history()
    print(bot_icon, "Bot started.")
    print(bar * 60)
    now = datetime.now()
    print(date_icon, "Date:", now.strftime("%d/%m/%Y"))
    print(time_icon, "Time:", now.strftime("%H:%M:%S"))
    print(bar * 60)
    print()
    print_commands()

    while True:

        usr_prompt = usr_icon + " " + "You " + user_arrow + " " 
        command = input(usr_prompt)
        save_message("User", command)

        if command.lower() == "exit" or command.lower() == "quit":

            response = "Goodbye!"
            print(f"{bot_icon} Bot:", response)
            save_message("Bot", response)
            speak(response, current_voice)
            dtnow = datetime.now()
            date = dtnow.strftime("%d/%m/%Y")
            time = dtnow.strftime("%H:%M:%S")
            with open("history.txt", "a") as f:
                f.write(f"{bar * 60}\n")
                f.write(f"{msg_icon}    Chat ended at: {date}, {time}\n")
                #TODO implement total time for the current chat

            break

        if command.lower() == "help":
            global help_command
            help_command = True

        response = process_command(command)
        print(f"{bot_icon} Bot:", response)
        save_message("Bot", response)
        if help_command == True:
            voice_enabled = False
        speak(response, current_voice)
        if help_command == True and voice_enabled == False: #TODO repair the bug
            help_command = False
            voice_enabled = True


if __name__ == "__main__":
    main()