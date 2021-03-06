-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

\c tournament;

create table players (ID serial primary key, Name text);

--create table score (ID serial references players(id), Player text, Opponent text, Win/Loss text)

--create table matches (Round int, Match_Number int, Player1_ID serial references players(ID), Player1_Name text references players(Name), Player2_ID serial references players(ID), Players2_Name text references players(Name), Winner text, primary key (Round, Match_Number));

-- create table matches (Round int, Match_Number int, Player1_ID serial references players(ID), Player2_ID serial references players(ID), Winner serial references players(ID), primary key (Round, Match_Number));

create table matches (Match_Number serial primary key, Winner int references players(ID), Loser int references players(ID));

create view match_number as (select players.ID, players.Name, count(matches.Winner) as matchs from players left join matches on players.ID = matches.Winner or players.ID = matches.Loser group by matches.Winner, matches.Loser, players.ID order by matchs);

create view score as (select players.ID, players.Name, count(matches.Winner) as wins, count(matches.Winner) as match_num from players left join matches on players.ID = matches.Winner group by matches.Winner, players.ID order by wins);

create view standings as (select score.ID, score.Name, score.wins, match_number.matchs as matches from score join match_number on score.ID = match_number.ID order by wins DESC);