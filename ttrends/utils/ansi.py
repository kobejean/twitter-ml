class ANSI:
    '''
    Allows you to do things with ANSI escape sequences.

    EXAMPLE:
        # prints blue text
        print(ANSI.BLUE + "Blue Text" + ANSI.ENDC)
    '''
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    BLACK = '\033[0;30m'
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[0;33m'
    BLUE = '\033[0;34m'
    PURPLE = '\033[0;35m'
    CYAN = '\033[0;36m'
    LIGHT_GREY = '\033[0;37m'
    DARK_GREY = '\033[1;30m'
    BOLD_RED = '\033[1;31m'
    BOLD_GREEN = '\033[1;32m'
    BOLD_YELLOW = '\033[1;33m'
    BOLD_BLUE = '\033[1;34m'
    BOLD_PURPLE = '\033[1;35m'
    BOLD_CYAN = '\033[1;36m'
    WHITE = '\033[1;37m'

if __name__ == "__main__":
    print(ANSI.GREEN + "TEST" + ANSI.ENDC)
    help(ANSI)
