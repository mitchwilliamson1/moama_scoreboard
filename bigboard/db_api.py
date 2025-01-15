import datetime
import sqlite3
import json
import pickle
import pytz
import requests
import config


local_tz = pytz.timezone("Australia/Sydney")

class Big_Board:
    def __init__(self):
        self.db_path = "bigboard.db"

    def encode_if_required(self, str_val):
        try:
            return str_val.encode()
        except Exception:
            return str_val


    def setup(self, js):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        sql = "DELETE FROM scoreboards_layout;"
        cursor.execute(sql)

        sql = "INSERT INTO scoreboards_layout (scoreboards_layout_id, layout, ip) VALUES(?, ?, ?);"
        game_id = cursor.executemany(sql, js)

        con.commit()


    def get_scoreboards(self):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        player_1_score=0
        player_2_score=0
        ends=0

        player_1_logo = 'charls.jpeg'
        player_2_logo = 'away.jpeg'

        coordinator_ip = '192.168.15.200:8000'

        Backboard = {
                    'scoreboards':{},
                    'layout':'',
                    'masterboard':{
                        'coordinator_ip':'',
                        'ends':0,
                        'competitors':{
                            '1':{
                                'score':0,
                                "logo": "moama_steamers.png"
                            },
                            '2':{
                                'score':0,
                                "logo": "away.jpeg"
                            },
                        }
                        }
                    }

        ips = cursor.execute('''SELECT * FROM scoreboards_layout''').fetchall()

        for ip in ips:
            Backboard['layout'] = ip['layout']
            try:
                response = requests.get('http://'+ip['ip']+'/get_game', timeout=0.2)
                scoreboard = json.loads(response.content)
            except:
                scoreboard = config.DEFAULT_GAME

            Backboard['scoreboards'][ip['scoreboards_layout_id']] = scoreboard

            Backboard['masterboard']['ends'] += int(scoreboard['ends'])
            Backboard['masterboard']['coordinator_ip'] = scoreboard['coordinator_ip']

            for competitor in scoreboard['competitors']:
                Backboard['masterboard']['competitors'][competitor]['score'] += int(scoreboard['competitors'][competitor]['score'])
                Backboard['masterboard']['competitors'][competitor]['logo'] = scoreboard['competitors'][competitor]['logo']


        return json.dumps(Backboard, indent=4)

############# YOU WILL NEED THIS ################

        #     ends += int(data[0]['ends'])
        #     coordinator_ip = data[0]['coordinator']

        #     for i in data[0]['competitors']:
        #         if i['competitor_id'] == 1:
        #             player_1_score += int(i['score'])
        #             player_1_logo = i['logo']
        #         if i['competitor_id'] == 2:
        #             player_2_score += int(i['score'])
        #             player_2_logo = i['logo']

        # for i in DEFAULT_MASTER[0]['competitors']:
        #     if i['player_id'] == 1:
        #         i['score'] = str(player_1_score)
        #         i['logo'] = str(player_1_logo)
        #     if i['player_id'] == 2:
        #         i['score'] = str(player_2_score)
        #         i['logo'] = str(player_2_logo)

        # DEFAULT_MASTER[0]['ends'] = ends
        # DEFAULT_MASTER[0]['coordinator_ip'] = coordinator_ip

        # return json.dumps(DEFAULT_MASTER, indent=4, sort_keys=True)


    def write_coordinator_score(self, js):
        response = requests.post('http://'+config.COORDINATOR_IP+'/games/add_score', json = js)
        print(response)
        return response.status_code


    def write_coordinator_ends(self, js):
        response = requests.post('http://'+config.COORDINATOR_IP+'/games/add_ends', json = js)
        print(response)
        return response.status_code

