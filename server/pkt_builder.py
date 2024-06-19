import struct
from typing import List

BUILD_CODES = {
    'HEART_BEAT':                       (0x01, 'heart_beat'), # S <-> C
    'WAYPOINT_MISSION':                 (0x10, 'waypoint_mission'), # S -> C
    'WAYPOINT_MISSION_START':           (0x11, None),
    'WAYPOINT_MISSION_STOP':            (0x12, None),
    # 'BATTERY_LEVEL':                    0x50,
    # 'SIGNAL_LEVEL':                     0x51,
    ################################
    'IS_FLYING':                        (0x61, None),
    'AIRCRAFT_LOCATION':                (0x62, None), 
    'VELOCITY_X':                       (0x63, None), 
    'VELOCITY_Y':                       (0x64, None), 
    'VELOCITY_Z':                       (0x65, None),

    'ATTITUDE_PITCH':                   (0x66, None), 
    'ATTITUDE_YAW':                     (0x67, None), 
    'ATTITUDE_ROLL':                    (0x68, None),
    'FLY_TIME_IN_SECONDS':              (0x69, None),
    ###################################
    'START_TAKEOFF':                    (0x70, None),
    'LANDING_READY':                    (0x71, None),
    'START_LANDING':                    (0x72, None),
}

def build_packet(code_name, *args):
    code, builder_name = BUILD_CODES[code_name]
    builder = globals()[builder_name]
    pkt = builder(*args)
    return code, pkt

################################# data types ########################################
def _build_int32(n:int)->bytes:
    assert isinstance(n, int)
    return struct.pack('>i', n)

def _build_uint32(n:int)->bytes:
    assert isinstance(n, int)
    return struct.pack('>I', n)

def _build_float(n:float)->bytes:
    assert isinstance(n, float)
    return struct.pack('>f', n)

def _build_string(n:str|bytes)->bytes:
    assert isinstance(n, (str, bytes))
    if isinstance(n, str):
        n = n.encode('utf-8')
    size = len(n)
    fmt = f'>I{size}s'
    return struct.pack(fmt, size, n)

def _build_bool(n:bool)->bytes:
    assert isinstance(n, bool)
    return struct.pack('?', n)

def _build_int8(n:int)->bytes:
    assert isinstance(n, int)
    return struct.pack('b', n)

def _build_uint8(n:int)->bytes:
    assert isinstance(n, int)
    return struct.pack('B', n)

##########################################################################

def heart_beat(check: bytes) -> bytes:
    assert len(check) == 4
    return check

################################# mission ##################################
def _build_waypoint_action(action:List)->bytes:
    assert len(action) == 2
    t, p = action
    return _build_uint8(t)+_build_uint8(p)

def _build_waypoint(wp:List)->bytes:
    assert len(wp) == 5
    lat, lng, alt, turn_mode, actions = wp
    r = _build_float(lat)
    r+= _build_float(lng)
    r+= _build_float(alt)
    r+= _build_uint8(turn_mode)
    r+= _build_uint8(len(actions))
    for action in actions:
        r+= _build_waypoint_action(action)
    return r


def waypoint_mission(mission: List) -> bytes:
    '''
    Estrutura do pacote:
    4 bytes (uint32)            -> tamanho da string POI (N)
    N bytes (string)            -> string POI
    4 bytes (float32)           -> auto flight speed
    4 bytes (float32)           -> max flight speed
    1 byte (bool)               -> end on signal lost 
    1 byte (uint8)              -> finished action
    1 byte (uint8)              -> flight path mode
    1 byte (uint8)              -> goto first waypoint mode
    1 byte (uint8)              -> heading mode
    1 byte (bool)               -> gimbal pitch roration enabled
    1 byte (uint8)              -> mission repeats
    1 byte (uint8)              -> waypoints count (M)
        < M vezes >
        4 bytes (float32)       -> latitude
        4 bytes (float32)       -> longitude
        4 bytes (float32)       -> altitude
        1 byte (uint8)          -> turn mode
        1 byte (uint8)          -> waypoint actions count (K)
            < K vezes >
            1 byte (uint8)      -> action type
            1 byte (uint8)      -> action param
    '''
    assert len(mission) == 11
    poi, speed, max_speed, eosl, end_action, fpm, goto_mode, heading, gpre, repeats, waypoints = mission
    r = _build_string(poi)
    r+= _build_float(speed)
    r+= _build_float(max_speed)
    r+= _build_bool(eosl)
    r+= _build_uint8(end_action)
    r+= _build_uint8(fpm)
    r+= _build_uint8(goto_mode)
    r+= _build_uint8(heading)
    r+= _build_bool(gpre)
    r+= _build_uint8(repeats)

    r+= _build_uint8(len(waypoints))
    for wp in waypoints:
        r+= _build_waypoint(wp)
    
    return r

####################################################################################

