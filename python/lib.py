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
),
t2 AS (
  SELECT replay_id, string_agg(name || ' (' || LEFT(race, 1) || ')' || translate(to_char(result, '9'), '12', '*'),  ' vs ') AS vs_str, string_agg(DISTINCT LEFT(race,1),'') AS races
  FROM replays_players
  GROUP BY replay_id
)
SELECT replays.id, CONCAT(elapsed_gameloops/22.4, ' seconds')::interval AS length, map, to_timestamp(utc_ts) AS timestamp, vs_str, substring(path FROM 43) AS path
FROM replays, t, t2
WHERE replays.id = t2.replay_id AND replays.id = t.replay_id
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

"""
WITH
t1 AS (SELECT replay_id, true_player_id, COUNT(*) FROM replays_tracker_events WHERE event_name = 'UnitDone' AND entity_name = 'Nexus' GROUP BY replay_id, true_player_id HAVING COUNT(*) >= 3),
t2 AS (
  SELECT replay_id, string_agg(name || ' (' || LEFT(race, 1) || ')', ' vs ') AS vs_str, string_agg(DISTINCT LEFT(race,1),'') AS races
  FROM replays_players
  GROUP BY replay_id
)
SELECT replays.id, vs_str, races, CONCAT(elapsed_gameloops/22.4, ' seconds')::interval, map, to_timestamp(utc_ts) at time zone 'UTC', substring(path FROM 44) FROM replays, t1, t2 WHERE replays.id = t1.replay_id AND replays.id = t2.replay_id ORDER BY utc_ts DESC;




WITH
t1 AS (
  SELECT DISTINCT replay_id, true_player_id
  FROM replays_tracker_events
  WHERE
    event_name = 'UnitDone' AND entity_name = 'PhotonCannon' AND gameloop < 120*22.4),
t2 AS (
  SELECT replay_id, string_agg(name || ' (' || LEFT(race, 1) || ')', ' vs ') AS vs_str, string_agg(DISTINCT LEFT(race,1),'') AS races
  FROM replays_players
  GROUP BY replay_id
)
SELECT replays.id, vs_str, races, CONCAT(elapsed_gameloops/22.4, ' seconds')::interval, map, to_timestamp(utc_ts) at time zone 'UTC', substring(path FROM 44) FROM replays, t1, t2 WHERE replays.id = t1.replay_id AND replays.id = t2.replay_id AND races='P' ORDER BY utc_ts DESC;
"""

"""
WITH t AS (
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'Zealot'
   AND nth_event = 6
   AND event_name IN ('UnitBorn', 'UnitDone', 'UpgradeDone')
   AND gameloop < 300*22.4
)        
SELECT replays.id, CONCAT(elapsed_gameloops/22.4, ' seconds')::interval AS length, map, to_timestamp(utc_ts) AS timestamp, vs_str, substring(path FROM 43) AS path
FROM replays, replays_players, t
WHERE replays.id = replays_players.replay_id AND replays.id = t.replay_id
ORDER BY utc_ts DESC;
"""


def select_proxy_hatch():
    query = """
WITH t AS (
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'Hatchery'
   AND squared_dist_from_home > 4900
   AND event_name IN ('UnitInit', UnitBorn', 'UnitDone', 'UpgradeDone')
   AND gameloop < 180*22.4
),
t2 AS (
  SELECT replay_id, string_agg(name || ' (' || LEFT(race, 1) || ')' || (CASE WHEN result = 1 THEN '*' ELSE ''), ' vs ') AS vs_str, string_agg(DISTINCT LEFT(race,1),'') AS races
  FROM replays_players
  GROUP BY replay_id
)
SELECT replays.id, CONCAT(elapsed_gameloops/22.4, ' seconds')::interval, map, to_timestamp(utc_ts), vs_str, substring(path FROM 43) FROM replays, t2 WHERE replays.id = t2.replay_id
ORDER BY utc_ts DESC;
    
    """

"""
WITH t AS (
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'Hatchery'
   AND squared_dist_from_home > 4900
   AND event_name IN ('UnitInit', 'UnitBorn', 'UnitDone', 'UpgradeDone')
   AND gameloop < 180*22.4
),
t2 AS (
  SELECT replay_id, string_agg(name || ' (' || LEFT(race, 1) || ')', ' vs ') AS vs_str, string_agg(DISTINCT LEFT(race,1),'') AS races
  FROM replays_players
  GROUP BY replay_id
)
SELECT replays.id, CONCAT(elapsed_gameloops/22.4, ' seconds')::interval AS length, map, to_timestamp(utc_ts) AS timestamp, vs_str, substring(path FROM 43) AS path
FROM replays, t, t2
WHERE replays.id = t2.replay_id AND replays.id = t.replay_id AND vs_str LIKE '%(T)%'
ORDER BY utc_ts DESC;
"""

    return None


"""
WITH t AS (
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'Marine'
   AND nth_event = 1
   AND event_name IN ('UnitBorn', 'UnitDone', 'UpgradeDone')
   AND gameloop < 195*22.4
INTERSECT
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'Reaper'
   AND nth_event = 2
   AND event_name IN ('UnitBorn', 'UnitDone', 'UpgradeDone')
   AND gameloop < 195*22.4
),
t2 AS (
  SELECT replay_id, string_agg(name || ' (' || LEFT(race, 1) || ')' || translate(to_char(result, '9'), '12', '*'),  ' vs ') AS vs_str, string_agg(DISTINCT LEFT(race,1),'') AS races
  FROM replays_players
  GROUP BY replay_id
)
SELECT replays.id, CONCAT(elapsed_gameloops/22.4, ' seconds')::interval AS length, map, to_timestamp(utc_ts) AS timestamp, vs_str, substring(path FROM 43) AS path
FROM replays, t, t2
WHERE replays.id = t2.replay_id AND replays.id = t.replay_id
ORDER BY utc_ts DESC;
"""

"""
WITH t AS (
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'Banshee'
   AND nth_event = 2
   AND event_name IN ('UnitBorn', 'UnitDone', 'UpgradeDone')
   AND gameloop < 320*22.4
INTERSECT
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'SiegeTank'
   AND nth_event = 2
   AND event_name IN ('UnitBorn', 'UnitDone', 'UpgradeDone')
   AND gameloop < 320*22.4
),
t2 AS (
  SELECT replay_id, string_agg(name || ' (' || LEFT(race, 1) || ')' || translate(to_char(result, '9'), '12', '*'),  ' vs ') AS vs_str, string_agg(DISTINCT LEFT(race,1),'') AS races
  FROM replays_players
  GROUP BY replay_id
)
SELECT replays.id, CONCAT(elapsed_gameloops/22.4, ' seconds')::interval AS length, map, to_timestamp(utc_ts) AS timestamp, vs_str, substring(path FROM 43) AS path
FROM replays, t, t2
WHERE replays.id = t2.replay_id AND replays.id = t.replay_id
ORDER BY utc_ts DESC;
"""

