-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Will delete the previous version of the database if this file is run again
DROP DATABASE IF EXISTS tournament;

-- Create the tournament database
CREATE DATABASE tournament;

-- Connect to the tournament database
\c tournament;

-- Create player table
CREATE TABLE player (
	user_id serial PRIMARY KEY,
	name text
);

-- Create match table
CREATE TABLE match (
	match_id serial PRIMARY KEY,
	winner_id integer REFERENCES player (user_id),
	loser_id integer REFERENCES player (user_id)
);

CREATE VIEW standings AS 
SELECT
wins_table.id as id,
wins_table.name as name,
wins_table.wins as wins,
wins_table.wins + losses_table.losses as matches

FROM

(SELECT
player.user_id as id,
player.name as name,
count(match.winner_id) as wins

FROM
player
left join match
on player.user_id = match.winner_id

GROUP BY        
player.user_id)
AS wins_table

LEFT JOIN    

(SELECT
player.user_id as id,
player.name as name,
count(match.loser_id) as losses                

FROM
player
left join match
on player.user_id = match.loser_id

GROUP BY
player.user_id)
AS losses_table

ON wins_table.id = losses_table.id

ORDER BY
wins_table.wins desc