from enum import Enum


class ANSI(Enum):
    RESET = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    DARK_GRAY = "\033[37m"
    DIM_WHITE = "\033[90m"
