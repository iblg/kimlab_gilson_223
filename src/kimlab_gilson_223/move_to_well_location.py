from basic_gsioc import run
from time import sleep
######################
# This code requires a 32-bit distribution of python to work.
# On the Kim Lab Lenovo, this is activated by running
# micromamba activate gsioc-win-32 since the environment is named gsioc-win-32
# ENV = gsioc-win-32
######################

# @log_command
def get_motor_statuses():
    status = run('M', cmd_type='i')
    return status

# @log_command
def move_to_xy(x: int, y: int, move_z_to_top_before_running: bool = True) -> str:
    """
    x: desired x location, in mm
    y: desired y location, in mm
    """
    x_lims = (0, 315) # these are the apparent limits on x and y. You can override them at your peril.
    y_lims = (0, 236)

    # check x values
    if x > x_lims[1]:
        print('x needs to be between {} and {}'.format(x_lims[0], x_lims[1]))
        print('You provided {}'.format(x))
        return
    elif x < x_lims[0]:
        print('x needs to be between {} and {}'.format(x_lims[0], x_lims[1]))
        print('You provided {}'.format(x))
        return
    else:
        pass
    
    # check y values
    if y > y_lims[1]:
        print('y needs to be between {} and {}'.format(y_lims[0], y_lims[1]))
        print('You provided {}'.format(x))
        return
    elif y < y_lims[0]:
        print('y needs to be between {} and {}'.format(y_lims[0], y_lims[1]))
        print('You provided {}'.format(x))
        return
    else:
        pass    

    if move_z_to_top_before_running:
        run(move_z_to_top()) # move z to top before moving xy to prevent crashes
    
    if x == 0: # handle edge case
        x = '000'
    
    if y == 0:
        y = '000'

    cmd_string = 'X' + str(x) + '0/' + str(y) + '0' # convert into tenths of millimeters (hence the extra zeros) and return the string.
    return cmd_string

# @log_command
def move_z_to_top() -> str:
    return 'Z2150' # 2150 tenths of mm is the top z height

# @log_command
def get_z_position() -> int:
    """
    Gets z position in mm
    """
    z = run('Z', cmd_type='i', show_response=True, sleep_before=5)
    z = z.strip()
    z = int(float(z)/ 10)
    return z

# @log_command
def get_xy_position() -> tuple[int, int]:
    """
    Gets x,y position in mm. Returns as a tuple.
    """
    x = run('X', cmd_type='i')
    x = x.strip()
    y = x.split(b'/')[1]
    x = x.split(b'/')[0]

    x = int(float(x)/10)
    y = int(float(y)/10)
    return (x,y)

# @log_command
def move_to_z(z: int, speed: int = 4) -> int:
    """
    z: int
    Desired z height in mm. Must be between 92 and 215. 215 = highest. 95 = lowest

    speed: int
    Speed setting (1=slowest, 5=fastest. Default = 4.)
    """

    if speed in (1,2,3,4,5): # Check speed setting for validity
        pass
    else:
        print('Wrong speed provided! Valid speeds are one of 1 = slowest, 2, 3, 4, 5 = fastest')
        return

    if z < 92:
        print('z must be between 92 and 215!')
        return
    elif z > 215:
        print('z must be between 92 and 215!')
        return
    else:
        cmd_string = 'Z' + str(z) + '0,' + str(speed)
        return cmd_string
    

# @log_command
def move_to_home() -> str:
    '''
    Convenience function to replace the less clear "H" function.
    '''

    return 'H'

# @log_command
def wait_until_movement_completes(sleep_time: float = 0.1) -> None:
    """
    Queries the current status of the motors. If any of them are running, sleeps for sleep_time seconds.
    """
    while(b'R' in get_motor_statuses()):
        sleep(sleep_time)
    return


# @log_command
def go_to_well(nx: int, ny: int) -> str:
    """
    Go to well, numbered by x and y indices.
    1-indexed!
    ***Assumes a 4x22 rack arrangement***

    """
    def check_nx():
        nx_lims = (1, 16)
        if nx >= nx_lims[0] and nx <= nx_lims[1]:
            return True
        else:
            return False
    
    def check_ny():
        ny_lims = (1, 11)
        if ny >= ny_lims[0] and ny <= ny_lims[1]:
            return True
        else:
            return False
    
    def get_x_from_index(idx):
        nx0 = 1
        nx1 = 16
        x0 = 14
        x1 = 315
        slope = (x1-x0) / (nx1-nx0)
        x = slope * (idx - nx0) + x0
        return x
    
    def get_y_from_index(idx):
        ny0 = 1
        ny1 = 11
        y0 = 38
        y1 = 234
        slope = (y1-y0) / (ny1-ny0)
        y = slope * (idx - ny0) + y0
        return y

    if check_nx():
        pass
    else:
        return
    
    if check_ny():
        pass
    else:
        return
    
    x = int(get_x_from_index(nx))
    y = int(get_y_from_index(ny))

    cmd_string = move_to_xy(x,y)
    return cmd_string

# @log_command
def go_to_drain(execute: bool = False) -> tuple[str, str]:

    cmd_str = move_to_xy(68,2)
    z_str = move_to_z(195)

    if execute:
        run(cmd_str)
        wait_until_movement_completes()
        run(z_str)

    return cmd_str, z_str

# @log_command
def go_to_needle_rinse(z_height=135, execute: bool = False) -> tuple[str, str]:
    cmd_str = move_to_xy(83,2)
    if z_height == 'top':
        z_str = move_to_z(215, speed=2)
    z_str = move_to_z(z_height, speed=2)
    if execute:
        run(cmd_str)
        wait_until_movement_completes()
        run(z_str)
    return cmd_str, z_str


def main():
    run(move_to_home())
    # run('H')
    wait_until_movement_completes()
    run(go_to_needle_rinse())
    wait_until_movement_completes()

    run(move_to_home())
    wait_until_movement_completes()

    # save_log_entries()

    return

if __name__ == '__main__':
    main()