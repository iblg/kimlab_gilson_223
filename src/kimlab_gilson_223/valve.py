from basic_gsioc import run
from minipuls_pump import pump, set_pump_rpm, set_pump_to_mode, stop_pump
from time import sleep
from logging import log_command, save_log_entries
from datetime import datetime

@log_command
def set_valve(direction: str | int, execute: bool = False, unit_id: int = 10):
    """
    Sets the Gilson diverting valve to either its position 0, away from the instrument, or 1, towards the instrument.
    
    
    :param direction: Indicates the direction to set the valve to. Possible values are 0, 'away', or 'waste' to set the valve
    to the port marked 0; or 1, 'toward', or 'needle' to the port marked 1.
    Most typical setup is that the port toward the instrument (port 1) is the needle direction. However, this is imprecise, and using 
    'needle' or 'waste' will print a warning.
    :type direction: str | int

    :param execute: If True, send command to instrument. Default False.
    :type execute: bool

    :param unit_id: Unit ID. Default is 10 for the 223 instrument.
    :type unit_id: int
    """

    zero_directions = [0, 'away', 'waste']
    one_directions = [1, 'toward', 'needle']
    acceptable_directions = zero_directions + one_directions

    def check_acceptable_directions():
        if direction in acceptable_directions:
            return True
        else:
            print('Direction {} not valid'.format(direction))
            print('Please provide one of {}'.format(acceptable_directions))
            return False
        
    if check_acceptable_directions():
        pass
    else:
        return
    
    def suggest_precise_language():
        if direction in ['waste', 'needle']:
            print('Warning: Setting direction with waste and needle is imprecise.')
            print('Waste and needle can be connected arbitrarily to either port.')
            print('Suggest using 0 and 1 or \'away\' and \'toward\' to indicate port facing away from or toward the autosampler body.')
            print('Continuing.')
        return
    suggest_precise_language()


    if direction in zero_directions:
        cmd_str = 'V0'
    elif direction in one_directions:
        cmd_str = 'V1'

    if execute:
        run(cmd_str, unit_id=unit_id)

    return cmd_str

def main():
    # log_entries = []
    now = datetime.now()

    # path_to_file = Path('~/OneDrive/Desktop/gilson223_logs')
    filename = now.strftime("%Y-%m-%d_%H-%M-%S") + '.csv'
    path_to_file = 'C:/Users/uvcom/OneDrive/Desktop/gilson223_logs/' + filename


    sleep_time = 3
    PUMP_ID = 30
    run(set_pump_to_mode('remote'), unit_id=PUMP_ID)
    run(set_pump_rpm(20), unit_id=PUMP_ID)
    run(pump('f'), unit_id=30)
    run(set_valve('away'))
    run(set_valve(0))
    sleep(sleep_time)
    run(set_valve('toward'))
    sleep(sleep_time)
    run('KH', unit_id=PUMP_ID)
    run(set_pump_to_mode('manual'))
    save_log_entries()
    
    return

if __name__ == '__main__':
    main()