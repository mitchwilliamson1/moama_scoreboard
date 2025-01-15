import datetime
import sqlite3
import json
import pickle
import pytz
import requests
import threading
import sys

import config


local_tz = pytz.timezone("Australia/Sydney")

class Games:
    def __init__(self):
        self.db_path = "co_ordinator.db"
        # self.init_database_tables()

    def get_game_types(self):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        parsed_rows = []
        game_types = cursor.execute("SELECT * FROM game_types").fetchall()

        for game_type in game_types:
            parsed_rows.append({
                "game_type_id": game_type["game_type_id"],
                "game_type": game_type["game_type"],
                "players": game_type["players"],
            })

        return parsed_rows

    def get_genders(self):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        parsed_rows = []
        genders = cursor.execute("SELECT * FROM genders").fetchall()

        for gender in genders:
            parsed_rows.append({
                "gender": gender["gender"],
                "gender_id": gender["gender_id"],
            })

        return parsed_rows

    def get_competitions(self):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        parsed_rows = []
        competitions = cursor.execute("SELECT * FROM competitions").fetchall()

        for competition in competitions:
            parsed_rows.append({
                "competition": competition["competition"],
                "competition_id": competition["competition_id"],
            })

        return parsed_rows

    def get_rounds(self):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        parsed_rows = []
        rounds = cursor.execute("SELECT * FROM rounds").fetchall()

        for _round in rounds:
            parsed_rows.append({
                "round": _round["round"],
                "round_id": _round["round_id"],
            })

        return parsed_rows


    def get_displays(self):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        parsed_rows = []
        displays = cursor.execute("SELECT * FROM displays").fetchall()

        for display in displays:
            parsed_rows.append({
                "display": display["display"],
                "display_id": display["display_id"],
            })

        return parsed_rows

    def get_grades(self):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        parsed_rows = []
        grades = cursor.execute("SELECT * FROM grades").fetchall()

        for grade in grades:
            parsed_rows.append({
                "grade": grade["grade"],
                "grade_id": grade["grade_id"],
            })

        return parsed_rows

    def get_rinks(self):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        parsed_rows = []
        rinks = cursor.execute("SELECT * FROM rinks").fetchall()

        for rink in rinks:
            parsed_rows.append({
                "rink": rink["rink"],
                "ip": rink["ip"],
                "rink_id": rink["rink_id"],
            })

        return parsed_rows


    def get_layouts(self):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        parsed_rows = []
        layouts = cursor.execute("SELECT * FROM layouts").fetchall()

        for layout in layouts:
            parsed_rows.append({
                "layout_id": layout["layout_id"],
                "layout": layout["layout"],
            })

        return parsed_rows

    def get_bigboards(self):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        bigboards = cursor.execute("""SELECT * FROM bigboards b
            INNER JOIN layouts ON b.current_layout  = layouts.layout_id """).fetchall()
        boards = []

        for bigboard in bigboards:
            boards.append({
                "bigboard": bigboard["bigboard"],
                "ip": bigboard["ip"],
                "bigboard_id": bigboard["bigboard_id"],
                "current_layout": {
                    "layout_id": bigboard["current_layout"],
                    "layout": bigboard["layout"]
                }
            })
        #     sql = f'''SELECT r.rink, r.ip, r.rink_id from master_link ml
        #             inner join bigboards b 
        #             on ml.bigboard = b.masterboard_id
        #             inner join rinks r 
        #             on ml.rink = r.rink_id
        #             where b.masterboard_id = ?'''
        #     params = [bigboard['masterboard_id']]
        #     rink_ips = cursor.execute(sql, params).fetchall()
        #     rinks = []
        #     for rink_ip in rink_ips:
        #         rinks.append({
        #             "rink": rink_ip[0],
        #             "ip": rink_ip[1],
        #             "rink_id": rink_ip[2],

        #          })

        #     parsed_rows.append({
        #         "bigboard": bigboard["bigboard"],
        #         "ip": bigboard["ip"],
        #         "masterboard_id": bigboard["bigboard_id"],
        #     })
        return boards


    def get_sponsors(self, dump):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        parsed_rows = []
        sponsors = cursor.execute("SELECT * FROM sponsors").fetchall()

        for sponsor in sponsors:
            parsed_rows.append({
                "sponsor_id": sponsor["sponsor_id"],
                "sponsor": sponsor["sponsor"],
                "sponsor_logo": sponsor["sponsor_logo"],
            })
        if dump:
            return json.dumps(parsed_rows)
        else:
            return parsed_rows

    def get_default_game(self):
        return [config.DEFAULT_GAME]



    def get_games(self, get_current):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        parsed_rows = []
        if get_current:
            sql = '''SELECT *, r.rink as rink_name, c.competition as comp_name FROM games g
                    inner join rinks r
                    on g.rink = r.rink_id
                    inner join competitions c
                    on g.competition = c.competition_id
                    WHERE finish_time IS NULL'''
        else:
            return json.dumps({})
            sql = '''SELECT *, r.rink as rink_name FROM games g
                    inner join rinks r
                    on g.rink = r.rink_id
                    WHERE finish_time IS NOT NULL'''

        games = cursor.execute(sql).fetchall()

        for game in games:
            sql = '''SELECT player_id,
                        cd.display,
                        cd.display_id,
                        p.first_name,
                        p.last_name,
                        club.logo,
                        c.competitor_id,
                        c.score,
                        c.sets FROM competitors AS c
                    INNER JOIN players AS p
                    ON c.player = p.player_id 
                    INNER JOIN displays AS cd
                    ON c.display = cd.display_id
                    INNER JOIN clubs AS club
                    ON p.club = club.club_id
                    WHERE c.game = ?'''
            params = [game['game_id']]
            players = cursor.execute(sql, params).fetchall()

            competitors = []
            for player in players:
                competitors.append({
                    "player_id": player['player_id'],
                    "first_name": player['first_name'],
                    "last_name": player['last_name'],
                    "competitor_id": player['competitor_id'],
                    "score": player['score'],
                    "sets": player['sets'],
                    "logo": player['logo'],
                    "display": {'display':player['display'],'display_id':player['display_id']},
                 })
            
            parsed_rows.append({
                "game_id": game["game_id"],
                "name": game["name"],
                "game_type": game["game_type"],
                "competition": {"competition":game["comp_name"], "competition_id":game["competition_id"]},
                "gender": game["gender"],
                "round": game["round"],
                "grade": game["grade"],
                "rink": {"rink":game["rink_name"], "rink_id":game["rink_id"], "ip":game["ip"]},
                "ends": game["ends"],
                "start_time": game["start_time"],
                "finish_time": game["finish_time"],
                "winner": game["winner"],
                "competitors": competitors
            })

        return json.dumps(parsed_rows)


    def get_players(self):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        parsed_rows = []
        players = cursor.execute("SELECT * FROM players").fetchall()

        for player in players:
            parsed_rows.append({
                "player_id": player["player_id"],
                "first_name": player["first_name"],
                "last_name": player["last_name"],
                "club": player["club"],
                "address": player["address"],
                "email": player["email"],
            })

        return json.dumps(parsed_rows)

    def get_clubs(self):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        parsed_rows = []
        clubs = cursor.execute("SELECT * FROM clubs").fetchall()

        for club in clubs:
            parsed_rows.append({
                "club_id": club["club_id"],
                "club_name": club["club_name"],
                "logo": club["logo"],
                "address": club["address"],
                "contact_details": club["contact_details"],
            })

        return json.dumps(parsed_rows)


    def create_game(self, js):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        utc = datetime.datetime.utcnow().replace(tzinfo=pytz.timezone('UTC'))

        sql = "INSERT INTO games (competition, rink, start_time) VALUES(?, ?, ?);"

        not_filled = False

        ignore_list = ['game_id',
            'name',
            'ends',
            'start_time',
            'finish_time',
            'coordinator_ip',
            'winner',
        ]

        for i in js:
            if i in ignore_list:
                continue

            if js[i]:
                for j in js[i]:
                    if type(js[i][j]) == dict:
                        for k in js[i][j]:
                            if js[i][j][k]:
                                continue
                            else:
                                js[i][j][k] = 'border border-danger'
                                not_filled = True
                    else:
                        continue
            else:
                js[i] = 'border border-danger'
                not_filled = True

        if not_filled:
            return js

        try:
            params = [js["competition"]["competition_id"], js["rink"]["rink_id"], utc]
            cursor.execute(sql, params)

            game_id = cursor.lastrowid

            js['game_id'] = game_id
            for player in js['competitors']:
                sql = "INSERT INTO competitors (player, game, display) VALUES(?, ?, ?);"
                params = [js['competitors'][player]['player_id'],
                    game_id,
                    js['competitors'][player]['display']['display_id']]
                cursor.execute(sql, params)

            r = con.commit()
            con.close()

            x = threading.Thread(target=self.write_scoreboard, args=(js,))
            x.start()
            return "success"
        except:
            import traceback
            print(js)
            print(traceback.format_exc())
            return js
        # except:
            # return "could not create game"
            # exceptiondata = traceback.format_exc().splitlines()
            # exceptionarray = [exceptiondata[-1]] + exceptiondata[1:-1]
            # return exceptionarray[0]


    def add_score(self, js):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        cmd = "UPDATE competitors SET score = ? WHERE player = ? and game = ?"
        params = (js["score"], js["player_id"], js["game_id"])
        res = cursor.execute(cmd, params)
        print(res.fetchone())
        if res.fetchone() is None:
            con.commit()
        return {
                "status": "ok",
        }



    def write_scoreboard(self, js):
        try:
            response = requests.post('http://'+js["rink"]["ip"]+'/create_game', json = js, timeout=2)
            return response.status_code
        except Exception as e:
            print("FAIL", e)
            return "fail"


    def update_scoreboard(self, js):
        try:
            response = requests.post('http://'+js["rink"]["ip"]+'/update_game', json = js, timeout=2)
            return response.status_code
        except Exception as e:
            print("FAIL", e)
            return "fail"


    def create_rink(self, js):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        cmd = "INSERT INTO rinks (ip, rink) VALUES (?, ?)"
        params = (js['ip'], js['rink'])
        
        res = cursor.execute(cmd,params)
        if res.fetchone() is None:
            con.commit()
        return {
                "status": "ok",
        }


    def create_masterboard(self, js):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        cmd = "INSERT INTO masterboards (ip, masterboard) VALUES (?, ?)"
        params = (js['ip'], js['masterboard'])
        
        res = cursor.execute(cmd,params)
        if res.fetchone() is None:
            con.commit()
        return {
                "status": "ok",
        }

        ######################


    def create_sponsor(self, logo_file, sponsor_name):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        print("FILE: ", logo_file)
        print("NAME: ", sponsor_name)

        try:
            logo_file.save("./assets/"+logo_file.filename)
        except:
            pass


        sql = 'INSERT INTO sponsors (sponsor, sponsor_logo) VALUES(?, ?);'
        params = [sponsor_name, logo_file.filename]

        cursor.execute(sql, params)
        con.commit()


    def update_sponsor(self, logo_file, sponsor_name):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        try:
            logo_file.save("./assets/"+logo_file.filename)
        except:
            pass

        cmd = "UPDATE sponsors SET sponsor = ?, sponsor_logo = ? WHERE sponsor_id = ?"
        params = [sponsor_name['sponsor'], logo_file.filename, sponsor_name['sponsor_id']]
        res = cursor.execute(cmd, params)
        if res.fetchone() is None:
            con.commit()
        return {
                "status": "ok",
        }


    def update_club(self, js, logo):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        try:
            logo.save("./assets/"+logo.filename)
        except:
            pass

        cmd = "UPDATE clubs SET club_name = ?, logo = ?, address = ?, contact_details = ? WHERE club_id = ?"
        params = [js['club_name'], logo.filename, js['address'], js['contact_details'], js['club_id']]
        res = cursor.execute(cmd, params)
        if res.fetchone() is None:
            con.commit()
        return {
                "status": "ok",
        }


    def update_game(self, js):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        cursor = con.cursor()

        cmd = "UPDATE games SET name = ?,game_type = ?,competition = ?,gender = ?,round = ?,grade = ?,rink = ?,ends = ?,start_time = ?,finish_time = ?,winner = ? WHERE game_id = ?"
        params = (js['name'],js['game_type'], js["competition"]["competition_id"], js['gender'], js['round'], js['grade'], js["rink"]["rink_id"], js['ends'], js['start_time'], js['finish_time'], js['winner'], js['game_id'] )

        res = cursor.execute(cmd, params)

        for competitor in js['competitors']:
            cmd = "UPDATE competitors SET score = ?,display = ? WHERE competitor_id = ? AND game = ?"
            params = (competitor['score'], competitor['display']['display_id'], competitor['competitor_id'], js['game_id'])
            res = cursor.execute(cmd, params)

        if res.fetchone() is None:
            con.commit()
            con.close()

            x = threading.Thread(target=self.update_scoreboard, args=(js,))
            x.start()
            return


    def finish_game(self, js):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        cursor = con.cursor()

        utc = datetime.datetime.utcnow().replace(tzinfo=pytz.timezone('UTC'))
        js['finish_time'] = utc

        cmd = "UPDATE games SET finish_time = ?,winner = ? WHERE game_id = ?"
        params = (js['finish_time'], js['winner'], js['game_id'] )

        js['finish_time'] = str(js['finish_time'])

        res = cursor.execute(cmd, params)

        if res.fetchone() is None:
            con.commit()
            con.close()

            x = threading.Thread(target=self.update_scoreboard, args=(js,))
            x.start()
            return


    def update_rink(self, js):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        cmd = "UPDATE rinks SET ip = ?, rink = ? WHERE rink_id = ?"
        params = [js['ip'], js['rink'], js['rink_id']]
        res = cursor.execute(cmd, params)
        if res.fetchone() is None:
            con.commit()
        return {
                "status": "ok",
        }


    def update_bigboards(self, js):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        cmd = "UPDATE bigboards SET bigboard = ?, ip = ?, current_layout = ? WHERE bigboard_id = ?"
        params = [js['bigboard'], js['ip'], js['current_layout']['layout_id'], js['bigboard_id']]
        res = cursor.execute(cmd, params)
        if res.fetchone() is None:
            con.commit()
            x = threading.Thread(target=self.write_bigboard, args=(js,))
            x.start()
        return {
                "status": "ok",
        }


    def write_bigboard(self, js):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        cmd = """SELECT rinks.rink_id, layouts.layout, rinks.ip from bigboard_layout_link bll
                INNER JOIN rinks ON bll.rink = rinks.rink_id
                INNER JOIN layouts ON bll.layout = layouts.layout_id
                WHERE bll.layout = ?"""
        params = [js['current_layout']['layout_id']]
        res = cursor.execute(cmd, params)

        ips = []
        for rink in res:
            ips.append((rink['rink_id'], rink['layout'], rink['ip']))

        try:
            response = requests.post('http://'+js['ip']+'/setup', json = ips)
            return response.status_code
        except:
            return "fail"


    def update_club(self, js):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        cmd = "UPDATE clubs SET club_name = ?, address = ?, contact_details = ? WHERE club_id = ?"
        params = [js['club_name'], js['address'], js['contact_details'], js['club_id']]
        res = cursor.execute(cmd, params)
        if res.fetchone() is None:
            con.commit()
        return {
                "status": "ok",
        }

    def update_player(self, js):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        cmd = "UPDATE players SET first_name = ?, last_name = ?, club = ?, bowls_number = ?, grade = ? WHERE player_id = ?"
        params = [js['first_name'], js['last_name'], js['club'], js['bowls_number'], js['grade'], js['player_id']]
        res = cursor.execute(cmd, params)
        if res.fetchone() is None:
            con.commit()
        return {
                "status": "ok",
        }



