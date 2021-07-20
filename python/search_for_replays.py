#!/usr/bin/env python3
import copy
import html
import itertools
import math
import os
import pathlib
import pprint
import sys
from collections import defaultdict
from datetime import datetime, timedelta

import mpyq
from s2protocol import versions

FRAMES_PER_SECOND = 16*1.4
BASE_CLOSENESS_THRESHOLD = 30
print("pathlib.Path(__file__).absolute().parent.parent: {}".format(pathlib.Path(__file__).absolute().parent.parent))
# REPLAY_DIR = pathlib.Path(__file__).absolute().parent.parent
REPLAY_DIR = pathlib.Path(__file__).absolute().parent.parent / "replays"

RACE_TRANSLATION_LOOKUP = {
    "저그": "Zerg",
    '异虫': 'Zerg',
    "蟲族": "Zerg",
    "Zerg": "Zerg",
    "Зерги": "Zerg",
    "테란": "Terran",
    "人類": "Terran",
    '人类': 'Terran',
    "Terraner": "Terran",
    "Terran": "Terran",
    'Терраны': 'Terran',
    'Terranie': 'Terran',
    "프로토스": "Protoss",
    "神族": "Protoss",
    "Protosi": "Protoss",
    "Protoss": "Protoss",
    '星灵': 'Protoss',
    'Протоссы': 'Protoss',
}


def get_time_for_gameloop(gameloop):
    return str(timedelta(seconds=gameloop/FRAMES_PER_SECOND))

def get_replay_filenames(path):
    assert path.exists(), path
    for root, dirs, files in os.walk(path):
        for name in files:
            yield os.path.join(root, name)

def get_data_from_replay(replay_file_name, internal_filename, extractor_func):
    archive = mpyq.MPQArchive(replay_file_name)
    contents = archive.header['user_data_header']['content']
    header = versions.latest().decode_replay_header(contents)

    base_build = header['m_version']['m_baseBuild']
    # protocol80669.py
    # protocol80949.py
    # protocol81009.py
    # protocol82457.py
    # protocol82893.py
    BUILD_REPLACEMENT = {
        # 80188: 78285,
        # 79998: 78285,
        # 81102: 81009,
        81433: 81009,
    }
    base_build = BUILD_REPLACEMENT.get(base_build, base_build)
    protocol = versions.build(base_build)

    contents = archive.read_file(internal_filename)
    return extractor_func(protocol, contents)

def get_replay_tracker_events_gen(replay_file_name):
    return get_data_from_replay(
        replay_file_name, 'replay.tracker.events',
        lambda protocol, contents: protocol.decode_replay_tracker_events(contents))

def get_replay_details(replay_file_name):
    return get_data_from_replay(
        replay_file_name, 'replay.details',
        lambda protocol, contents: protocol.decode_replay_details(contents))

def get_replay_initdata(replay_file_name):
    return get_data_from_replay(
        replay_file_name, 'replay.initData',
        lambda protocol, contents: protocol.decode_replay_initdata(contents))

PLAYER_SETUP_EVENT_NAME = 'NNet.Replay.Tracker.SPlayerSetupEvent'
def get_player_setup_events(filename):
    return tuple(itertools.takewhile(
        lambda event: event["_event"] == PLAYER_SETUP_EVENT_NAME,
        itertools.dropwhile(
            lambda event: event["_event"] != PLAYER_SETUP_EVENT_NAME,
            get_replay_tracker_events_gen(filename)
        )))

