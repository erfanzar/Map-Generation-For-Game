import json
import cv2 as cv
import numpy as np
import os
import numba as nb
from webcolors import name_to_rgb, hex_to_rgb

green = [15, 200, 12]
blue = [200, 5, 5]
yellow = [5, 215, 215]
red = [5, 5, 230]
purple = [230, 10, 180]
white = [220, 220, 220]
cyan = [210, 210, 5]

clr = {
    '#97493a': 'red',
    '#685347': 'brown',
    '#d3636e': 'pink',
    '#7d4b33': 'brighter brown',
    '#b64a19': 'orange',
    '#de9c8e': 'whiter pink'
}


class Cash:
    def __init__(self):
        pass

    def __call__(self, *args, **kwargs):
        return NotImplementedError


@nb.jit(forceobj=True, fastmath=True, nopython=False)
def look_loop(inputs: dict = None, look_for: str = 'level'):
    v = {}
    # range should be used cause numba only support these kinds of loops
    for i in range(len(inputs)):
        if (inputs[i][look_for] if f"{inputs[i][look_for]}" not in clr else clr[f"{inputs[i][look_for]}"]) not in v:
            v[f"{inputs[i][look_for]}"
            # if not f"{inputs[i][look_for]}".startswith('#') else hex_to_name(
            # f"{inputs[i][look_for]}")
            if f"{inputs[i][look_for]}" not in clr else clr[f"{inputs[i][look_for]}"]
            ] = len(v)
    return v


def merge(dict1=None, dict2=None):
    if dict2 is None:
        dict2 = {}
    if dict1 is None:
        dict1 = {}
    result = dict1 | dict2
    return result


def show(array):
    while True:
        cv.imshow('window', array)
        cv.waitKey(1)
        if cv.waitKey(1) == ord('q') or cv.waitKey(1) == 27:
            break


def read_json(path: [os.PathLike, str]) -> dict:
    with open(path, 'r') as r:
        return json.load(r)


def jsn_to_image(name: str = 'res.json', img_size: int = 350):
    with open(name, 'r') as r:
        data = json.load(r)

    frame = np.empty((img_size, img_size, 3)).astype(np.uint8)

    for i in range(len(data)):
        frame[int((data[i]['x']) / 3):int((data[i]['x']) / 3) + 2,
        int((data[i]['y']) / 3):int((data[i]['y']) / 3) + 2] = [130, 50, 255]

    while True:
        cv.imshow('f', frame)
        cv.waitKey(1)
        if cv.waitKey(1) == ord('q'):
            break


def x_y_to_image(x: list = None, y: list = None, img_size: int = 350, prp: int = 1, draw_color_name_hex: str = 'cyan'):
    frame = np.empty((img_size, img_size, 3)).astype(np.uint8)
    color = hex_to_rgb(draw_color_name_hex) if draw_color_name_hex.startswith('#') else name_to_rgb(draw_color_name_hex)
    color = np.array(color)

    for i in range(len(x)):
        frame[int(x[i] / prp):int(x[i] / prp) + 2,
        int(y[i] / prp):int(y[i] / prp) + 2] = color[::-1]

    while True:
        cv.imshow('f', frame)
        cv.waitKey(1)
        if cv.waitKey(1) == ord('q'):
            break


def create_x_y_l_for_data(name: str = 'bg.json', prp: int = 3):
    with open(name, 'r') as r:
        data = json.load(r)
    nna = []
    i = 0
    for dt in data:
        nna.append(
            {
                'id': i,
                'x': int((data[f"{dt}"]['x'] / 3)),
                'y': int((data[f"{dt}"]['y'] / 3)),
                'level': f"{data[f'{dt}']['level']}"
            }
        )
        i += 1
    with open(f'x_y_l_{name}', 'w') as w:
        json.dump(nna, w)


def attar_print(*args, end='\n'):
    print(*(f'\033[1;36m{v}' for v in args), end=end)


