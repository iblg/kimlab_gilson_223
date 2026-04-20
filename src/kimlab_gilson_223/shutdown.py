from kimlab_gilson_223.minipuls_pump import set_pump_to_mode, stop_pump
from kimlab_gilson_223.move import move_to_home, wait_until_movement_completes
from kimlab_gilson_223.basic_gsioc import run
import sys

def shutdown():
        print('Stopping pump and moving to waste position.')
        run(set_pump_to_mode('remote'), unit_id=30)
        run(stop_pump(), unit_id=30)
        run(set_pump_to_mode('keypad'), unit_id=30)        
        run(move_to_home())
        wait_until_movement_completes()


        sys.exit(130)