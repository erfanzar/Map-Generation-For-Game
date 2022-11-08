import json
import numpy as np
import math
from utils.utils import read_json, clr, look_loop, attar_print, loop_find, x_y_to_image, set_attar_to_spc, new_location, \
    save_json
import numba as nb
from webcolors import hex_to_name


def main():
    data = read_json(path='assets/map-mars.json')
    levels = look_loop(data)
    attar_print(levels)

    # to add subways and lobbies to data
    data = set_attar_to_spc(data, set_a='subway', spc_name='usage', must='inp["level"] == "white"')
    data = set_attar_to_spc(data, set_a='true', spc_name='lobby', must=f'inp["id"] in [2006,2033,2058]')

    # to find specified locations and set new location based ont them for teleport
    teleport_loc = loop_find(inputs=data, looks=['x', 'y'], must='inp["id"] in [227,1942,875,805,59]')
    tp_x, tp_y, tp_id = [teleport_loc.x, teleport_loc.y, teleport_loc.id]

    # adding teleports locations
    data = new_location(
        data, x=tp_x, y=tp_y, prp=1.5, usage='teleports', level='WLocations'
    )
    # teleports added :)

    # show teleport locations
    # teleport_new = loop_find(inputs=data, looks=['x', 'y'], must='inp.get("usage") == "teleports"')
    # llx, lly, _ = [teleport_new.x, teleport_new.y, teleport_new.id]
    # x_y_to_image(llx, lly, draw_color_name_hex='green')

    #
    festival_loc = loop_find(inputs=data, looks=['x', 'y'], must='inp["id"] in [2016,2035,2065]')
    fs_x, fs_y, fs_id = [festival_loc.x, festival_loc.y, festival_loc.id]
    data = new_location(
        data, x=fs_x, y=fs_y, prp=1.5, usage='festival', level='WLocations'
    )
    print(data)
    show_loc = loop_find(inputs=data, looks=['x', 'y'], must='inp.get("level") == "white"')
    llx, lly, _ = [show_loc.x, show_loc.y, show_loc.id]
    x_y_to_image(llx, lly, draw_color_name_hex='green')

    save_json(data=data)


if __name__ == "__main__":
    main()
