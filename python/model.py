from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.schema import (
    MetaData, Table, Column,
    ForeignKey, Identity,
)
from sqlalchemy.sql import (
    and_,
    select,
)
from sqlalchemy.types import (
    Integer, BigInteger, Text,
)

metadata = MetaData()
t_replays = Table(
    'replays', metadata,
    Column('id', BigInteger, Identity(always=True), primary_key=True),
    Column('elapsed_gameloops', Integer, nullable=False),
    Column('base_build', Integer, nullable=False),
    Column('map', Text, nullable=False),
    Column('utc_ts', BigInteger, nullable=False),
    Column('local_ts', BigInteger, nullable=False),
    Column('path', Text, nullable=False, unique=True),
    Column('sha256', Text, nullable=False, unique=True),
)

t_replays_players = Table(
    'replays_players', metadata,
    Column('id', BigInteger, Identity(always=True), primary_key=True),
    Column('replay_id', ForeignKey('replays.id')),
    Column('clan', Text, nullable=False),
    Column('name', Text, nullable=False),
    Column('race', Text, nullable=False),
    Column('result', Integer, nullable=False),
    Column('player_list_id', Integer, nullable=False),
    Column('team_id', Integer, nullable=False),
    Column('working_set_slot_id', Integer, nullable=False),
    Column('game_events_id', Integer, nullable=False),
    Column('tracker_events_id', Integer, nullable=False),
    Column('slot_id', Integer, nullable=False),
)

t_replays_tracker_events = Table(
    'replays_tracker_events', metadata,
    Column('id', BigInteger, Identity(always=True), primary_key=True),
    Column('replay_id', ForeignKey('replays.id')),
    Column('event_no', BigInteger, nullable=False),
    Column('event_name', Text, nullable=False),
    Column('event_id', Integer, nullable=False),
    Column('gameloop', Integer, nullable=False),
    Column('bits', Integer, nullable=False),
    Column('unit_tag_index', Integer, default=None),
    Column('unit_tag_recycle', Integer, default=None),
    Column('unit_type_name', Text, default=None),
    Column('control_player_id', Integer, default=None),
    Column('upkeep_player_id', Integer, default=None),
    Column('x', Integer, default=None),
    Column('y', Integer, default=None),
    Column('creator_unit_tag_index', Integer, default=None),
    Column('creator_unit_tag_recycle', Integer, default=None),
    Column('creator_ability_name', Text, default=None),
    Column('killer_player_id', Integer, default=None),
    Column('killer_unit_tag_index', Integer, default=None),
    Column('killer_unit_tag_recycle', Integer, default=None),
    Column('count', Integer, default=None),
    Column('player_id', Integer, default=None),
    Column('upgrade_type_name', Text, default=None),
    Column('stats', JSONB, default=None),
    Column('true_player_id', Integer, default=None),
    Column('entity_name', Text, default=None),
    Column('nth_event', Integer, nullable=False),
)

def get_replays_row_by_sha256(conn, sha256):
    stmt = select([t_replays]).where(t_replays.c.sha256 == sha256)
    return conn.execute(stmt).fetchone()
    

def insert_replays_row(conn, elapsed_gameloops, base_build, map_name, utc_ts, local_ts, path, sha256):
    stmt = t_replays.insert().values(
        elapsed_gameloops=elapsed_gameloops, base_build=base_build,
        map=map_name, utc_ts=utc_ts, local_ts=local_ts, path=path, sha256=sha256)
    return conn.execute(stmt).inserted_primary_key[0]

def insert_replays_players_rows(conn, rows):
    assert rows
    return conn.execute(t_replays_players.insert(), rows)

def insert_replays_tracker_events_rows(conn, rows):
    assert rows
    return conn.execute(t_replays_tracker_events.insert(), rows)

DEFAULT_REPLAYS_TRACKER_EVENTS_ROW = {
    'unit_tag_index': None,
    'unit_tag_recycle': None,
    'unit_type_name': None,
    'control_player_id': None,
    'upkeep_player_id': None,
    'x': None,
    'y': None,
    'creator_unit_tag_index': None,
    'creator_unit_tag_recycle': None,
    'creator_ability_name': None,
    'killer_player_id': None,
    'killer_unit_tag_index': None,
    'killer_unit_tag_recycle': None,
    'count': None,
    'player_id': None,
    'upgrade_type_name': None,
    'stats': None,
}    

def get_engine():
    return create_engine('postgresql://rbroot:changeme83@localhost/replaybrowser')
