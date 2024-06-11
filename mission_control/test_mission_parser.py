import unittest
import os
import copy
from icecream import ic

from mission_control import database, mission_parser, props
import config

ic.disable()

class TestConnection(unittest.TestCase):
    def setUp(self):
        temp_name = "db_test.db"
        self.temp_filepath = os.path.join(config.BASEPATH, temp_name)
        ic(self.temp_filepath)
        uri = r"sqlite:///" + self.temp_filepath
        self.db = database.Database(uri)
    
    def tearDown(self):
        if hasattr(self, "temp_filepath") and os.path.exists(self.temp_filepath):
            self.db.engine.dispose()
            os.remove(self.temp_filepath)
    
    def test_parse_waypoint_mission_model(self):
        mission_name = 'mission_test_78776'
        make_action = lambda: {'type': 'START_TAKE_PHOTO', 'param':1}
        waypoints = [
            {'lat': -2.13, 'lng': 44.56, 'alt': 10.0, 'turn_mode':'CLOCKWISE', 'actions':[make_action() for _ in range(5)]},
            {'lat': -2.23, 'lng': 44.56, 'alt': 10.0, 'turn_mode':'CLOCKWISE', 'actions':[make_action() for _ in range(5)]}, 
            {'lat': -2.23, 'lng': 44.46, 'alt': 10.0, 'turn_mode':'CLOCKWISE', 'actions':[make_action() for _ in range(5)]}, 
            {'lat': -2.13, 'lng': 44.46, 'alt': 10.0, 'turn_mode':'CLOCKWISE', 'actions':[make_action() for _ in range(5)]}, 
        ]
        r = self.db.add_waypoint_mission(name=mission_name,
                                    poi='-2.45:44.45',
                                    afs=5.0,
                                    mfs=10.0,
                                    eosl=False,
                                    end_action='AUTO_LAND',
                                    fpm='NORMAL',
                                    goto_mode='SAFELY',
                                    heading='CONTROL_BY_REMOTE_CONTROLLER',
                                    gpre=True,
                                    repeats=1,
                                    waypoints=waypoints
                                    )
        expected_data = ['-2.45:44.45', 5.0, 10.0, False, props.WaypointMissionFinishedAction.AUTO_LAND.value,
                         props.WaypointMissionFlightPathMode.NORMAL.value, props.WaypointMissionGotoWaypointMode.SAFELY.value,
                         props.WaypointMissionHeadingMode.CONTROL_BY_REMOTE_CONTROLLER.value, True, 1, [ 
                             # waypoints
                             [
                                -2.13, 44.56, 10.0, props.WaypointTurnMode.CLOCKWISE.value, [
                                    # actions
                                    [props.WaypointActionType.START_TAKE_PHOTO.value, 1],
                                    [props.WaypointActionType.START_TAKE_PHOTO.value, 1],
                                    [props.WaypointActionType.START_TAKE_PHOTO.value, 1],
                                    [props.WaypointActionType.START_TAKE_PHOTO.value, 1],
                                    [props.WaypointActionType.START_TAKE_PHOTO.value, 1],
                                 ]
                             ],
                             [
                                -2.23, 44.56, 10.0, props.WaypointTurnMode.CLOCKWISE.value, [
                                    # actions
                                    [props.WaypointActionType.START_TAKE_PHOTO.value, 1],
                                    [props.WaypointActionType.START_TAKE_PHOTO.value, 1],
                                    [props.WaypointActionType.START_TAKE_PHOTO.value, 1],
                                    [props.WaypointActionType.START_TAKE_PHOTO.value, 1],
                                    [props.WaypointActionType.START_TAKE_PHOTO.value, 1],
                                 ]
                             ],
                             [
                                -2.23, 44.46, 10.0, props.WaypointTurnMode.CLOCKWISE.value, [
                                    # actions
                                    [props.WaypointActionType.START_TAKE_PHOTO.value, 1],
                                    [props.WaypointActionType.START_TAKE_PHOTO.value, 1],
                                    [props.WaypointActionType.START_TAKE_PHOTO.value, 1],
                                    [props.WaypointActionType.START_TAKE_PHOTO.value, 1],
                                    [props.WaypointActionType.START_TAKE_PHOTO.value, 1],
                                 ]
                             ],
                             [
                                -2.13, 44.46, 10.0, props.WaypointTurnMode.CLOCKWISE.value, [
                                    # actions
                                    [props.WaypointActionType.START_TAKE_PHOTO.value, 1],
                                    [props.WaypointActionType.START_TAKE_PHOTO.value, 1],
                                    [props.WaypointActionType.START_TAKE_PHOTO.value, 1],
                                    [props.WaypointActionType.START_TAKE_PHOTO.value, 1],
                                    [props.WaypointActionType.START_TAKE_PHOTO.value, 1],
                                 ]
                             ]
                         ]
                         ]
        
        mission = self.db.get_mission_by_id(r)
        
        # expected_data2 = copy.deepcopy(expected_data)
        # expected_data2[10][0][4][-1][1] = 1
        # ic(expected_data)
        

        parsed_data = mission_parser.parse_mission_model(mission)
        ic(expected_data == parsed_data)
        self.assertEqual(expected_data, parsed_data)



