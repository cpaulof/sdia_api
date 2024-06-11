from datetime import datetime

from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer, Boolean, Float, DateTime,  Enum
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from . import props

class Base(DeclarativeBase): pass

class WaypointMission(Base):
    __tablename__ = 'waypoint_mission'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    point_of_interest: Mapped[str]

    auto_flight_speed: Mapped[float]  = mapped_column(Float(), default=5.0)
    max_flight_speed: Mapped[float]   = mapped_column(Float(), default=10.0)
    exit_on_signal_lost: Mapped[bool] = mapped_column(Boolean(), default=False)
    finished_action: Mapped[Enum] = mapped_column(Enum(props.WaypointMissionFinishedAction), default=props.WaypointMissionFinishedAction.GO_HOME)
    flight_path_mode: Mapped[int] = mapped_column(Enum(props.WaypointMissionFlightPathMode), default=props.WaypointMissionFlightPathMode.NORMAL)
    goto_first_waypoint_mode: Mapped[int] = mapped_column(Enum(props.WaypointMissionGotoWaypointMode), default=props.WaypointMissionGotoWaypointMode.SAFELY)
    heading_mode: Mapped[int] = mapped_column(Enum(props.WaypointMissionHeadingMode), default=props.WaypointMissionHeadingMode.TOWARD_POINT_OF_INTEREST)

    gimbal_pitch_rotation_enabled: Mapped[bool] = mapped_column(Boolean(), default=True)
    repeat_times: Mapped[int] = mapped_column(Integer(), default=1)
    created_at: Mapped[str] = mapped_column(DateTime(), default=datetime.now)
    waypoints: Mapped[List["Waypoint"]] = relationship(lazy="joined")

    def __repr__(self):
        return f'<Mission id={self.id} name="{self.name}" created_at="{self.created_at}" waypoints={len(self.waypoints)}'


class Waypoint(Base):
    __tablename__ = 'waypoint'
    id: Mapped[int] = mapped_column(primary_key=True)
    waypoint_mission_id: Mapped[int]  = mapped_column(ForeignKey('waypoint_mission.id'))
    latitude: Mapped[float]
    longitude: Mapped[float]
    altitude: Mapped[float]
    turn_mode: Mapped[int] = mapped_column(Enum(props.WaypointTurnMode), default=props.WaypointTurnMode.CLOCKWISE)
    
    waypoint_actions: Mapped[List["WaypointAction"]] = relationship(lazy="joined")



class WaypointAction(Base):
    __tablename__ = 'waypoint_action'
    id: Mapped[int] = mapped_column(primary_key=True)
    action_type: Mapped[Enum] = mapped_column(Enum(props.WaypointActionType))
    action_param: Mapped[int]

    waypoint_id: Mapped[int]  = mapped_column(ForeignKey('waypoint.id'))

if __name__ == "__main__":
    from sqlalchemy import create_engine, select
    from sqlalchemy.orm import Session

    engine = create_engine(r"sqlite:///C:/Users/copau/OneDrive/Desktop/Projeto DRONE IFMA/sdia_api/sdia.db", echo=False)
    Base.metadata.create_all(engine)
    
    with Session(engine) as session:
        # m = WaypointMission(name="Missao Teste", point_of_interest="-2.4344:44.1233")
        # session.add(m)

        # waypoint1 = Waypoint()
        # session.commit()

        # = select(WaypointMission).where(WaypointMission.id == 1)
        # s:WaypointMission = session.get(WaypointMission, 1)
        # session.get()
        # print("______________________")
        # print(s.flight_path_mode, s.flight_path_mode.value)
        # print("______________________")

        missions = session.query(WaypointMission).where(WaypointMission.name.contains("Teste")).all()
        m = missions[0]
        waypoint1 = Waypoint(waypoint_mission_id=m.id, latitude=2.342, longitude=44.2231, altitude=15.0)
        m.waypoints.append(waypoint1)
        #session.commit()
        print('missions', missions)