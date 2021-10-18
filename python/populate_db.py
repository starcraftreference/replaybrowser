#!/usr/bin/env python3
import collections
import copy
import hashlib
import html
import itertools
import math
import os
import pathlib
import pprint
import sys
from datetime import datetime, timedelta

import mpyq
from s2protocol import versions

from model import (
    get_engine,
    get_replays_row_by_sha256,
    insert_replays_row,
    insert_replays_players_rows,
    insert_replays_tracker_events_rows,
)

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

MAPS = (
    (
        "Eternal Empire LE",
        "永恆帝國 - 天梯版",
        "Empire éternel EC",
        "Ewiges Imperium LE",
        "이터널 엠파이어 - 래더",
        "Imperio eterno EE",
        'Imperio eterno EJ',
        '永恒帝国-天梯版',
        'Вечная империя РВ',
    ), (
        "World of Sleepers LE",
        "Welt der Schläfer LE",
        "休眠者之境 - 天梯版",
        "Domaine des dormeurs EC",
        "월드 오브 슬리퍼스 - 래더",
        'Mundo de durmientes EE',
    ), (
        "Triton LE",
        "Triton EC",
        "海神信使 - 天梯版",
        "트라이튼 - 래더",
        'Tritón EE',
    ), (
        "Nightshade LE",
        "Nocny Mrok ER",
        "毒茄樹叢 - 天梯版",
        "나이트쉐이드 - 래더",
        'Belladona EE',
        'Belladone EC',
    ), (
        "Zen LE",
        "젠 - 래더",
        'Zen EC',
        'Zen EE',
        'Zen EJ',
    ), (
        "Ephemeron LE",
        "Efemeryda ER",
        "이페머론 - 래더",
        'Efímero EE',
        'Éphémèrion EC',
    ), (
        "Purity and Industry LE",
    ), (
        "Golden Wall LE",
        "골든 월 - 래더",
        '黄金墙-天梯版',
        'Mur doré EC',
    ), (
        "Ever Dream LE",
        "에버 드림 - 래더",
        "永恒梦境-天梯版",
        "Помечтай РВ",
    ), (
        "Simulacrum LE",
        "시뮬레이크럼 - 래더",
        'Simulacre EC',
        'Simulacro EE',
    ), (
        "Pillars of Gold LE",
        "Золотые столпы РВ",
        '黄金之柱-天梯版',
        "Piliers d'or EC",
        '필러스 오브 골드 - 래더',
        'Pilares de Ouro LE',
        '黃金之柱 - 天梯版',
        "Złote Filary ER",
        "Goldene Säulen LE",
    ), (
        "Submarine LE",
        '潜水艇-天梯版',
        "Подводный мир РВ",
        "Sous-marin EC",
        '서브머린 - 래더',
        'Submarino LE',
        "潛水艇 - 天梯版",
        "Podwodny Świat ER",
    ), (
        "Deathaura LE",
        "Todesaura LE",
        '死亡光环-天梯版',
        '死亡光環 - 天梯版',
        "Aura de mort EC",
        '데스오라 - 래더',
        'Aura da Morte LE',
        "Aura Śmierci ER",
        "Аура смерти РВ",
    ), (
        "Ice and Chrome LE",
        '冰雪合金-天梯版',
        'Лед и хром РВ',
        "Glace et chrome EC",
        '아이스 앤 크롬 - 래더',
    ), (
        "Lightshade LE",
        "光影交错-天梯版",
        "光與影 - 天梯版",
        "라이트쉐이드 - 래더",
        "Lueur nocturne EC",
        "Luces y sombras EE",
        "Светотень РВ",
    ), (
        "Romanticide LE",
        "Romanticide EC",
        "Romanticídio LE",
        "Romanticidio EE",
        "Romantizid LE",
        "Romantyzm ER",
        "Романтицид РВ",
        "紫晶浪漫-天梯版",
        "羅曼死 - 天梯版",
        "로맨티사이드 - 래더",
    ), (
        "Oxide LE",
        "Óxido EE",
        "Оксид РВ",
        "锈化山巅-天梯版",
        "氧化物質 - 天梯版",
        "Oxid LE",
        "옥사이드 - 래더",
    ), (
        "Jagannatha LE",
        '世界主宰-天梯版',
        "札格納特 - 天梯版",
        "Jagannatha EC",
        "Jagannatha ER",
        "Яганната РВ",
        "자가나타 - 래더",
        "Jagannatha",
    ), (
        "2000 Atmospheres LE",
        "2000 Atmósferas EE",
        "2000 атмосфер РВ",
        "2000大氣壓力 - 天梯版",
        "大气2000-天梯版",
        "2000 애트모스피어 - 래더",
    ), (
        "Beckett Industries LE",
        "베케트 인더스트리즈 - 래더",
        "贝克特工业-天梯版",
    ), (
        "Blackburn LE",
        "블랙번 - 래더",
        "黑色燃烧-天梯版",
        "Блэкберн РВ",
    ),
)