"""
WITH t AS (
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'Barracks'
   AND nth_event = 3
   AND event_name IN ('UnitBorn', 'UnitDone', 'UpgradeDone')
   AND gameloop < 330*22.4
INTERSECT
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'Factory'
   AND nth_event = 1
   AND event_name IN ('UnitBorn', 'UnitDone', 'UpgradeDone')
   AND gameloop < 180*22.4
INTERSECT
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'Medivac'
   AND nth_event = 1
   AND event_name IN ('UnitBorn', 'UnitDone', 'UpgradeDone')
   AND gameloop < 330*22.4
INTERSECT
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'WidowMine'
   AND nth_event = 3
   AND event_name IN ('UnitBorn', 'UnitDone', 'UpgradeDone')
   AND gameloop < 330*22.4
),
t2 AS (
  SELECT replay_id, string_agg(name || ' (' || LEFT(race, 1) || ')' || translate(to_char(result, '9'), '12', '*'),  ' vs ') AS vs_str, string_agg(DISTINCT LEFT(race,1),'') AS races
  FROM replays_players
  GROUP BY replay_id
)
SELECT replays.id, CONCAT(elapsed_gameloops/22.4, ' seconds')::interval AS length, map, to_timestamp(utc_ts) AS timestamp, vs_str, substring(path FROM 43) AS path
FROM replays, t, t2
WHERE replays.id = t2.replay_id AND replays.id = t.replay_id
ORDER BY utc_ts DESC;
"""



"""
WITH t AS (
SELECT DISTINCT replay_id
FROM replays_tracker_events
WHERE
   entity_name = 'Barracks'
   AND nth_event = 3
   AND event_name IN ('UnitBorn', 'UnitDone', 'Upgrade')
   AND gameloop < 210*22.4
),
t2 AS (
  SELECT replay_id, string_agg(name || ' (' || LEFT(race, 1) || ')' || translate(to_char(result, '9'), '12', '*'),  ' vs ') AS vs_str, string_agg(DISTINCT LEFT(race,1),'') AS races
  FROM replays_players
  GROUP BY replay_id
)
SELECT replays.id, CONCAT(elapsed_gameloops/22.4, ' seconds')::interval AS length, map, to_timestamp(utc_ts) AS timestamp, vs_str, substring(path FROM 43) AS path
FROM replays, t, t2
WHERE replays.id = t2.replay_id AND replays.id = t.replay_id
ORDER BY utc_ts DESC;
"""

"""
WITH t AS (
SELECT DISTINCT replay_id
FROM replays_tracker_events
WHERE
   entity_name = 'Barracks'
   AND nth_event = 3
   AND event_name IN ('UnitBorn', 'UnitDone', 'Upgrade')
   AND gameloop < 210*22.4
INTERSECT
SELECT DISTINCT replay_id
FROM replays_tracker_events
WHERE
   entity_name = 'BlinkTech'
   AND nth_event = 1
   AND event_name IN ('UnitBorn', 'UnitDone', 'Upgrade')
   AND gameloop < 330*22.4
INTERSECT
SELECT DISTINCT replay_id
FROM replays_tracker_events
WHERE
   entity_name = 'Gateway'
   AND nth_event = 4
   AND event_name IN ('UnitBorn', 'UnitDone', 'Upgrade')
   AND gameloop < 330*22.4

),
t2 AS (
  SELECT replay_id, string_agg(name || ' (' || LEFT(race, 1) || ')' || translate(to_char(result, '9'), '12', '*'),  ' vs ') AS vs_str, string_agg(DISTINCT LEFT(race,1),'') AS races
  FROM replays_players
  GROUP BY replay_id
)
SELECT replays.id, CONCAT(elapsed_gameloops/22.4, ' seconds')::interval AS length, map, to_timestamp(utc_ts) AS timestamp, vs_str, substring(path FROM 43) AS path
FROM replays, t, t2
WHERE replays.id = t2.replay_id AND replays.id = t.replay_id
ORDER BY utc_ts DESC;
"""

"""
WITH t AS (
SELECT DISTINCT replay_id
FROM replays_tracker_events
WHERE
   entity_name = 'MissileTurret'
   AND nth_event = 1
   AND event_name IN ('UnitBorn', 'UnitDone', 'Upgrade')
   AND gameloop < 240*22.4
INTERSECT
SELECT DISTINCT replay_id
FROM replays_tracker_events
WHERE
   entity_name = 'VoidRay'
   AND nth_event = 1
   AND event_name IN ('UnitBorn', 'UnitDone', 'Upgrade')
   AND gameloop < 210*22.4
),
t2 AS (
  SELECT replay_id, string_agg(name || ' (' || LEFT(race, 1) || ')' || translate(to_char(result, '9'), '12', '*'),  ' vs ') AS vs_str, string_agg(DISTINCT LEFT(race,1),'') AS races
  FROM replays_players
  GROUP BY replay_id
)
SELECT replays.id, CONCAT(elapsed_gameloops/22.4, ' seconds')::interval AS length, map, to_timestamp(utc_ts) AS timestamp, vs_str, substring(path FROM 43) AS path
FROM replays, t, t2
WHERE replays.id = t2.replay_id AND replays.id = t.replay_id
ORDER BY utc_ts DESC;
"""


"""
WITH t AS (
SELECT DISTINCT replay_id
FROM replays_tracker_events
WHERE
   entity_name = 'Colossus'
   AND nth_event = 6
   AND event_name IN ('UnitBorn', 'UnitDone', 'Upgrade')
   AND creator_ability_name != 'HallucinationColossus'
),
t2 AS (
  SELECT replay_id, string_agg(name || ' (' || LEFT(race, 1) || ')' || translate(to_char(result, '9'), '12', '*'),  ' vs ') AS vs_str, string_agg(DISTINCT LEFT(race,1),'') AS races
  FROM replays_players
  GROUP BY replay_id
)
SELECT replays.id, CONCAT(elapsed_gameloops/22.4, ' seconds')::interval AS length, map, to_timestamp(utc_ts) AS timestamp, vs_str, substring(path FROM 43) AS path
FROM replays, t, t2
WHERE replays.id = t2.replay_id AND replays.id = t.replay_id
ORDER BY utc_ts DESC;
"""


"""
WITH t AS (
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'Gateway'
   AND nth_event = 4
   AND event_name IN ('UnitBorn', 'UnitDone', 'UpgradeDone')
   AND gameloop < 300*22.4
INTERSECT
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'Stalker'
   AND nth_event = 8
   AND event_name IN ('UnitBorn', 'UnitDone', 'UpgradeDone')
   AND gameloop < 360*22.4
INTERSECT
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'BlinkTech'
   AND nth_event = 1
   AND event_name IN ('UnitBorn', 'UnitDone', 'Upgrade')
   AND gameloop < 330*22.4
),
t2 AS (
  SELECT replay_id, string_agg(name || ' (' || LEFT(race, 1) || ')' || translate(to_char(result, '9'), '12', '*'),  ' vs ') AS vs_str, string_agg(DISTINCT LEFT(race,1),'') AS races
  FROM replays_players
  GROUP BY replay_id
)
SELECT replays.id, CONCAT(elapsed_gameloops/22.4, ' seconds')::interval AS length, map, to_timestamp(utc_ts) AS timestamp, vs_str, substring(path FROM 43) AS path
FROM replays, t, t2
WHERE replays.id = t2.replay_id AND replays.id = t.replay_id
ORDER BY utc_ts DESC;
"""

