import struct
from typing import List


BUILD_CODES = {
    'HEART_BEAT':                       (0x01, 'heart_beat'), # S <-> C
    'WAYPOINT_MISSION':                 (0x10, 'waypoint_mission'), # S -> C
    'WAYPOINT_MISSION_START':           (0x11, 'no_data_cmd'),
    'WAYPOINT_MISSION_STOP':            (0x12, 'no_data_cmd'),
    'WAYPOINT_MISSION_STATUS':          (0x13, None),
    'WAYPOINT_MISSION_EXECUTION_STATUS':(0x14, None),
    'WAYPOINT_MISSION_UPLOAD_RESULT':   (0x15, None),
    'WAYPOINT_MISSION_PAUSE':           (0x16, None),
    'WAYPOINT_MISSION_RESUME':          (0x17, None),
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

def _build_double(n:float)->bytes:
    assert isinstance(n, float)
    return struct.pack('>d', n)

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
def no_data_cmd(*args):
    return b''

def heart_beat(check: bytes) -> bytes:
    assert len(check) == 4
    return check

################################# mission ##################################
def _build_waypoint_action(action:List)->bytes:
    assert len(action) == 2
    t, p = action
    #print(action)
    return _build_uint8(t)+_build_int32(p) # param is not uint8 since Type Gimbal Pitch accepts param between -180 to +180

def _build_waypoint(wp:List)->bytes:
    assert len(wp) == 5
    lat, lng, alt, turn_mode, actions = wp
    r = _build_double(lat)
    r+= _build_double(lng)
    r+= _build_float(alt)
    r+= _build_uint8(turn_mode)
    r+= _build_uint8(len(actions))
    for action in actions:
        r+= _build_waypoint_action(action)
    return r


def waypoint_mission(mission) -> bytes:
    '''
    Estrutura do pacote:
    # 4 bytes (uint32)          -> tamanho da string POI (N)
    # N bytes (string)          -> string POI
    8 bytes (float64)           -> poi_lat
    8 bytes (float64)           -> poi_lng
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
        8 bytes (float64)       -> latitude
        8 bytes (float64)       -> longitude
        4 bytes (float32)       -> altitude
        1 byte (uint8)          -> turn mode
        1 byte (uint8)          -> waypoint actions count (K)
            < K vezes >
            1 byte (uint8)      -> action type
            4 byte (int32)      -> action param
    '''
    mission_list = parse_mission(mission)
    assert len(mission_list) == 11
    poi, speed, max_speed, eosl, end_action, fpm, goto_mode, heading, gpre, repeats, waypoints = mission_list
    poi_lat, poi_lng = [float(i) for i in poi.split(':')]
    #r = _build_string(poi)
    r = _build_double(poi_lat)
    r+= _build_double(poi_lng)
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

def parse_mission(mission):
    '''preparar um objeto WaypointMission para ser convertido
       para um byte array posteriormente.
       
--------------------------------------------------------------------------------------------------------
       O envio de uma missão ocorre apenas do servidor->cliente.

       O envio de uma missao para o drone implica que este
       deve registrar e carregar a missao.

       O fluxo básico de envio de missao até o ponto de estar pronto 
       para execução é:
            Envio -> Recebimento pelo Cliente -> Registro -> Uploading -> Pronto para Execução.

       O retorno de volta para o servidor indicara o sucesso 
       ou falha da operação que pode ser:
            SUCCESS
                Missão foi enviada, registrada, feito upload e está pronto para execução.

            REGISTER_FAILED
                O registro da missão falhou já na etapa inicial, possível causa é parametros da missão 
                estarem mal configurados.

            UPLOADING_FAILED
                O registro da missão foi bem sucedido porém falhou ao carrega-lá no drone. A principal causa 
                é o drone não está pronto para carregar a missão.
       '''
    poi = mission.point_of_interest
    auto_flight_speed = mission.auto_flight_speed
    max_flight_speed = mission.max_flight_speed
    exit_on_signal_lost = mission.exit_on_signal_lost
    finished_action = mission.finished_action.value
    flight_path_mode = mission.flight_path_mode.value
    goto_first_waypoint_mode = mission.goto_first_waypoint_mode.value
    heading_mode = mission.heading_mode.value
    gimbal_pitch_rotation_enabled = mission.gimbal_pitch_rotation_enabled
    repeat_times = mission.repeat_times
    waypoints = []
    for wp in mission.waypoints:
        waypoints.append(parse_waypoint(wp))
    
    return [poi, auto_flight_speed, max_flight_speed, exit_on_signal_lost, 
            finished_action, flight_path_mode, goto_first_waypoint_mode, heading_mode,
            gimbal_pitch_rotation_enabled, repeat_times, waypoints]
        
def parse_waypoint(wp):
    latitude = wp.latitude
    longitude = wp.longitude
    altitude = wp.altitude
    turn_mode = wp.turn_mode.value
    actions = []
    for action in wp.waypoint_actions:
            actions.append(parse_waypoint_action(action))
    return [latitude, longitude, altitude,turn_mode, actions]

def parse_waypoint_action(action):
    action_type = action.action_type.value
    action_param = action.action_param
    return [action_type, action_param]