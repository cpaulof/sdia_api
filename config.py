import os


BASEPATH = os.getcwd()

API_HOST = '0.0.0.0'
API_PORT = 5000
############ server ##############
SERVER_PORT = 6564
SERVER_VIDEO_FEED_PORT = 6565
SERVER_HOST = '0.0.0.0'
SERVER_RETRY = True
SERVER_LOG_EVENTS = True
SERVER_LOG_DIR = './logs/server/'
###################################

################ flight logger #####
FLIGHT_LOG_DIR = './logs/flight/'

####################################

########### mission db ###########
SQLITE_DB_FILEPATH = "./SDIA.db"

##################################

CAPTURE_URL = "C:\\Users\\copau\\OneDrive\\Desktop\\Projeto DRONE IFMA\\Recording 2024-06-15 155650.mp4"#'rtmp://127.0.0.1:1935/live'
RECORDER_DIR = './logs/camera/'

# video
# image
RECODER_MODE = 'video'


########### det ##############
DETECTION_CONF = 0.5
DETECTION_IOU = 0.2
DETECTION_IMAGE_SIZE = (640, 640)
