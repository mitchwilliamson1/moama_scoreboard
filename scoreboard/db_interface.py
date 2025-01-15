import datetime
import sqlite3
import json
import pickle
import pytz
import requests
import os
import asyncio
import sys

# import importlib
# config = importlib.import_module(sys.argv[1])

import config



local_tz = pytz.timezone("Australia/Sydney")

class Game:
    def __init__(self):
        self.db_path = "scoreboard.db"

    def encode_if_required(self, str_val):
        try:
            return str_val.encode()
        except Exception:
            return str_val

    def coordinator_running(self):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        cursor = con.cursor()
        parsed_rows = []
        
        coordinator_ip = cursor.execute('''SELECT coordinator_ip FROM games''').fetchone()

        from ipaddress import ip_address
        ip, separator, port = coordinator_ip[0].rpartition(':')
        assert separator # separator (`:`) must be present
        port = int(port) # convert to integer
        ip = ip_address(ip)
        return self.check(ip, port)

    def check(self, host,port,timeout=5):
        import socket
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #presumably 
        sock.settimeout(timeout)
        try:
           sock.connect((str(host),port))
        except:
            return False
        else:
            sock.close()
            return True


    def get_game(self):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        GAME = config.DEFAULT_GAME

        games = cursor.execute('''SELECT game_id,
                                name,
                                ends,
                                winner,
                                coordinator_ip,
                                c.competition as competition
                                FROM games g
                                INNER JOIN competitions c
                                ON g.competition = c.competition_id
                                WHERE finish_time is NULL''').fetchall()

        column_names = list(map(lambda x: x[0], cursor.description))

        if not games:
            self.create_game(GAME)

        for game in games:
            if game['ends'] < 0:
                self.create_game(GAME)

            sql = """SELECT competitor_id, player_id, first_name, last_name, score, sets, logo, d.display FROM competitors as c
                    INNER JOIN displays AS d
                    ON c.display = d.display_id
                    where game = ?"""
            params = (game['game_id'],)
            players = cursor.execute(sql, params).fetchall()
            competitors = []
            tie_break = []

            player_column_names = list(map(lambda x: x[0], cursor.description))

            for column in column_names:
                GAME[column] = game[column]
            GAME['coordinator_running'] = self.coordinator_running()


            for player in players:
                # BPL RULES
                if game['competition'] == 'BPL':
                    if float(player['sets']) > 2:
                        reset = self.reset_sets()
                    if player['sets'] == '1':
                        tie_break.append(1)

                for column in player_column_names:
                    GAME['competitors'][str(player['competitor_id'])][column] = player[column]

            # check if both players have sets == 1
            if len(tie_break) == 2:
                tie = True
            else:
                tie = False

            GAME["tie_break"]= tie

            return json.dumps(GAME)

    def delete_all_games(self):
        try:
            con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
            con.row_factory = sqlite3.Row
            cursor = con.cursor()

            sql = "DELETE FROM games"
            cursor.execute(sql)
            sql = "DELETE FROM competitors"
            cursor.execute(sql)
            con.commit()
        except:
            return "no data"


    def create_game(self, js):
        self.delete_all_games()

        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        utc = datetime.datetime.utcnow().replace(tzinfo=pytz.timezone('UTC'))

        js['finish_time'] = None

        print("JS: ", js)

        sql = "INSERT INTO games (game_id, competition, start_time, finish_time, coordinator_ip) VALUES(?,?,?,?,?);"
        params = (js['game_id'], js["competition"]["competition_id"], utc, js['finish_time'], js['coordinator_ip'])
        print(sql)
        print(params)
        game_id = cursor.execute(sql, params)

        for player in js['competitors']:
            competitor = js['competitors'][player]

            sql = "INSERT INTO competitors (player_id, first_name, last_name, logo, display, game) VALUES(?,?,?,?,?,?);"
            params = (js['competitors'][player]['player_id'],
                js['competitors'][player]['first_name'],
                js['competitors'][player]['last_name'],
                js['clubs'][player]['logo'],
                js['competitors'][player]['display']['display_id'],
                js['game_id'])
            cursor.execute(sql, params)
        con.commit()


    def update_game(self, js, coordinator_ip):
        self.delete_all_games()

        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        utc = datetime.datetime.utcnow().replace(tzinfo=pytz.timezone('UTC'))

        coordinator_ip += ':8000'

        if js['finish_time']:
            cursor.execute("DELETE from games")
            cursor.execute("DELETE from competitors")
            con.commit()

        else:
            sql = "INSERT INTO games (game_id, name, competition, start_time, finish_time, coordinator_ip, ends) VALUES(?,?,?,?,?,?,?);"
            params = (js['game_id'], js['name'], js["competition"]["competition_id"], utc, js['finish_time'], coordinator_ip, js['ends'])
            game_id = cursor.execute(sql, params)

            for player in js['competitors']:
                sql = "INSERT INTO competitors (player_id, first_name, last_name, score, sets, logo, display, game) VALUES(?,?,?,?,?,?,?,?);"
                params = (player['player_id'], player['first_name'], player['last_name'], player['score'], player['sets'], player['logo'], player['display']['display_id'], js['game_id'])
                cursor.execute(sql, params)
            con.commit()


    def add_ends(self, js):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        cmd = "UPDATE games SET ends = ? WHERE game_id = ?"
        params = [js["ends"], js["game_id"]]

        res = cursor.execute(cmd, params)

        con.commit()
        # if res.fetchone() is None:
        #     try:
        #         r_code = self.write_coordinator_ends(js)
        #     except:
        #         pass
        return {
                "status": "ok",
        }

    def reset_score(self):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        cmd = "UPDATE competitors SET score = 0"

        res = cursor.execute(cmd)
        con.commit()

        if res.fetchone() is None:
            return True
        else:
            return False


    def add_score(self, js):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        cmd = "UPDATE competitors SET score = ? WHERE player_id=?"
        params = [js["score"], js["player"]["player_id"]]

        res = cursor.execute(cmd, params)
        con.commit()

        return {
                "status": "ok",
        }

    def reset_sets(self):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        cmd = "UPDATE competitors SET sets = 0"

        res = cursor.execute(cmd)
        con.commit()

        if res.fetchone() is None:
            self.reset_score()
            return True
        else:
            return False


    def add_sets(self, js):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        print(js)

        cmd = "UPDATE competitors SET sets = ? WHERE player_id=?"
        params = [js["sets"], js["player"]["player_id"]]

        res = cursor.execute(cmd, params)
        con.commit()

        if res.fetchone() is None:
            reset = self.reset_score()
            if reset:
                return True
        return False 


    def coordinator_ip(self):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        cursor = con.cursor()
        return cursor.execute('''SELECT coordinator_ip FROM games''').fetchone()


    def write_coordinator_score(self, js):
        response = requests.post('http://'+self.coordinator_ip()+'/games/add_score', json = js)
        return response.status_code


    def write_coordinator_ends(self, js):
        response = requests.post('http://'+self.coordinator_ip()+'/games/add_ends', json = js)
        return response.status_code
