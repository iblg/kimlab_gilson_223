from kimlab_gilson_223.basic_gsioc import run
from kimlab_gilson_223.move import move_to_home, move_to_xy, move_z_to_top, move_to_z, wait_until_movement_completes
from kimlab_gilson_223.racks_4x22 import go_to_well_increments_along_y, zigzag_increments_along_y, go_to_well_nx_ny
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

###################################################
# These are not needed unless you are determining flow rate using calculate_t_to_dispense_mL
# pump_rpm = 15 # pump revolutions per minute
# tube_diameter = 0.5 # in mmcurren

# hplc_volume = 0.2 # required volumes for sampling
# icp_ms_volume = 2
# toc_half_volume = 10
###################################################



# def calculate_t_to_dispense_mL(vol: float, rpm: float, tube_diameter=0.5):
#     print(f'Calculating time to dispense {vol} mL of fluid at {rpm} rpm with Gilson-manufactured tube diameter {tube_diameter} mm.')

#     if 5 <= rpm <= 15:
#         pass
#     else:
#         print('This function only works between 5 and 15 rpm.')
#         print(f'You provided {rpm} rpm.')
#         return None
    
#     p1 = (5, 0.189) # rpm, mL/min according to Gilson table
#     p2 = (15, 0.558)
#     slope = (p2[1] - p1[1])/(p2[0] - p1[0])

#     flow_rate = p1[1] + slope * (rpm - p1[0])
#     flow_rate = flow_rate / 60 # convert to mL/sec from mL/min
#     collection_time = vol/flow_rate
#     return collection_time

# hplc_sampling_time = calculate_t_to_dispense_mL(hplc_volume, pump_rpm)
# icp_ms_sampling_time = calculate_t_to_dispense_mL(icp_ms_volume, pump_rpm)
# toc_sampling_time = calculate_t_to_dispense_mL(toc_half_volume, pump_rpm)
# sampling_time = hplc_sampling_time 


def move_to_waste(x: int, y: int) -> str:
    cmd_str = move_to_xy(x, y)
    return cmd_str

def collect_hplc(hplc_sampling_time: int, z_sampling=180) -> None:
    """
    Convenience function to increase readability.
    
    :param hplc_sampling_time: Description
    """
    run(move_to_z(z_sampling))

    sleep(hplc_sampling_time)
    run(move_z_to_top())

def collect_icp_ms(icp_ms_sampling_time, z_sampling=180) -> None:
    """
    Convenience function to increase readability.
    
    :param icp_ms_sampling_time: Description
    """
    run(move_to_z(z_sampling))
    sleep(icp_ms_sampling_time)
    run(move_z_to_top())

def collect_toc(toc_sampling_time: int, z_sampling=180) -> None:
    """
    Convenience function to increase readability.
    
    :param toc_sampling_time: Description
    """
    run(move_to_z(z_sampling))
    sleep(toc_sampling_time)
    run(move_z_to_top())

def collect(current_well: int, hplc_sampling_time, icp_ms_sampling_time, toc_sampling_time) -> int:
    # collect one set of samples. In this case, one sample is hplc, followed by 
    # ICPMS
    # TOC. TOC is collected in two vials
    print(f'Current well is {current_well}')
    run(go_to_well_increments_along_y(current_well)) # this line is basically "Go to next well"
    sleep(0.5)
    collect_hplc(hplc_sampling_time)
    current_well += 1

    print(f'Current well is {current_well}')
    run(go_to_well_increments_along_y(current_well))
    sleep(0.5)
    collect_icp_ms(icp_ms_sampling_time)
    current_well += 1

    print(f'Current well is {current_well}')
    run(go_to_well_increments_along_y(current_well))
    sleep(0.5)
    collect_toc(toc_sampling_time) # toc is collected in two vials, so collect_toc_will automatically do this
    current_well += 1
    
    print(f'Current well is {current_well}')
    run(go_to_well_increments_along_y(current_well))
    sleep(0.5)
    collect_toc(toc_sampling_time)
    current_well += 1
    return current_well

def sampling_24h(current_well, hplc_sampling_time, icp_ms_sampling_time, toc_sampling_time, wait_times_hours=[12,12]):
    for i in wait_times_hours:
        sleep_time = 3600 * i # convert to seconds
        print(f'Sleeping for {i} hours.')
        sleep(sleep_time)
        run(go_to_well_increments_along_y(current_well))
        current_well = collect(current_well, hplc_sampling_time, icp_ms_sampling_time, toc_sampling_time)
        run(move_to_xy(0,0))
    current_well = 1

    return current_well