MAP_LOOKUP = {}
for tup in MAPS:
    for map_name in tup:
        MAP_LOOKUP[map_name] = tup[0]

def get_replay_filenames(path):
    assert path.exists(), path
    for root, dirs, files in os.walk(path):
        for name in files:
            if name.endswith('.SC2Replay'):
                yield os.path.join(root, name)

def update_mtimes():
    for filename in get_replay_filenames(REPLAY_DIR):
        print(filename)
        try:
            replay_details = extract_replay_details(filename)
        except:
            continue
        utc_timestamp = replay_details['utc_timestamp']
        os.utime(filename, times=(utc_timestamp, utc_timestamp))

def get_replay_filenames_sorted_by_timestamp(path):
    return sorted(
        get_replay_filenames(path),
        key=lambda filename: os.stat(filename).st_mtime)

                
def get_header_from_replay(replay_file_name):
    try:
        archive = mpyq.MPQArchive(replay_file_name)
    except:
        print("issue opening file: {}".format(replay_file_name))
        raise
    contents = archive.header['user_data_header']['content']
    return versions.latest().decode_replay_header(contents)

def get_data_from_replay(replay_file_name, internal_filename, extractor_func):
    try:
        archive = mpyq.MPQArchive(replay_file_name)
    except:
        print("issue opening file: {}".format(replay_file_name))
        raise
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
        81102: 81009,
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

def get_replay_gamemetadata_json(replay_file_name):
    return get_data_from_replay(
        replay_file_name, 'replay.gamemetadata.json',
        lambda protocol, contents: protocol.decode_replay_(contents))


PLAYER_SETUP_EVENT_NAME = 'NNet.Replay.Tracker.SPlayerSetupEvent'
def get_player_setup_events(filename):
    return tuple(itertools.takewhile(
        lambda event: event["_event"] == PLAYER_SETUP_EVENT_NAME,
        itertools.dropwhile(
            lambda event: event["_event"] != PLAYER_SETUP_EVENT_NAME,
            get_replay_tracker_events_gen(filename)
        )))

def get_starting_positions(filename):
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
    return starting_positions

def extract_replay_details(filename):
    # first, get names of actual people playing, which is stored in
    # replay_details (replay_initdata has observers, though maybe you
    # can actually use it as a source of truth still if you look at
    # the "customInterface" flag?
    header = get_header_from_replay(filename)
    base_build = header['m_version']['m_baseBuild']
    elapsed_gameloops = header['m_elapsedGameLoops']
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
        player_id = e['m_playerId']
        slot_id = e['m_slotId']
        type_ = e['m_type']
        # type == 1 might be real players
        user_id = e['m_userId'] # same as slot_id, is the player id in replay_game_events
        player_info = player_lookup_by_list_id[i]
        # slot id is usually the same as working_slot_id, but it's kinda weird sometimes it looks like
        if player_info["game_events_id"] != user_id:
            print(player_setup_events)
            assert False
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

    starting_positions = get_starting_positions(filename)
    
    return {
        "vs_label": " vs ".join(vs_label_builder),
        "result": "-".join(result_builder),
        "map_title": map_title,
        "player_lookup_by_name": player_lookup,
        "utc_timestamp": unix_ts,
        "local_timestamp": local_ts,
        "starting_pos_by_ctrlPID": starting_positions,
        "elapsed_gameloops": elapsed_gameloops,
        "base_build": base_build,
    }