def extract_replay_details(filename):
    # first, get names of actual people playing, which is stored in
    # replay_details (replay_initdata has observers, though maybe you
    # can actually use it as a source of truth still if you look at
    # the "customInterface" flag?
    replay_details = get_replay_details(filename)
    WINDOWS_EPOCH_OFFSET = 116444736000000000
    timeLocalOffset = replay_details['m_timeLocalOffset']
    timeUTC = replay_details['m_timeUTC']
    unix_ts = (timeUTC - WINDOWS_EPOCH_OFFSET) / 10**7
    local_ts = (timeUTC - WINDOWS_EPOCH_OFFSET + timeLocalOffset) / 10**7

    player_list = replay_details['m_playerList']
    players_by_team = {}
    player_lookup = {}
    player_lookup_by_list_id = {}
    for i, player_info in enumerate(player_list):
        # e.g. player_info['m_name'] == b'&lt;RLSM&gt;<sp/>crankx'
        full_name = html.unescape(player_info['m_name'].decode('utf8'))
        if '<sp/>' in full_name:
            clan, name = full_name.split('<sp/>')
            assert clan.startswith('<') and clan.endswith('>')
            clan = clan[1:-1]
        else:
            clan, name = '', full_name
        observe = player_info['m_observe']
        race = RACE_TRANSLATION_LOOKUP[player_info['m_race'].decode('utf8')]
        result = player_info['m_result']
        team_id = player_info['m_teamId']
        working_set_slot_id = player_info['m_workingSetSlotId']
        player_record = {
            "player_list_id": i,
            "clan": clan,
            "name": name,
            "observe": observe,
            "race": race,
            "result": result,
            "team_id": team_id,
            "working_set_slot_id": working_set_slot_id,
        }
        player_lookup[name] = player_record
        player_lookup_by_list_id[i] = player_record
        if team_id not in players_by_team:
            players_by_team[team_id] = []
        players_by_team[team_id].append(player_record)
    map_title = replay_details['m_title'].decode('utf8')

    initdata = get_replay_initdata(filename)

    # there are a bunch of empty ones. looks like it mostly just has league data here that's useful.
    # this might actually be more accurate for determining a player's player_id in game_events!
    # note, maybe "customInterface is False for actual players, true for observers?
    for i, player_info in enumerate(initdata['m_syncLobbyState']['m_userInitialData']):
        name = player_info["m_name"].decode('utf8')
        if name not in player_lookup:
            continue
        clan = player_info["m_clanTag"].decode('utf8') if player_info["m_clanTag"] else ""
        if player_lookup[name]["clan"] != clan:
            continue
        player_lookup[name]["game_events_id"] = i

    # adjust for AI players who don't show up in game_events
    for player_record in player_lookup.values():
        if "game_events_id" not in player_record:
            player_record["game_events_id"] = None

    player_setup_events = get_player_setup_events(filename)

    for i, e in enumerate(player_setup_events):
        player_id = e.pop('m_playerId')
        slot_id = e.pop('m_slotId')
        type_ = e.pop('m_type')
        # type == 1 might be real players
        user_id = e.pop('m_userId') # same as slot_id, is the player id in replay_game_events
        player_info = player_lookup_by_list_id[i]
        # slot id is usually the same as working_slot_id, but it's kinda weird sometimes it looks like
        assert player_info["game_events_id"] == user_id
        player_info["tracker_events_id"] = player_id
        player_info["slot_id"] = slot_id

    result_builder = []
    vs_label_builder = []
    for team in players_by_team.values():
        # players_by_team[team_id].append("{} ({})".format(full_name.replace('<sp/>', ' '), race[0]))
        team_str_builder = []
        for player_info in team:
            player_str = "{} ({})".format(player_info["name"], player_info["race"][0])
            team_str_builder.append(player_str)
        vs_label_builder.append(", ".join(team_str_builder))
        result_builder.append(str(team[0]["result"]))

    starting_positions = {}
    for event in get_replay_tracker_events_gen(filename):
        e = copy.deepcopy(event)
        # example event we're looking for
        # {'_bits': 584,
        #  '_event': 'NNet.Replay.Tracker.SUnitBornEvent',
        #  '_eventid': 1,
        #  '_gameloop': 23518,
        #  'm_controlPlayerId': 2,
        #  'm_creatorAbilityName': b'StarportTrain',
        #  'm_creatorUnitTagIndex': 262,
        #  'm_creatorUnitTagRecycle': 3,
        #  'm_unitTagIndex': 515,
        #  'm_unitTagRecycle': 6,
        #  'm_unitTypeName': b'Battlecruiser',
        #  'm_upkeepPlayerId': 2,
        #  'm_x': 36,
        #  'm_y': 144}
        gameloop = e["_gameloop"]
        event_name = e["_event"]
        if gameloop > 0:
            break
        elif event_name not in (
                "NNet.Replay.Tracker.SUnitBornEvent",
                "NNet.Replay.Tracker.SUnitInitEvent"):
            continue

        controlPlayerId = e['m_controlPlayerId']
        if controlPlayerId == 0:
            # e.g., for neutral things like mineral fields and forcefields
            continue
        unitTypeName = e['m_unitTypeName'].decode('utf8')
        x, y = e['m_x'], e['m_y']

        if event_name == "NNet.Replay.Tracker.SUnitBornEvent" and gameloop == 0:
            if unitTypeName in ("Nexus", "Hatchery", "CommandCenter"):
                starting_positions[controlPlayerId] = (x, y)

    
    return {
        "vs_label": " vs ".join(vs_label_builder),
        "result": "-".join(result_builder),
        "map_title": map_title,
        "player_lookup_by_name": player_lookup,
        "utc_timestamp": unix_ts,
        "local_timestamp": local_ts,
        "starting_pos_by_ctrlPID": starting_positions,
    }


