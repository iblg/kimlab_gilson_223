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

    remote_strs = ['remote', 'computer', 'gsioc']
    keypad_strs = ['keypad', 'manual', 'local']
    cmd_str = 'S'
    if mode in remote_strs:
        cmd_str += 'R'
    elif mode in keypad_strs:
        cmd_str += 'K'
    else:
        print('Invalid mode. Valid modes are {}'.format(remote_strs + keypad_strs))
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

def pump(direction: str = 'f', execute: bool = False, unit_id: int = 30):
    """
    Docstring for fire_pump
    
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
    forward_strings = ['f', 'forward', 'clockwise', '>']
    reverse_strings = ['r', 'reverse', 'b', 'backward', 'counterclockwise', '<']
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
    
    cmd_str = 'K'
    if direction in forward_strings:
        cmd_str += '<'
    else:
        cmd_str += '>'
    

    
    if execute:
        run(cmd_str, unit_id=unit_id)
    
    return cmd_str


def stop_pump():
    return 'KH'

def main():
    # Set pump to remote mode
    run(set_pump_to_mode('remote'), unit_id=PUMP_ID)

    # Set pump rpm and direction
    run(set_pump_rpm(20), unit_id=PUMP_ID)
    # run(pump('ccw'))

    run('K<', unit_id=PUMP_ID,)

    # sleep(5)
    # run('V1')
    # sleep(5)
    # run('V0')
    # sleep(20)

    # Stop
    # run('KH', unit_id=PUMP_ID)
    run(stop_pump(), unit_id=PUMP_ID)
    run(set_pump_to_mode('keypad'), unit_id=PUMP_ID)
    return

if __name__ == '__main__':
    main()