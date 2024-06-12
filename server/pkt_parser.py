import threading

HANDLERS = {
    0x01: None,
    0x61: None,
}

def add_handler(code:int, func:callable)->None:
    HANDLERS[code] = func

def heart_beat_handler(data):
    print('HEART_BEAT', data)

def parse_packet(pkt):
    code = pkt[0]
    data = pkt[1:]
    handler = HANDLERS.get(code, None)
    if handler is not None:
        threading.Thread(target=handler, args=(data,)).start()














