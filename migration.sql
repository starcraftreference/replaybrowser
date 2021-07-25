DROP TABLE IF EXISTS replays_tracker_events;
DROP TABLE IF EXISTS replays_players;
DROP TABLE IF EXISTS replays;
CREATE TABLE replays (
  id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  elapsed_gameloops int NOT NULL,
  base_build int NOT NULL,
  map text NOT NULL,
  utc_ts bigint NOT NULL,
  local_ts bigint NOT NULL,
  path text NOT NULL UNIQUE,
  sha256 text NOT NULL UNIQUE
);

CREATE TABLE replays_players (
  id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  replay_id bigint NOT NULL REFERENCES replays,
  clan text NOT NULL,
  name text NOT NULL,
  race text NOT NULL,
  result int NOT NULL,
  player_list_id int NOT NULL,
  team_id int NOT NULL,
  working_set_slot_id int NOT NULL,
  game_events_id int NOT NULL,
  tracker_events_id int NOT NULL,
  slot_id int NOT NULL
);

CREATE TABLE replays_tracker_events (
  id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  replay_id bigint NOT NULL REFERENCES replays,
  event_no bigint NOT NULL,
  event_name text NOT NULL,
  event_id int NOT NULL,
  gameloop int NOT NULL,
  bits int NOT NULL,
  unit_tag_index int,
  unit_tag_recycle int,
  unit_type_name text,
  control_player_id int,
  upkeep_player_id int,
  x int,
  y int,
  creator_unit_tag_index int,
  creator_unit_tag_recycle int,
  creator_ability_name text,
  killer_player_id int,
  killer_unit_tag_index int,
  killer_unit_tag_recycle int,
  count int,
  player_id int,
  upgrade_type_name text,
  stats jsonb,
  true_player_id int,
  entity_name text,
  nth_event int NOT NULL,
  squared_dist_from_home int,
  UNIQUE(replay_id, event_no)
);
