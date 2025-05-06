import os
import re

class WFConsole():

    # Reset.---------------------------------------------------------------------------------------
    RESET = "\033[0m"

    # Regular colors.------------------------------------------------------------------------------
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    # Bright colors.-------------------------------------------------------------------------------
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"

    # Regular backgrounds.-------------------------------------------------------------------------
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"

    # Bright backgrounds.--------------------------------------------------------------------------
    BG_BRIGHT_BLACK = "\033[100m"
    BG_BRIGHT_RED = "\033[101m"
    BG_BRIGHT_GREEN = "\033[102m"
    BG_BRIGHT_YELLOW = "\033[103m"
    BG_BRIGHT_BLUE = "\033[104m"
    BG_BRIGHT_MAGENTA = "\033[105m"
    BG_BRIGHT_CYAN = "\033[106m"
    BG_BRIGHT_WHITE = "\033[107m"

    # Tagged style modifiers.----------------------------------------------------------------------
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    GOOD_TEXT = GREEN
    BAD_TEXT = RED
    WARNING_TEXT = YELLOW
    ACTION_TEXT = CYAN
    INFO_TEXT = MAGENTA
    FUNCTION = BLUE + UNDERLINE
    CLASS = BLUE + UNDERLINE
    KEY = MAGENTA + BG_GREEN

    def __init__(self):
        # Initialize an empty dictionary to store tag mappings.
        tag_map = {}

        # Loop through all attributes defined in the class (not instance).
        for key, value in self.__class__.__dict__.items():
            
            # Only include constants:
            # - Attribute name must be all uppercase (like 'RED', 'BOLD', etc.).
            # - Attribute value must be a string (we're targeting ANSI escape codes).
            if key.isupper() and isinstance(value, str):
                tag_map[key] = value  # Add to the tag map.

        # Assign the resulting dictionary to the instance variable.
        self.TAG_MAP = tag_map

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def fancy_print(self, text):
        def replacer(match):
            closing, tag = match.group(1), match.group(2)
            if closing:
                return self.RESET
            return self.TAG_MAP.get(tag, "")
        
        # Regex for <TAG> and </TAG> format.
        pattern = re.compile(r'<(/?)(\w+)>')
        styled_text = pattern.sub(replacer, text)
        print(styled_text + self.RESET)

    def fancy_input(self, text):
        def replacer(match):
            closing, tag = match.group(1), match.group(2)
            if closing:
                return self.RESET
            return self.TAG_MAP.get(tag, "")
        
        # Regex for <TAG> and </TAG> format.
        pattern = re.compile(r'<(/?)(\w+)>')
        styled_text = pattern.sub(replacer, text)
        return input(styled_text + self.RESET)


if __name__ == "__main__":

    # Create instance of WFConsole.
    console = WFConsole()

    # Clear the console.
    console.clear()
    console.fancy_print("\nthis is <FUNCTION>fancy_print()</FUNCTION>, welcome to <CLASS>WFConsole</CLASS> class test script. we just used <FUNCTION>clear()</FUNCTION> to clear the console.")
    text = f"FYI, layered <RED>f strings</RED> work with <FUNCTION>fancy_print()</FUNCTION> and <FUNCTION>fancy_input()</FUNCTION>!"
    console.fancy_print(f"{text}")
    console.fancy_input("\nthis is <FUNCTION>fancy_input()</FUNCTION>, press <KEY>ENTER</KEY> to continue...")
