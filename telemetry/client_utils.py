import struct
import datetime
import os

from . import config

class double:
    pass

KEYS = {
    1: ([double, double, float], ["latitude", "longitude", "altitude"], "LOCATION"),
    2: ([double], ["attitude_yaw"], "YAW"),
    3: ([double], ["attitude_roll"], "ROLL"),
    4: ([double], ["attitude_pitch"], "PITCH"),

    5: ([double], ["velocity_x"], "VELOCITY_X"),
    6: ([double], ["velocity_y"], "VELOCITY_Y"),
    7: ([double], ["velocity_z"], "VELOCITY_Z"),

    8: ([int], ["fly_time_seconds"], "FLY_TIME"),

    9: ([double, double, double], ["gimbal_attitude_yaw", "gimbal_attitude_roll", "gimbal_attitude_pitch"], "GIMBAL_ATTITUDE"),
}

def read_n(skt, n):
    b = b''
    for i in range(n):
        b+=skt.recv(1)
    return b

def read_int(skt):
    b = read_n(skt, 4)
    return struct.unpack('>i', b)[0]

def read_byte(skt):
    return struct.unpack('>b', skt.recv(1))[0]

def read_double(skt):
    b = read_n(skt, 8)
    return struct.unpack('>d', b)[0]

def read_float(skt):
    b = read_n(skt, 4)
    return struct.unpack('>f', b)[0]


DATA_TYPES = {
    double: (read_double, 8),
    float: (read_float, 4),
    int: (read_int, 4),
}

GLOBAL_DATA = {}
for _,_,name in KEYS.values():
    GLOBAL_DATA[name] = None

def get_key_data(skt, data_types, data_names, key_name):
    total_size = 0
    final = {
        'key_name': key_name,
        'data': {},
    }
    for data_type, data_name in zip(data_types,data_names):
        func, length = DATA_TYPES[data_type]
        data = func(skt)
        total_size+=length
        final['data'][data_name] = data
    return final, total_size

def save_state():
    state = []
    for i in GLOBAL_DATA.values():
        state.extend(i.values())
    path = config.DATA_FILEPATH
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as file:
            file.write("TIMESTAMP|LOCATION|ATTITUDE|VELOCITY|FLY_TIME|GIMBAL_ATTITUDE\n")
            file.close()
    with open(path, "a+") as file:
        text = "{}|{} {} {}|{} {} {}|{} {} {}|{}|{} {} {}\n".format(datetime.datetime.now(), *state)
        file.write(text)
        file.close()
    
    return state

def get_data(skt):
    global GLOBAL_DATA
    data_size = read_int(skt)
    if data_size == 0: 
        return 
        
    count = 0
    while count < data_size:
        key = read_byte(skt)
        assert key in KEYS, str(key)+" is not a valid key"

        data_types, data_names, key_name = KEYS[key]
        data, size = get_key_data(skt,  data_types, data_names, key_name)
        
        count+=size+1
        GLOBAL_DATA[data["key_name"]] = data["data"]
