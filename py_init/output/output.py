from py_init.output.shellcolors import colors
from py_init.output.execution_timer import Execution_Timer


# fixed message string length
# for formatting purpose
FIXED_MESSAGE_STRING_LENGTH = 60


class Output:
    def __init__(self) -> None:
        self.timer = Execution_Timer()

    def started(self, message: str) -> None:
        print(f" {colors.fg.green}  started {colors.reset}   {message}", end="\r")

    def passed(self, message: str) -> None:
        print(
            f" {colors.bg.green}{colors.fg.black} ✔ passed {colors.reset}"
            + f"   {message.ljust(FIXED_MESSAGE_STRING_LENGTH)}   "
            + f"{colors.fg.blue}{self.timer.get_run_time()}{colors.reset}"
        )

    def failed(self, message: str) -> None:
        print(f" {colors.bg.red}{colors.fg.white} ✘ failed {colors.reset}   {message}")

    def info(self, message: str) -> None:
        print(
            f" {colors.bg.orange}{colors.fg.black} ℹ info   {colors.reset}   {message}"
        )

