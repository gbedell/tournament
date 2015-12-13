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