"""
WITH t AS (
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'WidowMine'
   AND nth_event = 3
   AND event_name IN ('UnitBorn', 'UnitDone', 'UpgradeDone')
   AND gameloop < 240*22.4
INTERSECT
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'Medivac'
   AND nth_event = 1
   AND event_name IN ('UnitBorn', 'UnitDone', 'UpgradeDone')
   AND gameloop < 240*22.4
INTERSECT
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'Armory'
   AND nth_event = 1
   AND event_name IN ('UnitBorn', 'UnitDone', 'UpgradeDone')
   AND gameloop < 240*22.4
INTERSECT
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'Thor'
   AND nth_event = 1
   AND event_name IN ('UnitBorn', 'UnitDone', 'UpgradeDone')
   AND gameloop < 300*22.4
),
t2 AS (
  SELECT replay_id, string_agg(name || ' (' || LEFT(race, 1) || ')' || translate(to_char(result, '9'), '12', '*'),  ' vs ') AS vs_str, string_agg(DISTINCT LEFT(race,1),'') AS races
  FROM replays_players
  GROUP BY replay_id
)
SELECT replays.id, CONCAT(elapsed_gameloops/22.4, ' seconds')::interval AS length, map, to_timestamp(utc_ts) AS timestamp, vs_str, substring(path FROM 43) AS path
FROM replays, t, t2
WHERE replays.id = t2.replay_id AND replays.id = t.replay_id
ORDER BY utc_ts DESC;
"""

"""
WITH t AS (
SELECT DISTINCT replay_id
FROM replays_tracker_events
WHERE
   entity_name = 'WidowMine'
   AND nth_event = 3
   AND event_name IN ('UnitBorn', 'UnitDone', 'UpgradeDone')
   AND gameloop < 300*22.4
INTERSECT
SELECT DISTINCT replay_id
FROM replays_tracker_events
WHERE
   entity_name = 'Medivac'
   AND nth_event = 1
   AND event_name IN ('UnitBorn', 'UnitDone', 'UpgradeDone')
   AND gameloop < 300*22.4
INTERSECT
SELECT DISTINCT replay_id
FROM replays_tracker_events
WHERE
   entity_name = 'Barracks'
   AND nth_event = 3
   AND event_name IN ('UnitBorn', 'UnitDone', 'UpgradeDone')
   AND gameloop < 300*22.4
INTERSECT
SELECT DISTINCT replay_id
FROM replays_tracker_events
WHERE
   entity_name = 'Gateway'
   AND nth_event = 4
   AND event_name IN ('UnitBorn', 'UnitDone', 'UpgradeDone')
   AND gameloop < 300*22.4
INTERSECT
SELECT DISTINCT replay_id
FROM replays_tracker_events
WHERE
   entity_name = 'Stalker'
   AND nth_event = 8
   AND event_name IN ('UnitBorn', 'UnitDone', 'UpgradeDone')
   AND gameloop < 360*22.4

),
t2 AS (
  SELECT replay_id, string_agg(name || ' (' || LEFT(race, 1) || ')' || translate(to_char(result, '9'), '12', '*'),  ' vs ') AS vs_str, string_agg(DISTINCT LEFT(race,1),'') AS races
  FROM replays_players
  GROUP BY replay_id
)
SELECT replays.id, CONCAT(elapsed_gameloops/22.4, ' seconds')::interval AS length, map, to_timestamp(utc_ts) AS timestamp, vs_str, substring(path FROM 43) AS path
FROM replays, t, t2
WHERE replays.id = t2.replay_id AND replays.id = t.replay_id
ORDER BY utc_ts DESC;
"""


"""
WITH t AS (
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'SiegeTank'
   AND nth_event = 1
   AND event_name IN ('UnitBorn', 'UnitDone', 'UpgradeDone')
   AND gameloop < 225*22.4
INTERSECT
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'VikingFighter'
   AND nth_event = 1
   AND event_name IN ('UnitBorn', 'UnitDone', 'UpgradeDone')
   AND gameloop < 225*22.4
),
t2 AS (
  SELECT replay_id, string_agg(name || ' (' || LEFT(race, 1) || ')' || translate(to_char(result, '9'), '12', '*'),  ' vs ') AS vs_str, string_agg(DISTINCT LEFT(race,1),'') AS races
  FROM replays_players
  GROUP BY replay_id
)
SELECT replays.id, CONCAT(elapsed_gameloops/22.4, ' seconds')::interval AS length, map, to_timestamp(utc_ts) AS timestamp, vs_str, substring(path FROM 43) AS path
FROM replays, t, t2
WHERE replays.id = t2.replay_id AND replays.id = t.replay_id
ORDER BY utc_ts DESC;
"""

"""
WITH t AS (
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'Spire'
   AND nth_event = 1
   AND event_name IN ('UnitBorn', 'UnitDone', 'UpgradeDone')
   AND gameloop < 360*22.4
INTERSECT
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'Zergling'
   AND nth_event = 10
   AND event_name IN ('UnitBorn', 'UnitDone', 'UpgradeDone')
   AND gameloop < 240*22.4
),
t2 AS (
  SELECT replay_id, string_agg(name || ' (' || LEFT(race, 1) || ')' || translate(to_char(result, '9'), '12', '*'),  ' vs ') AS vs_str, string_agg(DISTINCT LEFT(race,1),'') AS races
  FROM replays_players
  GROUP BY replay_id
)
SELECT replays.id, CONCAT(elapsed_gameloops/22.4, ' seconds')::interval AS length, map, to_timestamp(utc_ts) AS timestamp, vs_str, substring(path FROM 43) AS path
FROM replays, t, t2
WHERE replays.id = t2.replay_id AND replays.id = t.replay_id
ORDER BY utc_ts DESC;
"""
"""
WITH t AS (
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'Spire'
   AND nth_event = 1
   AND event_name IN ('UnitBorn', 'UnitDone', 'UpgradeDone')
   AND gameloop <= 330*22.4
),
t2 AS (
  SELECT replay_id, string_agg(name || ' (' || LEFT(race, 1) || ')' || translate(to_char(result, '9'), '12', '*'),  ' vs ') AS vs_str, string_agg(DISTINCT LEFT(race,1),'') AS races
  FROM replays_players
  GROUP BY replay_id
)
SELECT replays.id, CONCAT(elapsed_gameloops/22.4, ' seconds')::interval AS length, map, to_timestamp(utc_ts) AS timestamp, vs_str, substring(path FROM 43) AS path
FROM replays, t, t2
WHERE replays.id = t2.replay_id AND replays.id = t.replay_id
ORDER BY utc_ts DESC;
"""


"""
WITH t AS (
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'Nexus'
   AND nth_event = 1
   AND event_name IN ('UnitBorn')
EXCEPT
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'Nexus'
   AND nth_event = 1
   AND event_name IN ('UnitInit')
   AND gameloop <= 120*22.4
),
t2 AS (
  SELECT replay_id, string_agg(name || ' (' || LEFT(race, 1) || ')' || translate(to_char(result, '9'), '12', '*'),  ' vs ') AS vs_str, string_agg(DISTINCT LEFT(race,1),'') AS races
  FROM replays_players
  GROUP BY replay_id
)
SELECT replays.id, CONCAT(elapsed_gameloops/22.4, ' seconds')::interval AS length, map, to_timestamp(utc_ts) AS timestamp, vs_str, substring(path FROM 43) AS path
FROM replays, t, t2
WHERE replays.id = t2.replay_id AND replays.id = t.replay_id AND vs_str LIKE '%(T)%'
ORDER BY utc_ts DESC;
"""


"""
WITH t AS (
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'RoachWarren'
   AND nth_event = 1
   AND event_name IN ('UnitBorn', 'UnitDone')
   AND gameloop <= 180*22.4
),
t2 AS (
  SELECT replay_id, string_agg(name || ' (' || LEFT(race, 1) || ')' || translate(to_char(result, '9'), '12', '*'),  ' vs ') AS vs_str, string_agg(DISTINCT LEFT(race,1),'') AS races
  FROM replays_players
  GROUP BY replay_id
)
SELECT replays.id, CONCAT(elapsed_gameloops/22.4, ' seconds')::interval AS length, map, to_timestamp(utc_ts) AS timestamp, vs_str, substring(path FROM 43) AS path
FROM replays, t, t2
WHERE replays.id = t2.replay_id AND replays.id = t.replay_id AND vs_str LIKE '%(T)%'
ORDER BY utc_ts DESC;
"""


