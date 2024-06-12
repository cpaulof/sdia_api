'''
Um código é um byte que representa a função dos 
dados subsequentes enviados no pacote.
cada código está associado a um nome único, descrevendo o 
código, e um Callable, uma função que montará o pacote de acordo com
seus argumentos.

Códigos podem ser exclusivos 
'''
import server.pkt_builder as rec
import server.pkt_parser as sen

# CODE, NAME, RECEIVER, SENDER
# CODE -> Código
# NAME -> Nome
# RECEIVER -> Callable responsável por decodificar o pacote (Client -> Server)
# SENDER -> Callable responsável por codificar o pacote (Server -> Client)

BUILD_CODES = {
    'HEART_BEAT':                       0x00,
    'WAYPOINT_MISSION':                 (0x40, rec.waypoint_mission),
    'WAYPOINT_MISSION_START':           0x41,
    'WAYPOINT_MISSION_STOP':            0x42,
    'BATTERY_LEVEL':                    0x50,
    'SIGNAL_LEVEL':                     0x51,
}

def build_packet(code_name, *args):
    code, builder, _ = BUILD_CODES[code_name]
    pkt = builder(*args)
    return code, pkt




