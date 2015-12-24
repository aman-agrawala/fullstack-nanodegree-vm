#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("delete from matches;")
    connection.commit()
    connection.close()


def deletePlayers():
    """Remove all the player records from the database."""
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("delete from players;")
    connection.commit()
    connection.close()


def countPlayers():
    """Returns the number of players currently registered."""
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("select count(*) as num from players;")
    count = cursor.fetchall()
    connection.close()
    return count[0][0]


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    connection = connect()
    cursor = connection.cursor()
    content = bleach.clean(name)
    cursor.execute("insert into players (Name) values (%s)", (content,))
    connection.commit()
    connection.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("select * from standings;")
    standings = cursor.fetchall()
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    connection = connect()
    cursor = connection.cursor()
    Clean_Winner = bleach.clean(winner)
    Clean_Loser = bleach.clean(loser)
    cursor.execute("insert into matches (Winner, Loser) values (%s,%s)",
                   (Clean_Winner, Clean_Loser,))
    connection.commit()
    connection.close()


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
    pairsList = []
    standings = playerStandings()
    rowNums = len(standings)

    # Commented this block out because list comprehension is faster
    # winList = []
    # print winList

    # for row in standings:
    #     winList.append(row[2])
    #     print winList
    # print winList[1]

    # Better way to do above block of code
    winList = [row[2] for row in standings]
    rows = range(1, len(winList)+1)
    rowLoc = 1
    while rowLoc <= len(rows):
        winVal = winList[rowLoc-1]
        numSimilar = winList.count(winVal)
        numPairs = numSimilar/2
        for y in winList[rowLoc-1:numPairs+rowLoc-1]:
            pair = (standings[rowLoc-1][0], standings[rowLoc-1][1],
                    standings[rowLoc][0], standings[rowLoc][1])
            pairsList.append(pair)
            rowLoc = rowLoc + 2
    return pairsList
