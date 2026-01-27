from basic_gsioc import run
from time import sleep

######################
# This code requires a 32-bit distribution of python to work.
# On the Kim Lab Lenovo, this is activated by running
# micromamba activate gsioc-win-32 since the environment is named gsioc-win-32
# ENV = gsioc-win-32
######################

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
