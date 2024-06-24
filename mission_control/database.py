import os

from icecream import ic
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, joinedload

from mission_control import models, props, mission_parser
import config

URI = r"sqlite:///" + os.path.join(config.BASEPATH, config.SQLITE_DB_FILEPATH)

class Database:
    def __init__(self, uri, echo=False):
        self.engine = create_engine(uri, echo=echo)
        models.Base.metadata.create_all(self.engine)
        #self.session:Session = Session(self.engine)
    
    def create_mission(self, name, poi, afs, mfs, eosl, end_action, fpm, goto_mode, heading, gpre, repeats):
        mission = None
        try:
            assert len(poi.split(':')) == 2, "POI not valid"
            assert isinstance(repeats, int) and repeats >= 1, "repeats not valid"
            assert all([isinstance(i, int) for i in (end_action, fpm, goto_mode, heading)]), "Enumerators not valid"
            assert all([isinstance(i, (float, int)) and i>0.0 for i in (afs, mfs)]), "flight speeds not valid"

            mission = models.WaypointMission(
                name=name,
                point_of_interest = poi,
                auto_flight_speed = float(afs),
                max_flight_speed = float(mfs),
                exit_on_signal_lost = eosl,
                finished_action = props.WaypointMissionFinishedAction(end_action),
                flight_path_mode = props.WaypointMissionFlightPathMode(fpm),
                goto_first_waypoint_mode = props.WaypointMissionGotoWaypointMode(goto_mode),
                heading_mode = props.WaypointMissionHeadingMode(heading),
                gimbal_pitch_rotation_enabled = gpre,
                repeat_times = repeats
            )
        except Exception as err:
            ic(err)

        return mission
    
    def create_waypoint(self, mission, lat, lng, alt, turn_mode):
        wp = None
        try:
            assert isinstance(lat, float), "latitude not valid"
            assert isinstance(lng, float), "longitude not valid"
            assert isinstance(alt, (float, int)), "altitude not valid"
            assert isinstance(turn_mode, int), "Turn mode notvalid"

            wp = models.Waypoint(waypoint_mission_id = mission.id,
                                 latitude=lat,
                                 longitude=lng,
                                 altitude=float(alt),
                                 turn_mode=props.WaypointTurnMode(turn_mode))

        except Exception as err:
            ic(err)

        return wp

    def create_waypoint_action(self, waypoint, action_type, action_param):
        action = None
        try:
            assert isinstance(action_type, int)
            assert isinstance(action_param, int)

            action = models.WaypointAction(waypoint_id=waypoint.id,
                                           action_type=props.WaypointActionType(action_type), 
                                           action_param=action_param)
        except Exception as err:
            ic(err)

        return action

    def add_waypoint_mission(self, **kw):
        with Session(self.engine) as session, session.begin():
            try:
                mission = self.create_mission(
                    kw['name'],
                    kw['point_of_interest'],
                    kw['auto_flight_speed'],
                    kw['max_flight_speed'],
                    kw['exit_on_signal_lost'],
                    kw['finished_action'],
                    kw['flight_path_mode'],
                    kw['goto_first_waypoint_mode'],
                    kw['heading_mode'],
                    kw['gimbal_pitch_rotation_enabled'],
                    kw['repeat_times'])
                assert mission is not None, 'Mission params not valid'

                waypoints = kw['waypoints']
                for wp in waypoints:
                    waypoint_ = self.create_waypoint(mission, wp['latitude'], wp['longitude'], wp['altitude'], wp['turn_mode'])
                    assert waypoint_ is not None, 'Waypoint params not valid'
                    for act in wp['waypoint_actions']:
                        action_ = self.create_waypoint_action(waypoint_, act['action_type'], act['action_param'])
                        assert action_ is not None, 'Action params not valid'
                        waypoint_.waypoint_actions.append(action_)
                    mission.waypoints.append(waypoint_)
                
                session.add(mission)
                session.flush()
                return mission.id

            except Exception as err:
                session.rollback()
                session.close()
                ic(err)
                return -1
    
    def get_mission_by_id(self, mission_id):
        with Session(self.engine) as session:
            mission = session.get(models.WaypointMission, mission_id)
            return mission
    
    def get_mission_list(self, amount, page):
        with Session(self.engine) as session:
            missions = session.query(models.WaypointMission).limit(amount).offset(page*amount).all()
            return missions
        
    def _serialize_one(self, mission):
        obj = mission_parser.parse_mission_model(mission)
        return obj
    
    def serialize(self, objs):
        if isinstance(objs, list):
            return [self._serialize_one(m) for m in objs]
        return self._serialize_one(objs)



#######################################################
def main():
    database = Database(URI)
    def _test_add_mission():
        mission_name = 'mission_test_78776'
        make_action = lambda: {'type': 'START_TAKE_PHOTOi', 'param':1}
        waypoints = [
            {'lat': -2.13, 'lng': 44.56, 'alt': 10.0, 'turn_mode':'CLOCKWISE', 'actions':[make_action() for _ in range(5)]},
            {'lat': -2.23, 'lng': 44.56, 'alt': 10.0, 'turn_mode':'CLOCKWISE', 'actions':[make_action() for _ in range(5)]}, 
            {'lat': -2.23, 'lng': 44.46, 'alt': 10.0, 'turn_mode':'CLOCKWISE', 'actions':[make_action() for _ in range(5)]}, 
            {'lat': -2.13, 'lng': 44.46, 'alt': 10.0, 'turn_mode':'CLOCKWISE', 'actions':[make_action() for _ in range(5)]}, 
        ]
        ic(database.add_waypoint_mission(name=mission_name,
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
                                    ))
    def _test_get_mission_list():
        ic(database.get_mission_list(3, 2))
    
    def _test_get_mission_by_id():
        mission = ic(database.get_mission_by_id(2))
        ic(mission.finished_action)
        ic(mission.finished_action.value)
    # _test_add_mission()
    # _test_get_mission_list()
    _test_get_mission_by_id()

