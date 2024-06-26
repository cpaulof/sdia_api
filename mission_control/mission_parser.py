import threading
import socket

from mission_control import models, props


def parse_mission_model(mission: models.WaypointMission)->bytes:
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
    finished_action = mission.finished_action.name
    flight_path_mode = mission.flight_path_mode.name
    goto_first_waypoint_mode = mission.goto_first_waypoint_mode.name
    heading_mode = mission.heading_mode.name
    gimbal_pitch_rotation_enabled = mission.gimbal_pitch_rotation_enabled
    repeat_times = mission.repeat_times
    waypoints = []
    for wp in mission.waypoints:
        waypoints.append(parse_waypoint_model(wp))
    
    return {'id': mission.id, 'name': mission.name, 'poi':poi, 'auto_flight_speed':auto_flight_speed,
            'max_flight_speed':max_flight_speed, 'exit_on_signal_lost':exit_on_signal_lost, 
            'finished_action': finished_action, 'flight_path_mode':flight_path_mode, 
            'goto_first_waypoint_mode':goto_first_waypoint_mode, 'heading_mode': heading_mode,
            'gimbal_pitch_rotation_enabled': gimbal_pitch_rotation_enabled, 
            'repeat_times': repeat_times, 'waypoints':waypoints}
        
def parse_waypoint_model(wp):
    latitude = wp.latitude
    longitude = wp.longitude
    altitude = wp.altitude
    turn_mode = wp.turn_mode.name
    actions = []
    for action in wp.waypoint_actions:
            actions.append(parse_waypoint_action_model(action))
    return {'latitude': latitude,
             'longitude':longitude,
             'altitude': altitude, 
             'turn_mode': turn_mode, 
             'actions': actions}

def parse_waypoint_action_model(action):
    action_type = action.action_type.name
    action_param = action.action_param
    return {'action_type':action_type, 'action_param':action_param}

  