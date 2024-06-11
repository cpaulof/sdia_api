import threading
import socket

from . import models, props


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
    
    
    