"""
WITH t AS (
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'Factory'
   AND nth_event = 2
   AND event_name IN ('UnitBorn', 'UnitDone')
   AND gameloop <= 12*60*22.4
INTERSECT
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'Barracks'
   AND nth_event = 5
   AND event_name IN ('UnitBorn', 'UnitDone')
),
t2 AS (
  SELECT replay_id, string_agg(name || ' (' || LEFT(race, 1) || ')' || translate(to_char(result, '9'), '12', '*'),  ' vs ') AS vs_str, string_agg(DISTINCT LEFT(race,1),'') AS races
  FROM replays_players
  GROUP BY replay_id
)
SELECT replays.id, CONCAT(elapsed_gameloops/22.4, ' seconds')::interval AS length, map, to_timestamp(utc_ts) AS timestamp, vs_str, substring(path FROM 43) AS path
FROM replays, t, t2
WHERE replays.id = t2.replay_id AND replays.id = t.replay_id AND vs_str LIKE '%(P)%'
ORDER BY utc_ts DESC;
"""


"""
WITH t AS (
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'Factory'
   AND nth_event = 2
   AND event_name IN ('UnitBorn', 'UnitDone')
   AND gameloop <= 540*22.4
),
t2 AS (
  SELECT replay_id, string_agg(name || ' (' || LEFT(race, 1) || ')' || translate(to_char(result, '9'), '12', '*'),  ' vs ') AS vs_str, string_agg(DISTINCT LEFT(race,1),'') AS races
  FROM replays_players
  GROUP BY replay_id
)
SELECT replays.id, CONCAT(elapsed_gameloops/22.4, ' seconds')::interval AS length, map, to_timestamp(utc_ts) AS timestamp, vs_str, substring(path FROM 43) AS path
FROM replays, t, t2
WHERE replays.id = t2.replay_id AND replays.id = t.replay_id AND vs_str LIKE '%(P)%'
ORDER BY utc_ts DESC;
"""


"""
WITH t AS (
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'VoidRay'
   AND nth_event = 1
   AND event_name IN ('UnitBorn', 'UnitDone')
   AND gameloop <= 195*22.4
),
t2 AS (
  SELECT replay_id, string_agg(name || ' (' || LEFT(race, 1) || ')' || translate(to_char(result, '9'), '12', '*'),  ' vs ') AS vs_str, string_agg(DISTINCT LEFT(race,1),'') AS races
  FROM replays_players
  GROUP BY replay_id
)
SELECT replays.id, CONCAT(elapsed_gameloops/22.4, ' seconds')::interval AS length, map, to_timestamp(utc_ts) AS timestamp, vs_str, substring(path FROM 43) AS path
FROM replays, t, t2
WHERE replays.id = t2.replay_id AND replays.id = t.replay_id AND vs_str LIKE '%(T)%'
ORDER BY utc_ts DESC;
"""


"""
WITH t AS (
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'Banshee'
   AND nth_event = 1
   AND event_name IN ('UnitBorn', 'UnitDone')
   AND gameloop <= 4*60*22.4
INTERSECT
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'Hellion'
   AND nth_event = 4
   AND event_name IN ('UnitBorn', 'UnitDone')
   AND gameloop <= 4*60*22.4
),
t2 AS (
  SELECT replay_id, string_agg(name || ' (' || LEFT(race, 1) || ')' || translate(to_char(result, '9'), '12', '*'),  ' vs ') AS vs_str, string_agg(DISTINCT LEFT(race,1),'') AS races
  FROM replays_players
  GROUP BY replay_id
)
SELECT replays.id, CONCAT(elapsed_gameloops/22.4, ' seconds')::interval AS length, map, to_timestamp(utc_ts) AS timestamp, vs_str, substring(path FROM 43) AS path
FROM replays, t, t2
WHERE replays.id = t2.replay_id AND replays.id = t.replay_id AND vs_str LIKE '%(Z)%'
ORDER BY utc_ts DESC;
"""


"""
WITH t AS (
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'Roach'
   AND nth_event = 5
   AND event_name IN ('UnitBorn', 'UnitDone')
   AND gameloop <= 195*22.4
),
t2 AS (
  SELECT replay_id, string_agg(name || ' (' || LEFT(race, 1) || ')' || translate(to_char(result, '9'), '12', '*'),  ' vs ') AS vs_str, string_agg(DISTINCT LEFT(race,1),'') AS races
  FROM replays_players
  GROUP BY replay_id
)
SELECT replays.id, CONCAT(elapsed_gameloops/22.4, ' seconds')::interval AS length, map, to_timestamp(utc_ts) AS timestamp, vs_str, substring(path FROM 43) AS path
FROM replays, t, t2
WHERE replays.id = t2.replay_id AND replays.id = t.replay_id AND vs_str LIKE '%(T)%'
ORDER BY utc_ts DESC;
"""

"""
WITH t AS (
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'Barracks'
   AND nth_event <= 2
   AND event_name IN ('UnitInit')
   AND squared_dist_from_home >= 4900
   AND gameloop <= 3*60*22.4
),
t2 AS (
  SELECT replay_id, string_agg(name || ' (' || LEFT(race, 1) || ')' || translate(to_char(result, '9'), '12', '*'),  ' vs ') AS vs_str, string_agg(DISTINCT LEFT(race,1),'') AS races
  FROM replays_players
  GROUP BY replay_id
)
SELECT replays.id, CONCAT(elapsed_gameloops/22.4, ' seconds')::interval AS length, map, to_timestamp(utc_ts) AS timestamp, vs_str, substring(path FROM 43) AS path
FROM replays, t, t2
WHERE replays.id = t2.replay_id AND replays.id = t.replay_id AND vs_str LIKE '%(P)%' AND map = 'Oxide LE'
ORDER BY utc_ts DESC;
"""

"""
WITH t AS (
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'BarracksReactor'
   AND nth_event = 1
   AND event_name IN ('UnitInit')
   AND gameloop <= (1*60+44+5)*22.4
INTERSECT
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'Barracks'
   AND nth_event = 2
   AND event_name IN ('UnitInit')
   AND gameloop <= (2*60+2+5)*22.4
--   AND gameloop <= 188*22.4
INTERSECT
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'Bunker'
   AND nth_event = 1
   AND event_name IN ('UnitInit')
   AND gameloop <= (2*60+12+5)*22.4
INTERSECT
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'Barracks'
   AND nth_event = 3
   AND event_name IN ('UnitInit')
   AND gameloop <= (2*60+25+15)*22.4
INTERSECT
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'Marauder'
   AND nth_event = 2
   AND event_name IN ('UnitBorn')
   AND gameloop <= (4*60+13+15)*22.4
INTERSECT
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'Stimpack'
   AND event_name IN ('Upgrade')
   AND gameloop <= (4*60+50+15)*22.4
),
t2 AS (
  SELECT replay_id, string_agg(name || ' (' || LEFT(race, 1) || ')' || translate(to_char(result, '9'), '12', '*'),  ' vs ') AS vs_str, string_agg(DISTINCT LEFT(race,1),'') AS races
  FROM replays_players
  GROUP BY replay_id
)
SELECT replays.id, CONCAT(elapsed_gameloops/22.4, ' seconds')::interval AS length, map, to_timestamp(utc_ts) AS timestamp, vs_str, substring(path FROM 43) AS path
FROM replays, t, t2
WHERE replays.id = t2.replay_id AND replays.id = t.replay_id AND vs_str LIKE '%(P)%'
ORDER BY utc_ts DESC;
"""


