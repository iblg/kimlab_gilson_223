from basic_gsioc import run
from time import sleep

############################################################
# This code requires a 32-bit distribution of python to work.
# On the Kim Lab Lenovo, this is activated by running
# micromamba activate gsioc-win-32 since the environment is named gsioc-win-32
# ENV = gsioc-win-32
############################################################

############################################################
# Note: The unit ID for the pump is 30 by default
############################################################

PUMP_ID = '30 312V3.1.2.0'
PUMP_ID = 30

def set_pump_to_mode(mode: str) -> str:
    mode = mode.lower()

    cmd_str = 'S'
    if mode == 'remote':
        cmd_str += 'R'
    elif mode == 'keyboard' or 'local':
        cmd_str += 'K'
    else:
        print('Invalid mode. Valid modes are \"remote\" or \"keypad\"')
        return None


    return cmd_str

def set_pump_rpm(rpm: float) -> str:
    hundredths = rpm * 100 # set in hundredths of rpm
    cmd_str = 'R{}'.format(int(hundredths))
    return cmd_str

# def run_pump():
    # return

# def read_pump_status():
    # response = run('K', cmd_type='i', unit_id=PUMP_ID)
    # return response

def main():
    run(set_pump_to_mode('remote'), unit_id=PUMP_ID)
    run(set_pump_rpm(10), unit_id=PUMP_ID)
    run('K>', unit_id=PUMP_ID, show_response=True, show_command_sent=True)
    sleep(10)
    run('KH', unit_id=PUMP_ID)
    run(set_pump_to_mode('keypad'), unit_id=PUMP_ID)
    return

if __name__ == '__main__':
    main()