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


#test_detection()

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