def print_params():
    print(50*'#')
    print(f'Pump ID: {PUMP_ID}')
    print(f'Waste location set to: ({WASTE_X},{WASTE_Y})')
    print(f'Pump direction: {PUMP_DIRECTION}')
    print(f'Number of days to run: {n_days}')
    print(f'Initial wait in minutes: {initial_wait_minutes}')
    print(f'Number of samples per day: {n_samples_per_day}')
    print(f'HPLC sampling time (seconds): {hplc_sampling_time}')
    print(f'ICP-MS sampling time (seconds): {icp_ms_sampling_time}')
    print(f'TOC sampling time (per vial, seconds): {toc_sampling_time}')
    print(f'Total time per sample (seconds): {total_time_per_sample}')
    print(f'Steady state wait time between sample (hours): {wait_time_seconds/3600}')
    print(f'24h sampling schedule: {wait_times_hours}')
    print(f'Estimated time of run (days): {estimated_runtime}')
    print(f'Top z height: 215')
    print(f'z height for sampling: {z_sampling}')
    print(50*'#')
    continue_flag = input('DO YOU WANT TO CONTINUE? (y/n)')
    return continue_flag

WASTE_X, WASTE_Y = 1, 1 # coordinates of waste position
PUMP_ID = 30 # Pump ID must be 30. Do not change this value when you send a pump command, or pump will not run!

def main():
    #### User-defined parameters
    PUMP_DIRECTION = 'counterclockwise'
    PUMP_RPM = 10
    z_sampling = 180 # dispensing z_height
    initial_wait_minutes = 30 # initial wait time, min
    
    # hplc_sampling_time = 225
    # icp_ms_sampling_time = 3000
    # toc_sampling_time = 2250 # TOC time per one IC vial, so time to dispense 10 mL
    current_well = 1


    #### For testing
    hplc_sampling_time = 225
    icp_ms_sampling_time = 3000
    toc_sampling_time = 2250 # TOC time per one IC vial, so time to dispense 10 mL
    wait_times_hours = [2/3600, 2/3600] #only uncomment this for testing


    ###### Derived variables
    # initial_wait = 60*initial_wait_minutes
    # total_time_per_sample = hplc_sampling_time + icp_ms_sampling_time + 2*toc_sampling_time
    # wait_time_seconds = (24 * 60 * 60 - n_samples_per_day * total_time_per_sample ) / n_samples_per_day
    # wait_times_hours = [wait_time_seconds/3600 for i in range(n_samples_per_day)]
    # estimated_runtime = (n_days * 24 * 3600 + initial_wait) / (24 * 3600)

    # # Perform user check to ensure all params are satisfactory
    # continue_flag = print_params()
    # if continue_flag.lower() == 'y':
    #     pass
    # else:
    #     print('User aborted the run.')
    #     return
    
    run(move_to_home())
    wait_until_movement_completes()
    run(move_to_waste(WASTE_X, WASTE_Y))
    wait_until_movement_completes()


    nwells = 15
    for i in range(1, nwells + 1):

        run(zigzag_increments_along_y(i, n_needles=2))
        wait_until_movement_completes()

        sleep(1)
    run(move_to_home())
    wait_until_movement_completes()


    # run(set_pump_to_mode('remote'), unit_id=PUMP_ID)
    # run(set_pump_rpm(pump_rpm), unit_id=PUMP_ID)
    # run(pump(direction=PUMP_DIRECTION), unit_id=PUMP_ID)

    # sleep(initial_wait)
    # current_well = collect(current_well, hplc_sampling_time, icp_ms_sampling_time, toc_sampling_time) # collect initial samples
    # run(move_to_waste(WASTE_X, WASTE_Y))
    # current_well = 1

    # for day in range(n_days):
    #     current_well = sampling_24h(current_well,  hplc_sampling_time, icp_ms_sampling_time, toc_sampling_time, wait_times_hours=wait_times_hours) # make sure to update the current well, or it will not increase

    # run(move_to_waste(WASTE_X, WASTE_Y))
    # run(stop_pump(), unit_id=PUMP_ID)
    # print('End')

    return

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Keyboard interrupt!')
        print('Stopping pump and moving to waste position.')
        run(set_pump_to_mode('remote'), unit_id=30)
        run(move_to_waste(WASTE_X, WASTE_Y))
        run(stop_pump(), unit_id=PUMP_ID)
        sys.exit(130)
