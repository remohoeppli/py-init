import time

# fixed time string length
# for formatting purpose
FIXED_TIME_STRING_LENGTH = 14


class Execution_Timer:
    """Timer class to stop script run time"""

    def __init__(self) -> None:
        self.start = time.time()
        self.last_time = self.start

    def get_run_time(self) -> str:
        new_time = time.time()
        time_since_timer_start = str(f"{new_time-self.start:.2f}  [s]")
        time_since_last_time = str(f"+{new_time-self.last_time:.2f}  [s]")
        output = (
            f"{time_since_timer_start.rjust(FIXED_TIME_STRING_LENGTH)}"
            + f"{time_since_last_time.rjust(FIXED_TIME_STRING_LENGTH)}"
        )
        self.last_time = new_time
        return output