"""
SELECT replay_id, CONCAT(gameloop/22.4, ' seconds')::interval AS length, entity_name, event_name, nth_event
FROM replays_tracker_events
WHERE
replay_id IN (5023, 4563, 6328, 6175, 6306) AND
(
  (entity_name = 'Marauder' AND nth_event = 2) OR
  (entity_name = 'Marine' AND nth_event = 16) OR
  (entity_name = 'Stimpack') OR
  (entity_name = 'ShieldWall') OR
  (entity_name = 'Barracks') OR
  (entity_name = 'SupplyDepot' AND nth_event = 2)
)
ORDER BY replay_id, gameloop;


 3319 | 00:17:20.714286 | Jagannatha LE  | 2021-05-26 06:36:41-07 | TIME (T) * vs 夜蝶蝶蝶蝶蝶蝶蝶 (P)  | /dreamhack_sc2_masters_2021_summer/3 - China/Group Stage/Group A/Winners Match/Time vs Firefly/20210526_-_GAME_2_-_Firefly_vs_TIME_-_P_vs_T_-_Jagannatha.SC2Replay
 2937 | 00:10:19.598214 | Romanticide LE | 2021-05-22 10:31:14-07 | BratOK (T)  vs ShoWTimE (P) *       | /dreamhack_sc2_masters_2021_summer/4 - Europe/Group Stage/Group B/10 - ShoWTimE vs Brat_OK/20210522 - GAME 1 - ShoWTimE vs Brat_OK - P vs T - Romanticide LE.SC2Replay
 5023 | 00:07:04.107143 | Oxide LE       | 2021-04-27 06:16:33-07 | DPGCure (T) * vs DPGZest (P)        | /wardi/2021_05/[TvP]  DPGCure vs DPGZest ьШеьВмьЭ┤ыУЬ - ыЮШыНФ.SC2Replay
 4723 | 00:12:05.580357 | Romanticide LE | 2021-04-07 04:29:23-07 | Ryung (T) * vs Ashbringer (P)       | /wardi/2021_04/[PvT]  Ashbringer vs [TeamGP]Ryung Romanticide LE.SC2Replay
 4563 | 00:05:11.741071 | Lightshade LE  | 2021-03-18 05:12:37-07 | LiquidClem (T) * vs DnS (P)         | /wardi/2021_04/[TvP]  [mlem]LiquidClem vs DnS Lightshade LE.SC2Replay
 6277 | 00:06:34.151786 | Deathaura LE   | 2021-02-07 08:05:39-08 | TYTY (T) * vs Zest (P)              | /wardi/2021_02/[TvP]  [ьЭ╕эИмыНФ]TYTY vs Zest Deathaura LE.SC2Replay
 7410 | 00:09:37.5      | Deathaura LE   | 2021-02-07 04:02:48-08 | Zest (P) * vs ByuN (T)              | /itax/Day_5_-_ITaX_Pro_Circuit_5/Day 5 - ITaX Pro Circuit 5/Series 4 - Zest vs ByuN/Zest vs ByuN_2_Deathaura.SC2Replay
 6306 | 00:10:59.464286 | Oxide LE       | 2021-01-31 04:52:42-08 | ByuN (T) * vs MaxPax (P)            | /wardi/2021_02/[TvP]  ByuN vs [Ex0n]MaxPax Oxide LE.SC2Replay
 6175 | 00:06:27.633929 | Oxide LE       | 2021-01-31 04:00:43-08 | ByuN (T) * vs Creator (P)           | /wardi/2021_02/[TvP]  ByuN vs [TeamNV]Creator Oxide LE.SC2Replay
 7435 | 00:16:29.375    | Deathaura LE   | 2021-01-29 07:04:20-08 | ByuN (T) * vs Patience (P)          | /itax/ITaX_Trovo_Series_013_ByuN_Solar_Patience_TIME/ITaX Trovo Series #013 ByuN Solar Patience TIME/Series 2 - ByuN vs Patience/ByuN vs Patience_2_Deathaura.SC2Replay
 6328 | 00:09:42.366071 | Romanticide LE | 2021-01-23 05:05:50-08 | DPGCure (T) * vs Zest (P)           | /wardi/2021_02/[TvP]  DPGCure vs [RYE]Zest Romanticide LE.SC2Replay



WITH t AS (
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'Raven'
   AND nth_event = 1
   AND event_name IN ('UnitBorn')
   AND gameloop <= (5*60)*22.4
INTERSECT
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'FactoryTechLab'
   AND nth_event = 2
   AND event_name IN ('UnitDone')
   AND gameloop <= (5*60)*22.4
EXCEPT
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name IN ('Hellion', 'WidowMine', 'SiegeTank', 'Cyclone')
   AND nth_event = 1
   AND event_name IN ('UnitBorn')
   AND gameloop <= (5*60)*22.4
),
t2 AS (
  SELECT replay_id, string_agg(name || ' (' || LEFT(race, 1) || ')' || translate(to_char(result, '9'), '12', '*'),  ' vs ') AS vs_str, string_agg(DISTINCT LEFT(race,1),'') AS races
  FROM replays_players
  GROUP BY replay_id
)
SELECT replays.id, CONCAT(elapsed_gameloops/22.4, ' seconds')::interval AS length, map, to_timestamp(utc_ts) AS timestamp, vs_str, substring(path FROM 43) AS path
FROM replays, t, t2
WHERE replays.id = t2.replay_id AND replays.id = t.replay_id AND vs_str LIKE '%(P)%'
ORDER BY utc_ts DESC;




WITH t AS (
SELECT DISTINCT replay_id
FROM replays_tracker_events
WHERE
   entity_name = 'BlinkTech'
   AND nth_event = 1
   AND event_name IN ('UnitBorn', 'UnitDone', 'Upgrade')
   AND gameloop < 330*22.4
INTERSECT
SELECT DISTINCT replay_id
FROM replays_tracker_events
WHERE
   entity_name = 'Gateway'
   AND nth_event = 4
   AND event_name IN ('UnitBorn', 'UnitDone', 'Upgrade')
   AND gameloop < 330*22.4
),
t2 AS (
  SELECT replay_id, string_agg(name || ' (' || LEFT(race, 1) || ')' || translate(to_char(result, '9'), '12', '*'),  ' vs ') AS vs_str, string_agg(DISTINCT LEFT(race,1),'') AS races
  FROM replays_players
  GROUP BY replay_id
)
SELECT replays.id, CONCAT(elapsed_gameloops/22.4, ' seconds')::interval AS length, map, to_timestamp(utc_ts) AS timestamp, vs_str, substring(path FROM 43) AS path
FROM replays, t, t2
WHERE replays.id = t2.replay_id AND replays.id = t.replay_id AND vs_str LIKE '%(T)%'
ORDER BY utc_ts DESC;




WITH t AS (
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'Hatchery'
   AND squared_dist_from_home > 4900
   AND event_name IN ('UnitInit', 'UnitBorn', 'UnitDone', 'UpgradeDone')
   AND gameloop < 180*22.4
),
t2 AS (
  SELECT replay_id, string_agg(name || ' (' || LEFT(race, 1) || ')' || translate(to_char(result, '9'), '12', '*'),  ' vs ') AS vs_str, string_agg(DISTINCT LEFT(race,1),'') AS races
  FROM replays_players
  GROUP BY replay_id
)
SELECT replays.id, CONCAT(elapsed_gameloops/22.4, ' seconds')::interval AS length, map, to_timestamp(utc_ts) AS timestamp, vs_str, substring(path FROM 43) AS path
FROM replays, t, t2
WHERE replays.id = t2.replay_id AND replays.id = t.replay_id AND vs_str LIKE '%(T)%'
ORDER BY utc_ts DESC;




WITH t AS (
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'Phoenix'
   AND nth_event = 4
   AND event_name IN ('UnitInit', 'UnitBorn', 'UnitDone', 'UpgradeDone')
   AND gameloop < 360*22.4
INTERSECT
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'Colossus'
   AND nth_event = 3
   AND event_name IN ('UnitInit', 'UnitBorn', 'UnitDone', 'UpgradeDone')
   AND gameloop < 600*22.4
),
t2 AS (
  SELECT replay_id, string_agg(name || ' (' || LEFT(race, 1) || ')' || translate(to_char(result, '9'), '12', '*'),  ' vs ') AS vs_str, string_agg(DISTINCT LEFT(race,1),'') AS races
  FROM replays_players
  GROUP BY replay_id
)
SELECT replays.id, CONCAT(elapsed_gameloops/22.4, ' seconds')::interval AS length, map, to_timestamp(utc_ts) AS timestamp, vs_str, substring(path FROM 43) AS path
FROM replays, t, t2
WHERE replays.id = t2.replay_id AND replays.id = t.replay_id AND vs_str LIKE '%(T)%'
ORDER BY utc_ts DESC;


WITH t AS (
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'Barracks'
   AND nth_event = 2
   AND event_name IN ('UnitInit', 'UnitBorn', 'UnitDone', 'UpgradeDone')
   AND gameloop < 180*22.4
INTERSECT
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'Reaper'
   AND nth_event = 4
   AND event_name IN ('UnitInit', 'UnitBorn', 'UnitDone', 'UpgradeDone')
   AND gameloop < 240*22.4
INTERSECT
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'CommandCenter'
   AND nth_event = 1
   AND event_name = 'UnitInit'
   AND gameloop < 240*22.4
),
t2 AS (
  SELECT replay_id, string_agg(name || ' (' || LEFT(race, 1) || ')' || translate(to_char(result, '9'), '12', '*'),  ' vs ') AS vs_str, string_agg(DISTINCT LEFT(race,1),'') AS races
  FROM replays_players
  GROUP BY replay_id
)
SELECT replays.id, CONCAT(elapsed_gameloops/22.4, ' seconds')::interval AS length, map, to_timestamp(utc_ts) AS timestamp, vs_str, substring(path FROM 43) AS path
FROM replays, t, t2
WHERE replays.id = t2.replay_id AND replays.id = t.replay_id AND vs_str LIKE '%(T)%'
ORDER BY utc_ts DESC;







WITH t AS (
SELECT DISTINCT replay_id
FROM replays_tracker_events
WHERE
   entity_name = 'DarkShrine'
   AND nth_event = 1
   AND event_name IN ('UnitInit', 'UnitBorn', 'UnitDone', 'UpgradeDone')
   AND gameloop < 270*22.4
INTERSECT
SELECT DISTINCT replay_id
FROM replays_tracker_events
WHERE
   entity_name = 'WidowMine'
   AND nth_event = 2
   AND event_name IN ('UnitInit', 'UnitBorn', 'UnitDone', 'UpgradeDone')
   AND gameloop < 270*22.4
INTERSECT
SELECT DISTINCT replay_id
FROM replays_tracker_events
WHERE
   entity_name = 'Medivac'
   AND nth_event = 1
   AND event_name = 'UnitInit'
   AND gameloop < 270*22.4
),
t2 AS (
  SELECT replay_id, string_agg(name || ' (' || LEFT(race, 1) || ')' || translate(to_char(result, '9'), '12', '*'),  ' vs ') AS vs_str, string_agg(DISTINCT LEFT(race,1),'') AS races
  FROM replays_players
  GROUP BY replay_id
)
SELECT replays.id, CONCAT(elapsed_gameloops/22.4, ' seconds')::interval AS length, map, to_timestamp(utc_ts) AS timestamp, vs_str, substring(path FROM 43) AS path
FROM replays, t, t2
WHERE replays.id = t2.replay_id AND replays.id = t.replay_id
ORDER BY utc_ts DESC;



WITH t AS (
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'Battlecruiser'
   AND nth_event = 1
   AND event_name IN ('UnitInit', 'UnitBorn', 'UnitDone', 'UpgradeDone')
   AND gameloop < 360*22.4
),
t2 AS (
  SELECT replay_id, string_agg(name || ' (' || LEFT(race, 1) || ')' || translate(to_char(result, '9'), '12', '*'),  ' vs ') AS vs_str, string_agg(DISTINCT LEFT(race,1),'') AS races
  FROM replays_players
  GROUP BY replay_id
)
SELECT replays.id, CONCAT(elapsed_gameloops/22.4, ' seconds')::interval AS length, map, to_timestamp(utc_ts) AS timestamp, vs_str, substring(path FROM 43) AS path
FROM replays, t, t2
WHERE replays.id = t2.replay_id AND replays.id = t.replay_id AND vs_str NOT LIKE '%(Z)%'
ORDER BY utc_ts DESC;


# TANK DROP
WITH t AS (
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'Medivac'
   AND nth_event = 1
   AND event_name IN ('UnitInit', 'UnitBorn', 'UnitDone', 'UpgradeDone')
   AND gameloop < (4*60)*22.4
INTERSECT
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'Marine'
   AND nth_event = 4
   AND event_name IN ('UnitInit', 'UnitBorn', 'UnitDone', 'UpgradeDone')
   AND gameloop < (4*60)*22.4
INTERSECT
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'SiegeTank'
   AND nth_event = 1
   AND event_name IN ('UnitInit', 'UnitBorn', 'UnitDone', 'UpgradeDone')
   AND gameloop < (4*60)*22.4
INTERSECT
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'Reaper'
   AND nth_event = 2
   AND event_name IN ('UnitInit', 'UnitBorn', 'UnitDone', 'UpgradeDone')
   AND gameloop < (4*60)*22.4
),
t2 AS (
  SELECT replay_id, string_agg(name || ' (' || LEFT(race, 1) || ')' || translate(to_char(result, '9'), '12', '*'),  ' vs ') AS vs_str, string_agg(DISTINCT LEFT(race,1),'') AS races
  FROM replays_players
  GROUP BY replay_id
)
SELECT replays.id, CONCAT(elapsed_gameloops/22.4, ' seconds')::interval AS length, map, to_timestamp(utc_ts) AS timestamp, vs_str, substring(path FROM 43) AS path
FROM replays, t, t2
WHERE replays.id = t2.replay_id AND replays.id = t.replay_id AND (
  vs_str ILIKE '%maru%' OR
  vs_str ILIKE '%clem%' OR
  vs_str ILIKE '%cure%'
)
ORDER BY utc_ts DESC;


WITH t AS (
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'Gateway'
   AND squared_dist_from_home > 4900
   AND nth_event = 1
   AND event_name IN ('UnitInit', 'UnitBorn', 'UnitDone', 'UpgradeDone')
   AND gameloop < (60)*22.4
),
t2 AS (
  SELECT replay_id, string_agg(name || ' (' || LEFT(race, 1) || ')' || translate(to_char(result, '9'), '12', '*'),  ' vs ') AS vs_str, string_agg(DISTINCT LEFT(race,1),'') AS races
  FROM replays_players
  GROUP BY replay_id
)
SELECT replays.id, CONCAT(elapsed_gameloops/22.4, ' seconds')::interval AS length, map, to_timestamp(utc_ts) AS timestamp, vs_str, substring(path FROM 43) AS path
FROM replays, t, t2
WHERE replays.id = t2.replay_id AND replays.id = t.replay_id
ORDER BY utc_ts DESC;



WITH t AS (
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'Ghost'
   AND event_name IN ('UnitInit', 'UnitBorn', 'UnitDone', 'UpgradeDone')
   AND gameloop < (8*60)*22.4
),
t2 AS (
  SELECT replay_id, string_agg(name || ' (' || LEFT(race, 1) || ')' || translate(to_char(result, '9'), '12', '*'),  ' vs ') AS vs_str, string_agg(DISTINCT LEFT(race,1),'') AS races
  FROM replays_players
  GROUP BY replay_id
)
SELECT replays.id, CONCAT(elapsed_gameloops/22.4, ' seconds')::interval AS length, map, to_timestamp(utc_ts) AS timestamp, vs_str, substring(path FROM 43) AS path
FROM replays, t, t2
WHERE replays.id = t2.replay_id AND replays.id = t.replay_id
ORDER BY utc_ts DESC;

TIME vs Serral: https://youtu.be/FeXHioEw3to
TIME vs Dark: https://youtu.be/veejL9mCnEs
Special vs Cham: https://youtu.be/rn6Ny-JZvtY



WITH t AS (
SELECT DISTINCT replay_id
FROM replays_tracker_events
WHERE
   entity_name = 'WidowMine'
   AND nth_event = 3
   AND event_name IN ('UnitInit', 'UnitBorn', 'UnitDone', 'UpgradeDone')
   AND gameloop < (5*60)*22.4
INTERSECT
SELECT DISTINCT replay_id
FROM replays_tracker_events
WHERE
   entity_name = 'Colossus'
   AND event_name IN ('UnitInit', 'UnitBorn', 'UnitDone', 'UpgradeDone')
   AND gameloop < (5*60)*22.4
),
t2 AS (
  SELECT replay_id, string_agg(name || ' (' || LEFT(race, 1) || ')' || translate(to_char(result, '9'), '12', '*'),  ' vs ') AS vs_str, string_agg(DISTINCT LEFT(race,1),'') AS races
  FROM replays_players
  GROUP BY replay_id
)
SELECT replays.id, CONCAT(elapsed_gameloops/22.4, ' seconds')::interval AS length, map, to_timestamp(utc_ts) AS timestamp, vs_str, substring(path FROM 43) AS path
FROM replays, t, t2
WHERE replays.id = t2.replay_id AND replays.id = t.replay_id
ORDER BY utc_ts DESC;


WITH t AS (
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'Zealot'
   AND nth_event = 4
   AND event_name IN ('UnitBorn', 'UnitDone', 'UpgradeDone')
   AND gameloop < 300*22.4
INTERSECT
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'WarpPrism'
   AND nth_event = 1
   AND event_name IN ('UnitBorn', 'UnitDone', 'UpgradeDone')
   AND gameloop < 300*22.4
),
t2 AS (
  SELECT replay_id, string_agg(name || ' (' || LEFT(race, 1) || ')' || translate(to_char(result, '9'), '12', '*'),  ' vs ') AS vs_str, string_agg(DISTINCT LEFT(race,1),'') AS races
  FROM replays_players
  GROUP BY replay_id
)
SELECT replays.id, CONCAT(elapsed_gameloops/22.4, ' seconds')::interval AS length, map, to_timestamp(utc_ts) AS timestamp, vs_str, substring(path FROM 43) AS path
FROM replays, t, t2
WHERE replays.id = t2.replay_id AND replays.id = t.replay_id
ORDER BY utc_ts DESC;


WITH t AS (
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'Marine'
   AND nth_event = 3
   AND event_name IN ('UnitBorn', 'UnitDone', 'UpgradeDone')
   AND gameloop < 210*22.4
INTERSECT
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'WidowMine'
   AND nth_event = 2
   AND event_name IN ('UnitBorn', 'UnitDone', 'UpgradeDone')
   AND gameloop < 300*22.4
INTERSECT
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'Medivac'
   AND nth_event = 1
   AND event_name IN ('UnitBorn', 'UnitDone', 'UpgradeDone')
   AND gameloop < 300*22.4
EXCEPT
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'Reaper'
   AND nth_event = 1
   AND event_name IN ('UnitBorn', 'UnitDone', 'UpgradeDone')
),
t2 AS (
  SELECT replay_id, string_agg(name || ' (' || LEFT(race, 1) || ')' || translate(to_char(result, '9'), '12', '*'),  ' vs ') AS vs_str, string_agg(DISTINCT LEFT(race,1),'') AS races
  FROM replays_players
  GROUP BY replay_id
)
SELECT replays.id, CONCAT(elapsed_gameloops/22.4, ' seconds')::interval AS length, map, to_timestamp(utc_ts) AS timestamp, vs_str, substring(path FROM 43) AS path
FROM replays, t, t2
WHERE replays.id = t2.replay_id AND replays.id = t.replay_id AND (
  vs_str ILIKE '%maru%' OR
  vs_str ILIKE '%clem%' OR
  vs_str ILIKE '%cure%'
)
ORDER BY utc_ts DESC;



WITH t AS (
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'Gateway'
   AND nth_event <= 2
   AND event_name IN ('UnitInit', 'UnitBorn', 'UnitDone', 'UpgradeDone')
   AND squared_dist_from_home >= 4900
   AND gameloop < 120*22.4
INTERSECT
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'Gateway'
   AND nth_event = 2
   AND event_name IN ('UnitInit', 'UnitBorn', 'UnitDone', 'UpgradeDone')
   AND gameloop < 120*22.4
EXCEPT
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'Nexus'
   AND nth_event <= 2
   AND event_name = 'UnitInit'
   AND gameloop < 120*22.4
),
t2 AS (
  SELECT replay_id, string_agg(name || ' (' || LEFT(race, 1) || ')' || translate(to_char(result, '9'), '12', '*'),  ' vs ') AS vs_str, string_agg(DISTINCT LEFT(race,1),'') AS races
  FROM replays_players
  GROUP BY replay_id
)
SELECT replays.id, CONCAT(elapsed_gameloops/22.4, ' seconds')::interval AS length, map, to_timestamp(utc_ts) AS timestamp, vs_str, substring(path FROM 43) AS path
FROM replays, t, t2
WHERE replays.id = t2.replay_id AND replays.id = t.replay_id AND (
  vs_str ILIKE '%maru%' OR
  vs_str ILIKE '%clem%' OR
  vs_str ILIKE '%cure%'
)
ORDER BY utc_ts DESC;


WITH t AS (
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'CommandCenter'
   AND nth_event = 2
   AND event_name = 'UnitInit'
   AND gameloop < 150*22.4
),
t2 AS (
  SELECT replay_id, string_agg(name || ' (' || LEFT(race, 1) || ')' || translate(to_char(result, '9'), '12', '*'),  ' vs ') AS vs_str, string_agg(DISTINCT LEFT(race,1),'') AS races
  FROM replays_players
  GROUP BY replay_id
)
SELECT replays.id, CONCAT(elapsed_gameloops/22.4, ' seconds')::interval AS length, map, to_timestamp(utc_ts) AS timestamp, vs_str, substring(path FROM 43) AS path
FROM replays, t, t2
WHERE replays.id = t2.replay_id AND replays.id = t.replay_id
ORDER BY utc_ts DESC;



WITH t AS (
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'Barracks'
   AND nth_event = 2
   AND event_name = 'UnitInit'
   AND squared_dist_from_home < 4900
   AND gameloop < 150*22.4
INTERSECT
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'Starport'
   AND nth_event = 1
   AND event_name = 'UnitInit'
   AND gameloop < 225*22.4
),
t2 AS (
  SELECT replay_id, string_agg(name || ' (' || LEFT(race, 1) || ')' || translate(to_char(result, '9'), '12', '*'),  ' vs ') AS vs_str, string_agg(DISTINCT LEFT(race,1),'') AS races
  FROM replays_players
  GROUP BY replay_id
)
SELECT replays.id, CONCAT(elapsed_gameloops/22.4, ' seconds')::interval AS length, map, to_timestamp(utc_ts) AS timestamp, vs_str, substring(path FROM 43) AS path
FROM replays, t, t2
WHERE replays.id = t2.replay_id AND replays.id = t.replay_id
ORDER BY utc_ts DESC;


WITH t AS (
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'Baneling'
   AND nth_event = 5
   AND event_name IN ('UnitInit', 'UnitBorn', 'UnitDone', 'UpgradeDone')
   AND gameloop < 240*22.4
),
t2 AS (
  SELECT replay_id, string_agg(name || ' (' || LEFT(race, 1) || ')' || translate(to_char(result, '9'), '12', '*'),  ' vs ') AS vs_str, string_agg(DISTINCT LEFT(race,1),'') AS races
  FROM replays_players
  GROUP BY replay_id
)
SELECT replays.id, CONCAT(elapsed_gameloops/22.4, ' seconds')::interval AS length, map, to_timestamp(utc_ts) AS timestamp, vs_str, substring(path FROM 43) AS path
FROM replays, t, t2
WHERE replays.id = t2.replay_id AND replays.id = t.replay_id
ORDER BY utc_ts DESC;

WITH t AS (
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'CommandCenter'
   AND nth_event = 2
   AND event_name = 'UnitInit'
   AND gameloop < (2*60+45)*22.4
INTERSECT
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'Starport'
   AND nth_event = 1
   AND event_name = 'UnitInit'
   AND gameloop < 195*22.4
INTERSECT
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'Banshee'
   AND nth_event = 1
   AND event_name = 'UnitBorn'
   AND gameloop < 300*22.4
INTERSECT
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'Barracks'
   AND nth_event = 2
   AND event_name IN ('UnitInit', 'UnitBorn', 'UnitDone', 'UpgradeDone')
   AND 240*22.4 < gameloop AND gameloop < 315*22.4
),
t2 AS (
  SELECT replay_id, string_agg(name || ' (' || LEFT(race, 1) || ')' || translate(to_char(result, '9'), '12', '*'),  ' vs ') AS vs_str, string_agg(DISTINCT LEFT(race,1),'') AS races
  FROM replays_players
  GROUP BY replay_id
)
SELECT replays.id, CONCAT(elapsed_gameloops/22.4, ' seconds')::interval AS length, map, to_timestamp(utc_ts) AS timestamp, vs_str, substring(path FROM 43) AS path
FROM replays, t, t2
WHERE replays.id = t2.replay_id AND replays.id = t.replay_id
ORDER BY utc_ts DESC;




WITH t AS (
SELECT DISTINCT replay_id
FROM replays_tracker_events
WHERE
   entity_name = 'CommandCenter'
   AND nth_event = 2
   AND event_name = 'UnitInit'
   AND gameloop < (2*60+45)*22.4
INTERSECT
SELECT DISTINCT replay_id
FROM replays_tracker_events
WHERE
   entity_name = 'Starport'
   AND nth_event = 1
   AND event_name = 'UnitInit'
   AND gameloop < 195*22.4
INTERSECT
SELECT DISTINCT replay_id
FROM replays_tracker_events
WHERE
   entity_name = 'Banshee'
   AND nth_event = 1
   AND event_name = 'UnitBorn'
   AND gameloop < 300*22.4
INTERSECT
SELECT DISTINCT replay_id
FROM replays_tracker_events
WHERE
   entity_name = 'Barracks'
   AND nth_event = 2
   AND event_name = 'UnitInit'
   AND 240*22.4 < gameloop AND gameloop < 315*22.4
INTERSECT
SELECT DISTINCT replay_id
FROM replays_tracker_events
WHERE
   entity_name = 'Roach'
   AND nth_event = 1
   AND event_name IN ('UnitInit', 'UnitBorn', 'UnitDone', 'UpgradeDone')
   AND gameloop < 360*22.4
),
t2 AS (
  SELECT replay_id, string_agg(name || ' (' || LEFT(race, 1) || ')' || translate(to_char(result, '9'), '12', '*'),  ' vs ') AS vs_str, string_agg(DISTINCT LEFT(race,1),'') AS races
  FROM replays_players
  GROUP BY replay_id
)
SELECT replays.id, CONCAT(elapsed_gameloops/22.4, ' seconds')::interval AS length, map, to_timestamp(utc_ts) AS timestamp, vs_str, substring(path FROM 43) AS path
FROM replays, t, t2
WHERE replays.id = t2.replay_id AND replays.id = t.replay_id
ORDER BY utc_ts DESC;


WITH t AS (
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'Stargate'
   AND nth_event = 1
   AND event_name = 'UnitInit'
   AND squared_dist_from_home >= 4900
   AND gameloop < (4*60)*22.4
INTERSECT
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'VoidRay'
   AND nth_event = 1
   AND event_name = 'UnitBorn'
   AND gameloop < (4*60)*22.4
),
t2 AS (
  SELECT replay_id, string_agg(name || ' (' || LEFT(race, 1) || ')' || translate(to_char(result, '9'), '12', '*'),  ' vs ') AS vs_str, string_agg(DISTINCT LEFT(race,1),'') AS races
  FROM replays_players
  GROUP BY replay_id
)
SELECT replays.id, CONCAT(elapsed_gameloops/22.4, ' seconds')::interval AS length, map, to_timestamp(utc_ts) AS timestamp, vs_str, substring(path FROM 43) AS path
FROM replays, t, t2
WHERE replays.id = t2.replay_id AND replays.id = t.replay_id AND vs_str LIKE '%(T)%'
ORDER BY utc_ts DESC;


WITH t AS (
SELECT DISTINCT replay_id, true_player_id
FROM replays_tracker_events
WHERE
   entity_name = 'LurkerDenMP'
),
t2 AS (
  SELECT replay_id, string_agg(name || ' (' || LEFT(race, 1) || ')' || translate(to_char(result, '9'), '12', '*'),  ' vs ') AS vs_str, string_agg(DISTINCT LEFT(race,1),'') AS races
  FROM replays_players
  GROUP BY replay_id
)
SELECT replays.id, CONCAT(elapsed_gameloops/22.4, ' seconds')::interval AS length, map, to_timestamp(utc_ts) AS timestamp, vs_str, substring(path FROM 43) AS path
FROM replays, t, t2
WHERE replays.id = t2.replay_id AND replays.id = t.replay_id AND vs_str LIKE '%(T)%'
ORDER BY utc_ts DESC;


/asus_rog_online_2021/Group Stage/Group B/1 - Solar vs Clem/21-09-17 19_46_03 - Romanticide LE - LiquidClem vs Solar.SC2Replay
