import threading

HANDLERS = {
    0x01: [],
    0x61: [],
}

PARSERS_CODE = {
    0x01: '_no_return_parser',
    0x61: 'telemetry_data',
    0x70: '_no_return_parser',
    0x71: '_no_return_parser',
    0x72: '_no_return_parser',
}

def add_handler(code:int, func:callable)->None:
    HANDLERS[code].append(func)

def heart_beat_handler(data):
    print('HEART_BEAT', data)

def parse_packet(pkt):
    code = pkt[0]
    data = pkt[1:]
    handlers = HANDLERS.get(code, [])
    for handler in handlers:
        threading.Thread(target=handler, args=(data,)).start()




############ parsers ##########################
def heart_beat_parser(data):
    return data

# placeholder 
def _no_return_parser(data):
    return data