def loop_find(inputs: dict = None, looks=None, must: str = None):
    if looks is None:
        looks = ['x', 'y']
    if must is None:
        print("must is None do break")
        exit()
    cs = Cash()
    for look in looks:
        setattr(cs, look, [])
    setattr(cs, 'id', [])
    for inp in inputs:
        if eval(must):
            for look in looks:
                eval(f'cs.{look}.append({inp[look]})')
            eval(f'cs.id.append({inp["id"]})')
    return cs


def set_attar_to_spc(inputs: dict = None, spc_name: str = 'spc',
                     must: str = None, set_a: [str, int] = None):
    """
    :param inputs: dict
    :param spc_name: known prm
    :param must: if stmt
    :param set_a: set when must \n
     inp: is a local that you cant change but must be implemented for must like inp["level"] == "white"
    :return: verified inputs
    """
    if must is None:
        must = 'inp["level"] == "white"'

    for i, inp in enumerate(inputs):
        if eval(must):
            inputs[i][f'{spc_name}'] = set_a
    return inputs


def new_location(inputs: dict = None, prp: [float, int] = 1.5,
                 x: [int, list] = None, y: [int, list] = None, level: str = 'white', usage: str = 'teleports'):
    lc = np.array([x, y]).T
    prp = np.array(prp, dtype=lc.dtype)
    lc -= prp
    last_id = len(inputs) - 1

    for i, loc in enumerate(lc):
        last_id = len(inputs) - 1
        lac = {
            "id": last_id,
            'x': loc[0].tolist(),
            'y': loc[1].tolist(),
            'level': level,
            'usage': usage
        }
        inputs.append(lac)
    return inputs


def save_json(path: [str, os.PathLike] = 'save.json', data: [list, dict] = None):
    with open(path, 'w') as w:
        json.dump(data, w)


def calculate_distance(data: dict = None):
    subway = loop_find(data, looks=['x', 'y', 'id'], must='inp.get("usage") == "subway"')
    teleports = loop_find(data, looks=['x', 'y', 'id'], must='inp.get("usage") == "teleports"')
    festival = loop_find(data, looks=['x', 'y', 'id'], must='inp.get("usage") == "festival"')
    lobby = loop_find(data, looks=['x', 'y', 'id'], must='inp.get("usage") == "lobby"')
    subway_array = np.array([subway.x, subway.y]).T
    teleports_array = np.array([teleports.x, teleports.y]).T
    festival_array = np.array([festival.x, festival.y]).T
    lobby_array = np.array([lobby.x, lobby.y]).T
    subway_mean = [np.mean(ix) for ix in subway_array]
    teleports_mean = [np.mean(ix) for ix in teleports_array]
    festival_mean = [np.mean(ix) for ix in festival_array]
    lobby_mean = [np.mean(ix) for ix in lobby_array]
    min_distance = 0
    max_distance = 290.2
    for i, d in enumerate(data):
        x = d['x']
        y = d['y']
        d_a = np.array([x, y]).T
        d_m = np.mean(d_a) / max_distance
        ls, lt, lf, ll = 110, 110, 110, 110
        lsi, lti, lfi, lli = 0, 0, 0, 0
        for index, s in enumerate(subway_mean):
            cal = abs(d_m - s)
            lsi = index if cal < ls else lsi
            ls = cal if cal < ls else ls

        for index, s in enumerate(teleports_mean):
            cal = abs(d_m - s)
            lti = index if cal < lt else lti
            lt = cal if cal < lt else lt

        for index, s in enumerate(festival_mean):
            cal = abs(d_m - s)
            lfi = index if cal < lf else lfi
            lf = cal if cal < lf else lf

        for index, s in enumerate(lobby_mean):
            cal = abs(d_m - s)
            lli = index if cal < ll else lli
            ll = cal if cal < ll else ll

        data[i]['distance_from_lobby'] = ((lli / max_distance) + d_m) * 100
        data[i]['distance_from_festival'] = ((lfi / max_distance) + d_m) * 100
        data[i]['distance_from_teleports'] = ((lti / max_distance) + d_m) * 100
        data[i]['distance_from_subway'] = ((lsi / max_distance) + d_m) * 100
        # print(((lli / max_distance) + d_m) * 100)
    return data