EVENT_WHITELIST_DICT = {
    "NNet.Replay.Tracker.SUnitBornEvent": "UnitBorn",
    "NNet.Replay.Tracker.SUnitInitEvent": "UnitInit",
    "NNet.Replay.Tracker.SUnitDoneEvent": "UnitDone",
    "NNet.Replay.Tracker.SUnitDiedEvent": "UnitDied",
    "NNet.Replay.Tracker.SUpgradeEvent": "Upgrade",
    "NNet.Replay.Tracker.SPlayerStatsEvent": "Stats",
}
def get_tracker_events_rows(filename, replay_id):
    unit_lookup = {}
    rows = []
    counter = collections.defaultdict(int)
    starting_positions = get_starting_positions(filename)
    
    for event_no, e in enumerate(get_replay_tracker_events_gen(filename)):
        event_name = e["_event"]
        if event_name not in EVENT_WHITELIST_DICT:
            continue
        entity_name = None
        true_player_id = None
        unit_tag_index = e.get("m_unitTagIndex")
        unit_tag_recycle = e.get("m_unitTagRecycle")
        unit_id = (unit_tag_index, unit_tag_recycle)
        unit_type_name = e.get("m_unitTypeName")
        if unit_type_name is not None:
            unit_type_name = unit_type_name.decode('utf-8')
            true_player_id = e["m_controlPlayerId"]
            entity_name = unit_type_name
            unit_lookup[unit_id] = (true_player_id, entity_name)
        if unit_tag_index is not None and unit_type_name is None:
            true_player_id, entity_name = unit_lookup[unit_id]
        creator_ability_name = e.get("m_creatorAbilityName")
        if creator_ability_name is not None:
            creator_ability_name = creator_ability_name.decode('utf-8')
        upgrade_type_name = e.get('m_upgradeTypeName')
        if upgrade_type_name is not None:
            upgrade_type_name = upgrade_type_name.decode('utf-8')
            true_player_id = e['m_playerId']
            entity_name = upgrade_type_name
        if entity_name is not None and entity_name.startswith(('Beacon', 'Spray', 'GameHeart', 'Reward')):
            continue
        key = (EVENT_WHITELIST_DICT[event_name], true_player_id, entity_name)
        counter[key] += 1
        x, y = e.get("m_x"), e.get("m_y")
        squared_dist = None
        if x is not None and y is not None and true_player_id != 0:
            if true_player_id not in starting_positions:
                print(starting_positions)
                print(filename, replay_id)
                assert False
            x_home, y_home = starting_positions[true_player_id]
            squared_dist = (x-x_home)**2 + (y-y_home)**2

        row = {
            'replay_id': replay_id,
            'event_no': event_no,
            'event_name': EVENT_WHITELIST_DICT[event_name],
            'event_id': e["_eventid"],
            'gameloop': e["_gameloop"],
            'bits': e["_bits"],
            'unit_tag_index': unit_tag_index,
            'unit_tag_recycle': unit_tag_recycle,
            'unit_type_name': unit_type_name,
            'control_player_id': e.get("m_controlPlayerId"),
            'upkeep_player_id': e.get("m_upkeepPlayerId"),
            'x': e.get("m_x"),
            'y': e.get("m_y"),
            'creator_unit_tag_index': e.get("m_creatorUnitTagIndex"),
            'creator_unit_tag_recycle': e.get("m_creatorUnitTagRecycle"),
            'creator_ability_name': creator_ability_name,
            'killer_player_id': e.get("m_killerPlayerId"),
            'killer_unit_tag_index': e.get("m_killerUnitTagIndex"),
            'killer_unit_tag_recycle': e.get("m_killerUnitTagRecycle"),
            'count': e.get('m_count'),
            'player_id': e.get('m_playerId'),
            'upgrade_type_name': upgrade_type_name,
            'stats': e.get('m_stats'),
            'true_player_id': true_player_id,
            'entity_name': entity_name,
            'nth_event': counter[key],
            'squared_dist_from_home': squared_dist,
        }
        rows.append(row)
    return rows

def populate_db_with_replay(filename):
    engine = get_engine()
    m = hashlib.sha256()
    with open(filename, 'rb') as f:
        m.update(f.read())
    sha256 = m.hexdigest()
    existing_row = get_replays_row_by_sha256(engine, sha256)
    if existing_row:
        return

    try:
        replay_details = extract_replay_details(filename)
    except:
        return
    if all(player_info["game_events_id"] is None for player_info in replay_details["player_lookup_by_name"].values()):
        return
    if len(replay_details["player_lookup_by_name"]) != 2:
        return
    elapsed_gameloops = replay_details['elapsed_gameloops']
    base_build = replay_details['base_build']
    map_name = replay_details['map_title']
    if map_name not in MAP_LOOKUP:
        print(map_name)
    else:
        map_name = MAP_LOOKUP[map_name]
    utc_ts = replay_details['utc_timestamp']
    local_ts = replay_details['local_timestamp']
    path = filename

        
    with engine.begin() as conn:
        replay_id = insert_replays_row(conn, elapsed_gameloops, base_build, map_name, utc_ts, local_ts, path, sha256)
        player_rows = [{
            'replay_id': replay_id,
            'clan': player_info["clan"],
            'name': player_info["name"],
            'race': player_info["race"],
            'result': player_info["result"],
            'player_list_id': player_info["player_list_id"],
            'team_id': player_info["team_id"],
            'working_set_slot_id': player_info["working_set_slot_id"],
            'game_events_id': player_info["game_events_id"],
            'tracker_events_id': player_info["tracker_events_id"],
            'slot_id': player_info["slot_id"],
        } for player_info in replay_details["player_lookup_by_name"].values()]
        insert_replays_players_rows(conn, player_rows)
        insert_replays_tracker_events_rows(conn, get_tracker_events_rows(filename, replay_id))

def main():
    for replay_filename in get_replay_filenames_sorted_by_timestamp(REPLAY_DIR):
        print("processing {}".format(replay_filename))
        populate_db_with_replay(replay_filename)
    return 0

if __name__ == "__main__":
    status = main()
    sys.exit(status)