EXAMPLE_REPLAY = "dreamhack_sc2_masters_2020_fall/Season Finals/Group Stage/Group B/1 Reynor vs. Nice/Ever Dream.SC2Replay"
THRESHOLD = 70
# Zerg player makes a hatchery sufficient far away from their home base, early enough in the game
def is_proxy_hatch(replay_file):
    replay_metadata = extract_replay_details(replay_file)
    races = set()
    for info in replay_metadata['player_lookup_by_name'].values():
        races.add(info['race'])
    # zerg player must exist
    if "Zerg" not in races:
        return False
    starting_pos_by_ctrlPID = replay_metadata["starting_pos_by_ctrlPID"]
    for event in get_replay_tracker_events_gen(replay_file):
        e = copy.deepcopy(event)
        gameloop = e["_gameloop"]
        event_name = e["_event"]
        if gameloop >= FRAMES_PER_SECOND*180:
            break
        elif event_name not in (
                "NNet.Replay.Tracker.SUnitBornEvent",
                "NNet.Replay.Tracker.SUnitInitEvent"):
            continue
        
        controlPlayerId = e['m_controlPlayerId']
        if controlPlayerId == 0:
            # e.g., for neutral things like mineral fields and forcefields
            continue
        unitTypeName = e['m_unitTypeName'].decode('utf8')
        x, y = e['m_x'], e['m_y']

        if unitTypeName == "Hatchery":
            start_x, start_y = starting_pos_by_ctrlPID[controlPlayerId]
            dx, dy = x-start_x, y-start_y
            if dx*dx+dy*dy > THRESHOLD**2:
                print(math.sqrt(dx*dx+dy*dy))
                print(timedelta(seconds=gameloop/FRAMES_PER_SECOND))
                return True

def is_cannon_rush(replay_file):
    replay_metadata = extract_replay_details(replay_file)
    races = set()
    for info in replay_metadata['player_lookup_by_name'].values():
        races.add(info['race'])
    # protoss player must exist
    if "Protoss" not in races:
        return False
    starting_pos_by_ctrlPID = replay_metadata["starting_pos_by_ctrlPID"]
    for event in get_replay_tracker_events_gen(replay_file):
        e = copy.deepcopy(event)
        gameloop = e["_gameloop"]
        event_name = e["_event"]
        if gameloop >= FRAMES_PER_SECOND*180:
            break
        elif event_name not in (
                "NNet.Replay.Tracker.SUnitBornEvent",
                "NNet.Replay.Tracker.SUnitInitEvent"):
            continue
        
        controlPlayerId = e['m_controlPlayerId']
        if controlPlayerId == 0:
            # e.g., for neutral things like mineral fields and forcefields
            continue
        unitTypeName = e['m_unitTypeName'].decode('utf8')
        x, y = e['m_x'], e['m_y']
        start_x, start_y = starting_pos_by_ctrlPID[controlPlayerId]
        dx, dy = x-start_x, y-start_y
        dist_squared_from_home = dx*dx+dy*dy

        if unitTypeName == "PhotonCannon" and dist_squared_from_home > THRESHOLD**2:
            time = get_time_for_gameloop(gameloop)
            map_title = replay_metadata["map_title"]
            vs_label = replay_metadata["vs_label"]
            utc_timestamp = replay_metadata["utc_timestamp"]
            print("distance: {}".format(math.sqrt(dx*dx+dy*dy)))
            print("{}: {} ({}), {}".format(time, vs_label, map_title, datetime.utcfromtimestamp(utc_timestamp)))
            print(replay_file)
            return True

