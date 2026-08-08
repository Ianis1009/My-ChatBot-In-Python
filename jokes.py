import random

JOKES = [

    "Why do programmers prefer dark mode? "
    "Because light attracts bugs.",

    "Why do programmers confuse Halloween "
    "and Christmas? "
    "Because OCT 31 equals DEC 25.",

    "What do programmers do when they are hungry? "
    "They grab a byte.",

    "Why was the computer cold? "
    "Because it left its Windows open.",

    "Why did the Python programmer wear glasses? "
    "Because they could not C.",

    "Why was the developer broke? "
    "Because they used up all their cache.",

    "What is a programmer's favorite type of music? "
    "Algorithm and blues.",

    "Why did the developer go outside? "
    "To check whether the cloud was working."

    "Why did the computer get promoted? "
    "It had outstanding processing skills."

    "I told my computer I needed a break. "
    "Now it won't stop sending me vacation ads."

    "Why did the function break up with the variable? "
    "It needed some space."


] #TODO add more

def get_joke():
    return random.choice(JOKES)