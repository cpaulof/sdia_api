import unittest
import os
from icecream import ic

from mission_control import database, mission_parser, props
import config

ic.disable()

class TestDatabase(unittest.TestCase):
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
    

    ######## testes
    def test_create_mission(self):
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
        
        self.assertNotEqual(r, -1)
        ##################
        # assegurar que foi inserido no db e corresponde ao mesmo registro

        
    
    def test_fail_creating_mission_with_bad_params(self):
        mission_name = 'mission_test_78776'
        ### WRONG Enum option "START_TAKE_PHOTOi"

        make_action = lambda: {'type': 'START_TAKE_PHOTOi', 'param':1} 
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
        self.assertEqual(r, -1)

    def test_get_mission(self):
        # create a mission first
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
        self.assertNotEqual(r, -1)

        # assure the db returns that register
        mission_db = self.db.get_mission_by_id(r)
        self.assertIsNotNone(mission_db)
        self.assertEqual(mission_db.name, mission_name)

    def test_get_mission_list(self):
        def _create_mission():
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
            self.assertNotEqual(r, -1)
        
        n = 12
        for i in range(n):
            _create_mission()
        
        ############

        missions = self.db.get_mission_list(200, 0)
        self.assertEqual(len(missions), n)




