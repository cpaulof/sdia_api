from enum import Enum

# __all__ = [
#     'WaypointMissionFinishedAction',
#     'WaypointMissionGotoWaypointMode',
#     'WaypointMissionFlightPathMode',
#     'WaypointMissionHeadingMode',
#     'WaypointTurnMode',
#     'WaypointActionType'
# ]

class WaypointMissionFinishedAction(Enum):
    NO_ACTION           = 0
    GO_HOME             = 1 # default
    AUTO_LAND           = 2
    GO_FIRST_WAYPOINT   = 3
    CONTINUE_UNTIL_END  = 4

class WaypointMissionGotoWaypointMode(Enum):
    SAFELY          = 0 # default
    POINT_TO_POINT  = 1

class WaypointMissionFlightPathMode(Enum):
    NORMAL = 0 #default
    CURVED = 1

class WaypointMissionHeadingMode(Enum):
    AUTO                            = 0 # default
    USING_INITIAL_DIRECTION         = 1
    CONTROL_BY_REMOTE_CONTROLLER    = 2
    USING_WAYPOINT_HEADING          = 3
    TOWARD_POINT_OF_INTEREST        = 4

class WaypointTurnMode(Enum):
    CLOCKWISE           = 0
    COUNTER_CLOCKWISE   = 1

class WaypointActionType(Enum):
    STAY                    = 0
    START_TAKE_PHOTO        = 1
    START_RECORD            = 2
    STOP_RECORD             = 3
    RESET_GIMBAL_YAW        = 4
    GIMBAL_PITCH            = 5
    CAMERA_ZOOM             = 6
    CAMERA_FOCUS            = 7
    PHOTO_GROUPING          = 8
    FINE_TUNE_GIMBAL_PITCH  = 9

