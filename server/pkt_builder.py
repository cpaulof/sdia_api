import struct
from typing import List


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
    
def heart_beat(check: bytes) -> bytes:
    assert len(check) == 4
    return check

############################################################################# mission
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

