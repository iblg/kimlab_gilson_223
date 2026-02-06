########################################################
# These functions should only be used if you have
# an arrangement of 4x22 racks!
########################################################
from move import move_to_xy

def go_to_well(nx: int, ny: int) -> str:
    """
    Docstring for go_to_well
    Go to well number, numbered by x and y indices.
    1-indexed!
    ***Assumes a 4x22 rack arrangement***
    
    :param nx: Index (starts at 1) of the well in direction along the length 
    of the instrument (i.e. parallel to the instrument body). 
    Each #22 rack has four wells in this direction.
    In the 4x22 rack configuration, 1 <= nx <= 16.
    :type nx: int
    :param ny:   Index (starts at 1) of the well in direction perpendicular to the length 
    of the instrument. 
    Each #22 rack has eleven wells in this direction.
    In the 4x22 rack configuration, 1 <= nx <= 11.
    :type ny: int

    :return: cmd_str, the xy coordinates of the well.
    :rtype: str
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
