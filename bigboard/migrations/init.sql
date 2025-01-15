CREATE TABLE IF NOT EXISTS scoreboards_layout
(scoreboards_layout_id INTEGER PRIMARY KEY,
layout text"",
ip text DEFAULT NULL);
INSERT into scoreboards_layout (scoreboards_layout_id, layout, ip)
VALUES (1, 'BPL', '192.168.15.201:8081'),
(2, 'BPL', '192.168.15.202:8081'),
(3, 'BPL', '192.168.15.203:8081'),
(4, 'BPL', '192.168.15.204:8081'),
(5, 'BPL', '192.168.15.205:8081'),
(6, 'BPL', '192.168.15.206:8081'),
(7, 'BPL', '192.168.15.207:8081'),
(8, 'BPL', '192.168.15.208:8081')
ON CONFLICT DO NOTHING;
