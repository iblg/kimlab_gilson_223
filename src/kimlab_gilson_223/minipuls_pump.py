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

def set_pump_to_mode(mode: str, execute: bool = False, unit_id: int = 30) -> str:
    """
    Set pump to either keypad or remote mode
    
    :param mode: The mode you wish to set the pump to. Valid values are 'remote' or 'keypad'.
    :type mode: str

    :param execute: Default False. If False, just returns the string and does not issue the command to the instrument.
    If True, calls a run command to pass the command to the instrument.
    :type execute: bool

    :param unit_id: Unit ID for the pump. By default, it is 30. The Unit ID can be discovered by using the Scan function in GSIOC utility.
    :type unit_id: int

    :return: Returns the command string.
    :rtype: str
    """
    mode = mode.lower()

    cmd_str = 'S'
    if mode == 'remote':
        cmd_str += 'R'
    elif mode == 'keypad':
        cmd_str += 'K'
    else:
        print('Invalid mode. Valid modes are \"remote\" or \"keypad\"')
        return None

    if execute:
        run(cmd_str, unit_id=unit_id)

    return cmd_str


def set_pump_rpm(rpm: float, execute: bool = False, unit_id: int = 30) -> str:
    """
    Docstring for set_pump_rpm
    
    :param rpm: Desired pump speed in revolutions per minute.
    :type rpm: float

    :param execute: Default False. If False, function will return the command string.
    If true, function will issue the command to the instrument.
    :type execute: bool

    :param unit_id: Unit ID for the pump. By default, it is 30. The Unit ID can be discovered by using the Scan function in GSIOC utility.
    :type unit_id: int

    :return: cmd_str, the command string
    :rtype: str
    """
    
    hundredths = rpm * 100 # set in hundredths of rpm
    cmd_str = 'R{}'.format(int(hundredths))
    return cmd_str

def run_pump(direction: str = 'f', execute: bool = False, unit_id: int = 30):
    """
    Docstring for run_pump
    
    :param direction: Direction in which you wish to run the pump. 
    Acceptable values are 
    'f', 'forward', 'cw', 'clockwise', '>' for forward running
    and 
    'r', 'reverse', 'b', 'backward', 'ccw', 'counterclockwise', '<'
    for reverse running
    :type direction: str

    :param execute: Default False. If False, function will return the command string.
    If true, function will issue the command to the instrument.
    :type execute: bool

    :param unit_id: Unit ID for the pump. By default, it is 30. The Unit ID can be discovered by using the Scan function in GSIOC utility.
    :type unit_id: int

    :return: cmd_str, the command string
    :rtype: str
    """
    forward_strings = ['f', 'forward', 'cw', 'clockwise', '>']
    reverse_strings = ['r', 'reverse', 'b', 'backward', 'ccw', 'counterclockwise', '<']
    acceptable_strings = forward_strings + reverse_strings
    def check_direction():
        if direction in acceptable_strings:
            return True
        else:
            print('Direction {} not recognized.'.format(direction))
            print('Valid values are: {}'.format(acceptable_strings))
            return False
    
    if check_direction():
        pass
    else:
        return
    
    cmd_str = 'K' + direction

    
    if execute:
        run(cmd_str, unit_id=unit_id)
    
    return cmd_str

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