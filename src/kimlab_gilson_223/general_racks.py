"""
Docstring for general_racks

The Gilson 223 has four spots for racks. 
This generalizes the racks so that new racks can be quickly defined,
and rack layouts can be built so that methods can be more quickly defined.


"""
from basic_gsioc import run
from move import move_to_xy

def get_rack_origin_coords(datatype='list') -> list | dict:
    y = 20
    coords = [
        [4, y], [82, y], [164, y], [242,y]
    ]
    if datatype == 'list' or list:
        return coords
    elif datatype == 'dict' or dict:
        keys = ['1', '2', '3', '4']
        coords = {k: val for k, val in zip(keys, coords)}
        return coords
    else: print('Desired datatype not expected. Please enter \'list\' or \'dict\'')

def rack_22(rack_index: int):
    """
    Docstring for rack_22
    This is the coordinate set for the model 22 rack from Gilson,
    which can be used with IC tubes.
    """
    origin = get_rack_origin_coords()
    origin = origin[rack_index]
    print(origin)
    return

def main():
    # c = get_rack_origin_coords()
    rack0 = rack_22(0)
    return

if __name__ == '__main__':
    main()