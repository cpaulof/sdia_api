# import detection.detector
# from server_events import ServerEvents
# import client_mock
# import config
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


#test_detection()
def test_h264_decoder():
    import os
    import subprocess

    import av
    import av.datasets
    import cv2

    # We want an H.264 stream in the Annex B byte-stream format.
    # We haven't exposed bitstream filters yet, so we're gonna use the `ffmpeg` CLI.
    h264_path = "C:/Users/copau/night.264"
    i = av.datasets.curated("pexels/time-lapse-video-of-night-sky-857195.mp4")
    print(i)
    # if not os.path.exists(h264_path):
    #     subprocess.check_call(
    #         [
    #             "ffmpeg",
    #             "-i",
    #             f'"{i}"',
    #             "-vcodec",
    #             "copy",
    #             "-an",
    #             "-bsf:v",
    #             "h264_mp4toannexb",
    #             h264_path,
    #         ]
    #     )


    fh = open(h264_path, "rb")

    codec = av.CodecContext.create("h264", "r")
    codec.pix_fmt = 'yuv420p'
    while True:
        chunk = fh.read(1 << 16)

        packets = codec.parse(chunk)
        print("Parsed {} packets from {} bytes:".format(len(packets), len(chunk)))

        for packet in packets:
            print("   ", packet)

            frames = codec.decode(packet)
            for frame in frames:
                
                print("       ", frame, frame.to_rgb().to_ndarray().shape)
                img = frame.to_rgb().to_ndarray()
                cv2.imshow("img", cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                cv2.waitKey(int(1000/60))


        # We wait until the end to bail so that the last empty `buf` flushes
        # the parser.
        if not chunk:
            break

    print(dir(frame))



def test_parse_mission():
    mission_id = 14
    from mission_control import database
    from server import pkt_builder
    import struct
    db = database.Database(database.URI)
    m = db.get_mission_by_id(mission_id)
    ic(m)

    mission_data = ic(pkt_builder.parse_mission(m))

    pkt = ic(pkt_builder.waypoint_mission(mission_data))
    
    def test_client_mission_pkt_decode(pkt):
        poi_length = pkt[:4]
        poi_length, = struct.unpack('>I', poi_length)
        i = 4
        ic(poi_length)
        poi = b''
        for k in range(i, i+poi_length):
            poi+=pkt[k:k+1]
        i+=poi_length
        ic(poi)
        fmt = '>2f?4B?B'
        size = struct.calcsize(fmt)
        params = struct.unpack(fmt, pkt[i:i+size])
        i+=size
        ic(params)
        wp_count, = struct.unpack('>B', pkt[i:i+1])
        ic(wp_count)
        i+=1
        for k in range(wp_count):
            fmt = '>3f2B'
            size = struct.calcsize(fmt)
            wp_params = struct.unpack(fmt, pkt[i:i+size])
            i+=size
            ic(wp_params)
            action_count = wp_params[-1]
            for j in range(action_count):
                fmt = '>Bi'
                size = struct.calcsize(fmt)
                action_params = struct.unpack(fmt, pkt[i:i+size])
                i+=size
                ic(action_params)
        

    test_client_mission_pkt_decode(pkt)




test_parse_mission()