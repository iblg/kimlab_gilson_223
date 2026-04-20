from kimlab_gilson_223.shutdown import shutdown
from kimlab_gilson_223.basic_gsioc import run
from kimlab_gilson_223.move import move_to_home, move_to_xy, move_z_to_top, move_to_z, wait_until_movement_completes, go_to_needle_rinse
from kimlab_gilson_223.racks_4x22 import go_to_well_increments_along_y
from kimlab_gilson_223.minipuls_pump import set_pump_to_mode, set_pump_rpm, pump, stop_pump
from kimlab_gilson_223.valve import set_valve
import sys
import signal
from time import sleep

from labjack import ljm

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

def flowmeter_calib_2026_04_06():
    # uses 2026_04_06 calibration of serial number 01842 McMillan 112 flowmeter
    slope = 20.0744
    int = 1.8462

    return int, slope

def convert_volts_to_flow(V):
    int, slope = flowmeter_calib_2026_04_06()
    return int + slope * V

def collect_vial(sampling_time: int, z_sampling=180) -> None:
    """
    Convenience function to increase readability.
    
    :param hplc_sampling_time: Description
    """
    wait_until_movement_completes()
    run(move_to_z(z_sampling))
    run(set_valve('away'))

    sleep(sampling_time)
    run(set_valve('toward'))
    run(move_z_to_top())


def rinse_needle_and_lines(rinsing_time):
    run(set_valve('toward'))
    run(go_to_needle_rinse()[0])
    run(go_to_needle_rinse()[1]) # move z direction
    run(set_valve('away'))
    sleep(rinsing_time)
    print('Rinsing for {} seconds'.format(rinsing_time))
    
    run(set_valve('toward'))
    run(move_z_to_top())
    wait_until_movement_completes()

def collect(current_well: int, sampling_time: float, n_vials=1) -> int:

    # collect one sample
    for i in range(n_vials):
        wait_until_movement_completes()
        run(go_to_well_increments_along_y(current_well)) # this line is basically "Go to next well"
        collect_vial(sampling_time)
        current_well += 1

    return current_well

WASTE_X, WASTE_Y = 1, 1 # coordinates of waste position
PUMP_ID = 30 # Pump ID must be 30. Do not change this value when you send a pump command, or pump will not run!
N_NEEDLES = 1

def main():
    # handle = ljm.openS("ANY", "ANY", "ANY")  # For connecting to labjack device, if desired
    # info = ljm.getHandleInfo(handle) 
    
    #### User-defined parameters
    PUMP_DIRECTION = 'counterclockwise'
    pump_rpm = 48 # rpm of 48 corresponds to about 46 ml/min
    flow_rate = 46./60 # flow rate divided by 60 s
    # sampling_time_per_vial = 10 / flow_rate # time in seconds
    nsamples = 8
    # sampling_time_per_vial = 4.5 
    sampling_time_per_vial = 1
    vials_per_sample = 3
    # time_between_samples = 10*60
    time_between_samples = 3


    print(f'Total samples {nsamples}')
    print(f'Total vials {vials_per_sample*nsamples}')
    print('Time to ten ml:', sampling_time_per_vial)
    line_flush_time = 5
    current_well = 1

    z_sampling = 180 # dispensing z_height
    initial_wait_minutes = 30 # initial wait time, min

    # # Perform user check to ensure all params are satisfactory
    # continue_flag = print_params()
    # if continue_flag.lower() == 'y':
    #     pass
    # else:
    #     print('User aborted the run.')
    #     return
    # run(set_pump_to_mode('remote'), unit_id=PUMP_ID)
    # run(set_pump_rpm(pump_rpm), unit_id=PUMP_ID)
    # run(pump(direction=PUMP_DIRECTION), unit_id=PUMP_ID)

    run(move_to_home())
    wait_until_movement_completes()
    for i in range(nsamples):
        rinse_needle_and_lines(line_flush_time)
        current_well = collect(current_well, sampling_time_per_vial, n_vials=vials_per_sample)
        needle_rinse_str, z_str = go_to_needle_rinse()
        run(needle_rinse_str)
        sleep(time_between_samples)

    run(move_to_home())
    wait_until_movement_completes()
    # run(stop_pump(), unit_id = PUMP_ID)

    print('End')

    return

    
if __name__ == '__main__':
    main()
    # try:
    #     main()
    # except TypeError as te:
    #     print('TypeError', te)
    # except KeyboardInterrupt as ke:
    #     print(ke)
    # except UnboundLocalError as ue:
    #     print(ue)
    # finally:
    #     print('Shutting down pump and homing instrument')
    #     shutdown()
        
