CREATE TABLE IF NOT EXISTS game_types
(game_type_id INTEGER PRIMARY KEY,
players INTEGER"",
game_type TEXT, "")

INSERT into game_types (game_type_id, players, game_type)
VALUES (1, 2, 'Singles'),
(2, 4, 'Pairs'),
(3, 6, 'Triples'),
(4, 8, 'Fours') 
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS competitions
(competition_id INTEGER PRIMARY KEY,
competition TEXT, "");

INSERT into competitions (competition_id, competition)
VALUES (1, 'Pennant / Club / Gala'),
(2, 'BPL')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS genders
(gender_id INTEGER PRIMARY KEY,
gender text, "")
INSERT into genders (gender_id, gender)
VALUES (1, 'Mens'),
(2, 'Ladies'),
(3, 'Mixed'),
(4, 'Open') 
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS rounds
(round_id INTEGER PRIMARY KEY,
round text, "")
INSERT into rounds (round_id, round)
VALUES (1, 64),
(2, 32),
(3, 16),
(4, 'Quarter'),
(5, 'Semi'),
(6, 'Final') 
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS displays
(display_id INTEGER PRIMARY KEY,
display text, "")
INSERT into displays (display_id, display)
VALUES (1, 'Default'),
(2, 'Logo'),
(3, 'First Initial'),
(4, 'Fist and Last Initial') 
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS grades
(grade_id INTEGER PRIMARY KEY,
grade text, "")
INSERT into grades (grade_id, grade)
VALUES (1, 'Premiere'),
(2, '1'),
(3, '2'),
(4, '3'),
(5, '4'),
(6, '5'),
(7, '6') 
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS sponsors
(sponsor_id INTEGER PRIMARY KEY,
sponsor TEXT NOT NULL DEFAULT "",
sponsor_logo TEXT NOT NULL)
INSERT into sponsors (sponsor_id, sponsor, sponsor_logo)
VALUES (1, 'Bell Property', 'belle_whitebg.png'),
(2, 'XXXX', 'xxxx.png') 
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS rinks
(rink_id INTEGER PRIMARY KEY,
rink text,
ip text, "")
INSERT into rinks (rink_id, rink, ip)
VALUES (1, 'Rink 1', '192.168.15.201:8081'),
(2, 'Rink 2', '192.168.15.202:8081'),
(3, 'Rink 3', '192.168.15.203:8081'),
(4, 'Rink 4', '192.168.15.204:8081'),
(5, 'Rink 5', '192.168.15.205:8081'),
(6, 'Rink 6', '192.168.15.206:8081'),
(7, 'Rink 7', '192.168.15.207:8081'),
(8, 'Rink 8', '192.168.15.208:8081')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS layouts
(layout_id INTEGER PRIMARY KEY,
layout text)
INSERT into layouts (layout_id, layout)
VALUES (1, 'BPL'),
(2, 'General Scoreboard (8) Rinks'),
(3, 'Premier Pennant (4) Rinks & Masterboard'),
(4, '(2) Pennant Games with (3) Rinks & Masterboard')
ON CONFLICT DO NOTHING;


CREATE TABLE IF NOT EXISTS bigboard_layout_link
(bigboard_layout_link_id INTEGER PRIMARY KEY,
layout INTEGER DEFAULT NULL,
rink INTEGER DEFAULT NULL,
FOREIGN KEY (layout)
REFERENCES layouts (layout_id),
FOREIGN KEY (rink)
REFERENCES rinks (rink_id));
INSERT INTO bigboard_layout_link (bigboard_layout_link_id, layout, rink)
VALUES (1,1,1),
(2,1,2),
(3,1,3),
(4,1,4),
(5,1,5),
(6,1,6),
(7,1,7),
(8,1,8),
(9,2,1),
(10,2,2),
(11,2,3),
(12,2,4),
(13,2,5),
(14,2,6),
(15,2,7),
(16,2,8),
(17,3,1),
(18,3,2),
(19,3,3),
(20,3,4),
(21,4,1),
(22,4,2),
(23,4,3),
(24,4,4),
(25,4,5),
(26,4,6);
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS bigboards
(bigboard_id INTEGER PRIMARY KEY,
bigboard text,
ip text "",
current_layout INTEGER DEFAULT 1,
FOREIGN KEY (current_layout)
REFERENCES layouts (layout_id));
INSERT into bigboards (bigboard_id, bigboard, ip, current_layout)
VALUES (1, 'Bigboard 1', '192.168.15.215:8081', 1)
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS games
(game_id INTEGER PRIMARY KEY,
name text DEFAULT NULL,
game_type INTEGER DEFAULT NULL,
gender INTEGER DEFAULT NULL,
competition INTEGER DEFAULT NULL,
round INTEGER DEFAULT NULL,
grade INTEGER DEFAULT NULL,
rink INTEGER DEFAULT NULL,
sponsor INTEGER DEFAULT NULL,
start_time text,
finish_time text DEFAULT NULL,
ends INTEGER DEFAULT 0,
winner INTEGER DEFAULT NULL,
FOREIGN KEY (game_type)
REFERENCES game_type (game_type_id)
ON UPDATE CASCADE
ON DELETE SET DEFAULT,
FOREIGN KEY (gender)
REFERENCES genders (gender_id)
ON UPDATE CASCADE
ON DELETE SET DEFAULT,
FOREIGN KEY (competition)
REFERENCES competitions (competition_id)
ON UPDATE CASCADE
ON DELETE SET DEFAULT,
FOREIGN KEY (round)
REFERENCES rounds (round_id)
ON UPDATE CASCADE
ON DELETE SET DEFAULT,
FOREIGN KEY (grade)
REFERENCES grades (grade_id)
ON UPDATE CASCADE
ON DELETE SET DEFAULT,
FOREIGN KEY (rink)
REFERENCES rinks (rink_id)
ON UPDATE CASCADE
ON DELETE SET DEFAULT,
FOREIGN KEY (sponsor)
REFERENCES sponsors (sponsor_id)
ON UPDATE CASCADE
ON DELETE SET DEFAULT,
FOREIGN KEY (winner)
REFERENCES competitors (team)
ON UPDATE CASCADE
ON DELETE SET DEFAULT)
