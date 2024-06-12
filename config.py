import os


BASEPATH = os.getcwd()

############ server ##############
SERVER_PORT = 3535
SERVER_HOST = '127.0.0.1'
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