def is_adept_twister(replay_file):
    replay_metadata = extract_replay_details(replay_file)
    races = set()
    for info in replay_metadata['player_lookup_by_name'].values():
        races.add(info['race'])
    # protoss player must exist
    if "Protoss" not in races:
        return False
    starting_pos_by_ctrlPID = replay_metadata["starting_pos_by_ctrlPID"]
    unit_counts_by_ctrlPID = {ctrlPID: defaultdict(int) for ctrlPID in starting_pos_by_ctrlPID}
    for event in get_replay_tracker_events_gen(replay_file):
        e = copy.deepcopy(event)
        gameloop = e["_gameloop"]
        event_name = e["_event"]
        if gameloop >= FRAMES_PER_SECOND*240:
            break
        elif event_name not in (
                "NNet.Replay.Tracker.SUnitBornEvent",
                "NNet.Replay.Tracker.SUnitInitEvent"):
            continue
        
        controlPlayerId = e['m_controlPlayerId']
        if controlPlayerId == 0:
            # e.g., for neutral things like mineral fields and forcefields
            continue
        unitTypeName = e['m_unitTypeName'].decode('utf8')
        unit_counts_by_ctrlPID[controlPlayerId][unitTypeName] += 1
        x, y = e['m_x'], e['m_y']
        start_x, start_y = starting_pos_by_ctrlPID[controlPlayerId]
        dx, dy = x-start_x, y-start_y
        dist_squared_from_home = dx*dx+dy*dy
        if unit_counts_by_ctrlPID[controlPlayerId]["Adept"] >= 5:
            time = get_time_for_gameloop(gameloop)
            map_title = replay_metadata["map_title"]
            vs_label = replay_metadata["vs_label"]
            utc_timestamp = replay_metadata["utc_timestamp"]
            print("distance: {}".format(math.sqrt(dx*dx+dy*dy)))
            print("{}: {} ({}), {}".format(time, vs_label, map_title, datetime.utcfromtimestamp(utc_timestamp)))
            print(replay_file)
            return True

def is_roach_rush(replay_file):
    replay_metadata = extract_replay_details(replay_file)
    races = set()
    for info in replay_metadata['player_lookup_by_name'].values():
        races.add(info['race'])
    # protoss player must exist
    if "Zerg" not in races:
        return False
    starting_pos_by_ctrlPID = replay_metadata["starting_pos_by_ctrlPID"]
    unit_counts_by_ctrlPID = {ctrlPID: defaultdict(int) for ctrlPID in starting_pos_by_ctrlPID}
    for event in get_replay_tracker_events_gen(replay_file):
        e = copy.deepcopy(event)
        gameloop = e["_gameloop"]
        event_name = e["_event"]
        if gameloop >= FRAMES_PER_SECOND*240:
            break
        elif event_name not in (
                "NNet.Replay.Tracker.SUnitBornEvent",
                "NNet.Replay.Tracker.SUnitInitEvent"):
            continue
        
        controlPlayerId = e['m_controlPlayerId']
        if controlPlayerId == 0:
            # e.g., for neutral things like mineral fields and forcefields
            continue
        unitTypeName = e['m_unitTypeName'].decode('utf8')
        unit_counts_by_ctrlPID[controlPlayerId][unitTypeName] += 1
        x, y = e['m_x'], e['m_y']
        start_x, start_y = starting_pos_by_ctrlPID[controlPlayerId]
        dx, dy = x-start_x, y-start_y
        dist_squared_from_home = dx*dx+dy*dy
        if unit_counts_by_ctrlPID[controlPlayerId]["Roach"] >= 3:
            time = get_time_for_gameloop(gameloop)
            map_title = replay_metadata["map_title"]
            vs_label = replay_metadata["vs_label"]
            utc_timestamp = replay_metadata["utc_timestamp"]
            print("distance: {}".format(math.sqrt(dx*dx+dy*dy)))
            print("{}: {} ({}), {}".format(time, vs_label, map_title, datetime.utcfromtimestamp(utc_timestamp)))
            print(replay_file)
            return True

