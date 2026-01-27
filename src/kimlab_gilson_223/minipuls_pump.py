from basic_gsioc import run
from time import sleep

############################################################
# Note: The unit ID for the pump is 30 by default
############################################################

PUMP_ID = 30

def run_pump():
    return

def read_pump_status():
    response = run('V', cmd_type='i', unit_id=PUMP_ID)
    return response

def main():
    print(read_pump_status())
    return
