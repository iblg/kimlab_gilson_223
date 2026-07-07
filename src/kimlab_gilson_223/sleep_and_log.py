import sys
import ctypes
from ctypes import *
from time import sleep
from datetime import datetime
from kimlab_gilson_223.logging import log_command, save_log_entries

# @log_command
# def sleep_and_log(t):
#     to_log = f'Sleeping for {t} seconds'
#     print(to_log)
#     sleep(t)
#     return to_log

@log_command
def sleep_and_log(t):
    to_log = f'Sleeping for {t} seconds'
    print(to_log)

    bar_length = 40
    interval = 0.1
    steps = int(t / interval)

    for i in range(steps + 1):
        elapsed = i * interval
        progress = elapsed / t
        filled = int(bar_length * progress)
        bar = '█' * filled + '-' * (bar_length - filled)
        percent = progress * 100
        sys.stdout.write(f'\r[{bar}] {percent:.1f}%')
        sys.stdout.flush()
        if i < steps:
            sleep(interval)

    # Ensure we sleep any remaining fractional time
    remainder = t - (steps * interval)
    if remainder > 0:
        sleep(remainder)

    sys.stdout.write('\r[' + '█' * bar_length + '] 100.0%\n')
    sys.stdout.flush()

    return to_log