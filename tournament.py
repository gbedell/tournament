#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    query = ('DELETE FROM match;')
    c.execute(query)
    conn.commit()
    conn.close()

def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    query = ('DELETE FROM player;')
    c.execute(query)
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor()
    query = ('SELECT count(*) FROM player;')
    c.execute(query)
    results = c.fetchone()
    count_of_players = results[0]
    conn.commit()
    conn.close()
    return count_of_players

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    c = conn.cursor()
    query = ('INSERT INTO player (name) VALUES (%s);')
    c.execute(query, (name,))
    conn.commit()
    conn.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    c = conn.cursor()
    query = ("""SELECT
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
            ;""")
    c.execute(query)
    results = c.fetchall()
    return results
    conn.commit()
    conn.close()


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    c = conn.cursor()
    query = ('INSERT INTO match (winner_id, loser_id) VALUES (%s, %s);')
    c.execute(query, (winner, loser))
    conn.commit()
    conn.close()
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    standings = playerStandings()

    pairings = []

    # These indexes will be used to select the appropriate pairs for the game
    beg_index = 0
    end_index = 1

    while end_index < len(standings):

        first_player = standings[beg_index]
        second_player = standings[end_index]

        pairing = (first_player[0], first_player[1], second_player[0], second_player[1])

        pairings.append(pairing)

        # Extends the index to find the next appropriate pairing
        beg_index += 2
        end_index += 2

    return pairings




