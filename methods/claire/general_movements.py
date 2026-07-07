from kimlab_gilson_223.racks_4x22 import go_to_well_increments_along_y
from kimlab_gilson_223.basic_gsioc import run
from kimlab_gilson_223.move import move_to_xy, move_to_z,  move_to_home, move_z_to_top, wait_until_movement_completes, get_z_position
from kimlab_gilson_223.minipuls_pump import set_pump_to_mode, set_pump_rpm, pump, stop_pump
from kimlab_gilson_223.basic_gsioc import immediate
import sys
import signal
from time import sleep

######################################################
# Python documentation for the autosampler can be found at: 
# To run: must open Git Bash and navigate using cd to
#
#   /c/Users/uvcom/dev/kimlab_gilson_223/methods/ 
#
# Activate correct micromamba environment by entering
#
#   micromamba activate micromamba activate gsioc-win-32
#
# Then run 
#
#   python this_file_name.py
######################################################


def main():
    # run(set_pump_to_mode('remote'), unit_id=30)
    # run(move_to_home())
    print(immediate(10,'X'))
    print(immediate(10, 'Z'))
    run(move_to_xy(10,10))
    run(move_to_home())
    # run(wait_until_movement_completes())
    # run(move_z_to_top())
    run(move_to_z(95))
    print(immediate(10, 'X'))
    print(immediate(10, 'Z'))
    # print(get_z_position())
    # run()
    # sleep(10)

    # run(go_to_well_increments_along_y(8))
    # sleep(1)
    # run(move_to_z(180))
    # sleep(180)
    # run(move_to_z(215))
    # sleep(1)
    # run(move_to_home())
    
    return

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Keyboard interrupt!')
        print('Stopping pump and moving to waste position.')
        run(set_pump_to_mode('remote'), unit_id=30)
        run(move_to_home())
        run(stop_pump(), unit_id=30)
        sys.exit(130)
