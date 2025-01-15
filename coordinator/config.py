COORDINATOR_IP = "192.168.32.10:8000"

DEFAULT_GAME = {
    "game_id": -1,
    "coordinator_ip":COORDINATOR_IP,
    "start_time":"",
    "finish_time": None,
    "winner":"",
    "name": "standard",
    "ends":0,
    "competition": {
        "competition_id":1,
        "competition":"Pennant / Club / Gala",
    },
    "rink": {},
    "competitors": {
        "1": {
            "player_id": "",
            "first_name": "",
            "last_name": "",
            "score": 0,
            "sets": 0,
            "logo": "moama_steamers.png",
            "default_logo": "moama_steamers.png",
            "display": {"display": "Logo", "display_id": 2},
        },
        "2": {
            "player_id": "",
            "first_name": "",
            "last_name": "",
            "score": 0,
            "sets": 0,
            "logo": "away.jpeg",
            "default_logo": "away.jpeg",
            "display": {"display": "Logo", "display_id": 2},
        },
    },
    "clubs": {
        "1": {"club_id": 1, "club_name": "Moama", "logo": "moama_steamers.png"},
        "2": {"club_id": 2, "club_name": "Away", "logo": "away.jpeg"},
    },
    "displays": {
        "1": {"display": "Default", "display_id": 1},
        "2": {"display": "Default", "display_id": 1},
    },
}
