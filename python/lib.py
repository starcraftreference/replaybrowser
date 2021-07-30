def replays_with_units(unit_thresholds, seconds):
    pass

# ./search.py --matchup=TvP (Proxy)Unit/Upgrade:qty:(init):(by_time)
# ./search.py (Proxy)Unit/Upgrade:qty:(init):(by_time)
# ./search.py ProxyPhotonCannon:1:init:180
# results:
#   1243, 2021-07-27 01:43:28, 12:10, TvP, maru, *Prince, Submarine LE, 2:46

"""
SELECT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'PhotonCannon'
   AND squared_dist_from_home > 70
   AND nth_event = 1
   AND is_init
   AND gameloop < by_time*22.4;


SELECT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'PhotonCannon'
   AND squared_dist_from_home > 70
   AND nth_event = 1
   AND event_name = 'UnitInit'
   AND gameloop < 180*22.4;

CREATE INDEX build_index ON replays_tracker_events (entity_name, nth_event, event_name);


WITH t AS (
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'CommandCenter'
   AND nth_event = 1
   AND event_name = 'UnitDone'
   AND gameloop < 180*22.4
INTERSECT
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'Marine'
   AND nth_event = 7
   AND event_name IN ('UnitBorn', 'UnitDone', 'UpgradeDone')
   AND gameloop < 300*22.4
INTERSECT
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'Medivac'
   AND nth_event = 1
   AND event_name IN ('UnitBorn', 'UnitDone', 'UpgradeDone')
   AND gameloop < 250*22.4
INTERSECT
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'WidowMine'
   AND nth_event = 3
   AND event_name IN ('UnitBorn', 'UnitDone', 'UpgradeDone')
   AND gameloop < 250*22.4
)
SELECT replays.id, elapsed_gameloops, map, to_timestamp(utc_ts), clan, name, race, tracker_events_id, substring(path FROM 43) FROM replays, replays_players, t WHERE replays.id = replays_players.replay_id AND replays.id = t.replay_id
ORDER BY utc_ts DESC;
"""



"""
WITH t AS (
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'CommandCenter'
   AND nth_event = 1
   AND event_name IN ('UnitBorn', 'UnitDone', 'UpgradeDone')
   AND gameloop < 180*22.4
)
SELECT replays.id, elapsed_gameloops, map, utc_ts, clan, name, race, tracker_events_id, substring(path FROM 43) FROM replays, replays_players, t WHERE replays.id = replays_players.replay_id AND replays.id = t.replay_id
ORDER BY utc_ts DESC;


WITH t AS (
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'Hellion'
   AND nth_event = 2
   AND event_name = 'UnitBorn'
   AND gameloop < 200*22.4
INTERSECT
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'Bunker'
   AND nth_event = 1
   AND event_name IN ('UnitBorn', 'UnitDone', 'UpgradeDone')
   AND gameloop < 180*22.4
)
SELECT replays.id, elapsed_gameloops, map, utc_ts, clan, name, race, tracker_events_id, substring(path FROM 43) FROM replays, replays_players, t WHERE replays.id = replays_players.replay_id AND replays.id = t.replay_id
ORDER BY utc_ts DESC;
"""



"""
WITH t AS (
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'CommandCenter'
   AND nth_event = 1
   AND event_name IN ('UnitBorn', 'UnitDone', 'UpgradeDone')
   AND gameloop < 180*22.4
)
SELECT replays.id, elapsed_gameloops, map, utc_ts, clan, name, race, tracker_events_id, substring(path FROM 43) FROM replays, replays_players, t WHERE replays.id = replays_players.replay_id AND replays.id = t.replay_id
ORDER BY utc_ts DESC;


"""

"""
WITH t AS (
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'VoidRay'
   AND nth_event = 1
   AND event_name IN ('UnitBorn', 'UnitDone', 'UpgradeDone')
   AND gameloop < 195*22.4
INTERSECT
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'Zealot'
   AND nth_event = 1
   AND event_name IN ('UnitBorn', 'UnitDone', 'UpgradeDone')
   AND gameloop < 195*22.4
INTERSECT
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'Adept'    
   AND nth_event = 1
   AND event_name IN ('UnitBorn', 'UnitDone', 'UpgradeDone')
   AND gameloop < 195*22.4
)        
SELECT replays.id, elapsed_gameloops, map, to_timestamp(utc_ts), clan, name, race, substring(path FROM 43) FROM replays, replays_players, t WHERE replays.id = replays_players.replay_id AND replays.id = t.replay_id
ORDER BY utc_ts DESC;

WITH t AS (
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'VoidRay'
   AND nth_event = 1
   AND event_name IN ('UnitBorn', 'UnitDone', 'UpgradeDone')
   AND gameloop < 195*22.4
)
SELECT replays.id, elapsed_gameloops, map, to_timestamp(utc_ts), clan, name, race, substring(path FROM 43) FROM replays, replays_players, t WHERE replays.id = replays_players.replay_id AND replays.id = t.replay_id
ORDER BY utc_ts DESC;


"""

"""
WITH t AS (
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'VoidRay'
   AND nth_event = 1
   AND event_name IN ('UnitBorn', 'UnitDone', 'UpgradeDone')
   AND gameloop < 195*22.4
INTERSECT
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'Zealot'
   AND nth_event = 1
   AND event_name IN ('UnitBorn', 'UnitDone', 'UpgradeDone')
   AND gameloop < 195*22.4
INTERSECT
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'Adept'    
   AND nth_event = 1
   AND event_name IN ('UnitBorn', 'UnitDone', 'UpgradeDone')
   AND gameloop < 195*22.4
)        
SELECT replays.id, elapsed_gameloops, map, to_timestamp(utc_ts), clan, name, race, substring(path FROM 43) FROM replays, replays_players, t WHERE replays.id = replays_players.replay_id AND replays.id = t.replay_id
ORDER BY utc_ts DESC;

WITH t AS (
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'RoachWarren'
   AND nth_event = 1
   AND event_name IN ('UnitBorn', 'UnitDone', 'UpgradeDone')
   AND gameloop < 120*22.4
)
SELECT replays.id, elapsed_gameloops, map, to_timestamp(utc_ts), clan, name, race, substring(path FROM 44) FROM replays, replays_players, t WHERE replays.id = replays_players.replay_id AND replays.id = t.replay_id
ORDER BY utc_ts DESC;

"""
"""
medivac and 3 mines by 4:03
7 marines
cc
"""

"""
SELECT replay_id FROM replays_players WHERE 
"""

"""
WITH t AS (
  SELECT replay_id, string_agg(name || ' (' || LEFT(race, 1) || ')', ' vs ') AS vs_str
  FROM replays_players
  GROUP BY replay_id
)
SELECT replays.id, vs_str, CONCAT(elapsed_gameloops/22.4, ' seconds')::interval, map, to_timestamp(utc_ts) at time zone 'UTC', substring(path FROM 44) from replays, t WHERE replays.id = t.replay_id AND path ILIKE '%trap%' ORDER BY utc_ts DESC;
"""
