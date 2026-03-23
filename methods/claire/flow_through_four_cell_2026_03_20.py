from kimlab_gilson_223.basic_gsioc import run
from kimlab_gilson_223.move import move_to_home, move_to_xy, move_z_to_top, move_to_z
from kimlab_gilson_223.racks_4x22 import go_to_well_increments_along_y
from kimlab_gilson_223.minipuls_pump import set_pump_to_mode, set_pump_rpm, pump, stop_pump
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

PUMP_ID = 30 # Pump ID must be 30. Do not change this value when you send a pump command, or pump will not run!
WASTE_X, WASTE_Y = 1, 1 # coordinates of waste position
PUMP_DIRECTION = 'counterclockwise'


z_sampling = 180 # dispensing z_height

initial_wait_minutes = 0.06 # initial wait time, min
initial_wait = 60*initial_wait_minutes
wait_times_hours = [12, 12] # the number of hours to wait before sampling. Should add to 24.

pump_rpm = 15 # pump revolutions per minute
tube_diameter = 0.5 # in mmcurren

hplc_volume = 0.2 # required volumes for sampling
icp_ms_volume = 2
toc_half_volume = 10

n_days = 10

def calculate_t_to_dispense_mL(vol: float, rpm: float, tube_diameter=0.5):
    print(f'Calculating time to dispense {vol} mL of fluid at {rpm} rpm with Gilson-manufactured tube diameter {tube_diameter} mm.')

    if 5 <= rpm <= 15:
        pass
    else:
        print('This function only works between 5 and 15 rpm.')
        print(f'You provided {rpm} rpm.')
        return None
    
    p1 = (5, 0.189) # rpm, mL/min according to Gilson table
    p2 = (15, 0.558)
    slope = (p2[1] - p1[1])/(p2[0] - p1[0])

    flow_rate = p1[1] + slope * (rpm - p1[0])
    flow_rate = flow_rate / 60 # convert to mL/sec from mL/min
    collection_time = vol/flow_rate
    return collection_time

hplc_sampling_time = calculate_t_to_dispense_mL(hplc_volume, pump_rpm)
icp_ms_sampling_time = calculate_t_to_dispense_mL(icp_ms_volume, pump_rpm)
toc_sampling_time = calculate_t_to_dispense_mL(toc_half_volume, pump_rpm)

def move_to_waste(x: int, y: int) -> str:
    cmd_str = move_to_xy(x, y)
    return cmd_str

def custom_handler(signum, frame):
    print("Interrupt received! Performing custom shutdown...")
    run(move_to_home())
    run(stop_pump())
    sys.exit(130)

def collect_hplc(hplc_sampling_time: int = hplc_sampling_time) -> None:
    """
    Convenience function to increase readability.
    
    :param hplc_sampling_time: Description
    """
    run(move_to_z(z_sampling))

    sleep(hplc_sampling_time)
    run(move_z_to_top())

def collect_icp_ms(icp_ms_sampling_time: int = icp_ms_sampling_time) -> None:
    """
    Convenience function to increase readability.
    
    :param icp_ms_sampling_time: Description
    """
    run(move_to_z(z_sampling))
    sleep(icp_ms_sampling_time)
    run(move_z_to_top())

def collect_toc(toc_sampling_time: int = toc_sampling_time) -> None:
    """
    Convenience function to increase readability.
    
    :param toc_sampling_time: Description
    """
    run(move_to_z(z_sampling))
    sleep(toc_sampling_time)
    run(move_z_to_top())

def collect(current_well: int) -> int:
    # collect one set of samples. In this case, one sample is hplc, followed by 
    # ICPMS
    # TOC. TOC is collected in two vials
    run(go_to_well_increments_along_y(current_well)) # this line is basically "Go to next well"
    collect_hplc()
    current_well += 1
    run(go_to_well_increments_along_y(current_well))
    collect_icp_ms()
    current_well += 1
    run(go_to_well_increments_along_y(current_well))
    collect_toc() # toc is collected in two vials, so collect_toc_will automatically do this
    current_well += 1
    run(go_to_well_increments_along_y(current_well))
    collect_toc()
    current_well += 1
    return current_well

def sampling_24h(current_well, wait_times_hours=[12,12]):
    for i in wait_times_hours:
        sleep_time = 3600 * i # convert to seconds
        print('Sleeping for {i} hours.')
        sleep(sleep_time)
        current_well = collect(current_well)

    return current_well

def main():
    current_well = 1

    run(set_pump_to_mode('remote'), unit_id=PUMP_ID)
    # run(move_to_home())
    run(move_to_xy(100,100))

    # run(move_to_waste(WASTE_X, WASTE_Y))
    run(set_pump_rpm(pump_rpm), unit_id=PUMP_ID)
    run(pump(direction=PUMP_DIRECTION), unit_id=PUMP_ID)
    sleep(10)

    # sleep(initial_wait)
    # current_well = collect(current_well=current_well) # collect initial samples

    # # for day in range(n_days):
    # #     current_well = sampling_24h(current_well, wait_times_hours=wait_times_hours) # make sure to update the current well, or it will not increase

    # run(move_to_waste(WASTE_X, WASTE_Y))
    run(stop_pump(), unit_id=PUMP_ID)
    print('End')


    return

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Keyboard interrupt!')
        print('Stopping pump and moving to waste position.')
        run(set_pump_to_mode('remote'), unit_id=PUMP_ID)
        run(move_to_waste(WASTE_X, WASTE_Y))
        run(stop_pump(), unit_id=PUMP_ID)
        sys.exit(130)
