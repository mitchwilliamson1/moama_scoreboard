CREATE TABLE IF NOT EXISTS displays
(display_id INTEGER PRIMARY KEY,
display text, "")
INSERT into displays (display_id, display)
VALUES (1, 'Default'),
(2, 'Logo'),
(3, 'First Initial'),
(4, 'Fist and Last Initial') 
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS competitions
(competition_id INTEGER PRIMARY KEY,
competition TEXT, "");
INSERT into competitions (competition_id, competition)
VALUES (1, 'Pennant / Club / Gala'),
(2, 'BPL')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS games
(game_id INTEGER PRIMARY KEY,
name text DEFAULT NULL,
competition INTEGER DEFAULT NULL,
sponsor TEXT NOT NULL DEFAULT "",
start_time text DEFAULT NULL, 
finish_time text DEFAULT NULL, 
ends int DEFAULT 0,
winner text DEFAULT "",
coordinator_ip text DEFAULT "127.0.0.1:8000",
FOREIGN KEY (competition)
REFERENCES competitions (competition_id)
ON UPDATE CASCADE
ON DELETE SET DEFAULT)

CREATE TABLE IF NOT EXISTS competitors
(competitor_id INTEGER NOT NULL PRIMARY KEY,
player_id INTEGER DEFAULT "No Player",
first_name text DEFAULT "",
last_name text DEFAULT "",
score text DEFAULT 0,
sets text DEFAULT 0,
logo text DEFAULT "",
display INTEGER NOT NULL DEFAULT 1,
game INTEGER NOT NULL DEFAULT "No Game",
FOREIGN KEY (display)
REFERENCES displays (display_id)
ON UPDATE CASCADE
ON DELETE SET DEFAULT,
FOREIGN KEY (game)
REFERENCES games (game_id)
ON UPDATE CASCADE
ON DELETE SET DEFAULT)