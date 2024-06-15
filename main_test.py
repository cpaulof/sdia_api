import detection.detector
from server_events import ServerEvents
import client_mock
import config
from icecream import ic
import time

def test_client_server():
    ic.enable()
    server_events = ServerEvents()
    ic(server_events)
    ic(server_events.start_server())
    server_events.initialize_default_listeners()



    client = client_mock._Client(config.SERVER_HOST, config.SERVER_PORT)
    ic(client)
    time.sleep(2)
    ic('TAKING OFFFFFFFFFFFFFF')
    client.takeoff()

    time.sleep(10)

    ic('LANDINGGGGGGGGGGGGGGG')
    client.land()
    time.sleep(5)
    ic('TAKING OFFFFFFFFFFFFFF')
    client.takeoff()

def test_detection():
    import detection
    detection.detector.main()


test_detection()