BEACONS = {
    'BeaconArmy',
    'BeaconAttack',
    'BeaconAuto',
    'BeaconClaim',
    'BeaconCustom1',
    'BeaconCustom2',
    'BeaconCustom3',
    'BeaconCustom4',
    'BeaconDefend',
    'BeaconDetect',
    'BeaconExpand',
    'BeaconHarass',
    'BeaconIdle',
    'BeaconRally',
    'BeaconScout',
}
        
def matches(replay_file, query):
    replay_metadata = extract_replay_details(replay_file)
    races = set()
    for info in replay_metadata['player_lookup_by_name'].values():
        races.add(info['race'])
    # protoss player must exist
    if "race" in query and query["race"] not in races:
        return False
    starting_pos_by_ctrlPID = replay_metadata["starting_pos_by_ctrlPID"]
    unit_counts_by_ctrlPID = {ctrlPID: defaultdict(int) for ctrlPID in starting_pos_by_ctrlPID}
    for event in get_replay_tracker_events_gen(replay_file):
        e = copy.deepcopy(event)
        gameloop = e["_gameloop"]
        event_name = e["_event"]
        if gameloop >= FRAMES_PER_SECOND*query["max_time"]:
            break
        elif event_name not in (
                "NNet.Replay.Tracker.SUnitBornEvent",
                "NNet.Replay.Tracker.SUnitInitEvent"):
            continue
        
        controlPlayerId = e['m_controlPlayerId']
        if controlPlayerId == 0:
            # e.g., for neutral things like mineral fields and forcefields
            continue
        unitTypeName = e['m_unitTypeName'].decode('utf8')
        if unitTypeName in BEACONS:
            continue
        unit_counts_by_ctrlPID[controlPlayerId][unitTypeName] += 1
        x, y = e['m_x'], e['m_y']
        start_x, start_y = starting_pos_by_ctrlPID[controlPlayerId]
        dx, dy = x-start_x, y-start_y
        dist_squared_from_home = dx*dx+dy*dy
        # pprint.pprint(get_time_for_gameloop(gameloop))
        # pprint.pprint(unit_counts_by_ctrlPID)
        if all(unit_counts_by_ctrlPID[controlPlayerId][unit_name] >= threshold
               for unit_name, proxy_predicate, threshold in query["units"]):
            time = get_time_for_gameloop(gameloop)
            map_title = replay_metadata["map_title"]
            vs_label = replay_metadata["vs_label"]
            utc_timestamp = replay_metadata["utc_timestamp"]
            print("distance: {}".format(math.sqrt(dx*dx+dy*dy)))
            print("{}: {} ({}), {}".format(time, vs_label, map_title, datetime.utcfromtimestamp(utc_timestamp)))
            print(replay_file)
            return True
    

        
def is_proxy(dist_squared_from_home):
    return dist_squared_from_home > 70**2

def is_anywhere(dist_squared_from_home):
    return True

# TODO: Maybe make these namedtuples

# adept twister is 5 adepts by 3:30
ADEPT_TWISTER = {
    "units": (
        ("Adept", is_anywhere, 5),
    ),
    "max_time": 210,
}

THREE_CC_HELLION_BANSHEE = {
    "units": (
        ("Hellion", is_anywhere, 8),
        ("Banshee", is_anywhere, 2),
        ("CommandCenter", is_anywhere, 3),
    ),
    "race": "Terran",
    "max_time": 330,
}

PROXY_HATCH = {
    "units": (
        ("Hatchery", is_proxy, 1),
    ),
    "max_time": 180,
}

CHARGELOT_ALLIN = {
    "units": (
        ("Zealot", is_anywhere, 8),
    ),
    "race": "Protoss",
    "max_time": 330, # 5:00
}

def main():
    # matches("/home/darren/gitrepo/replaybrowser/replays/teamliquid_starleague_7/Semifinals/Semifinals Match 2/Reynor VS Cure Game 4.SC2Replay", THREE_CC_HELLION_BANSHEE)
    # return 0
    abs_paths = []
    for root, dirs, files in os.walk(REPLAY_DIR):
        for name in files:
            if not name.endswith(".SC2Replay"):
                continue
            abs_paths.append(os.path.join(root, name))
    for abs_path in abs_paths:
        print("processing {}".format(abs_path))
        if matches(abs_path, CHARGELOT_ALLIN):
            continue
    return 0

if __name__ == "__main__":
    status = main()
    sys.exit(status)
