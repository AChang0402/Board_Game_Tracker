from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import games_model

DATABASE = "board_game_tracker_schema"

class Play:
    def __init__(self,data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.game_id = data['game_id']
        self.date = data['date']
        self.num_players = data['num_players']
        self.winner = data['winner']

    @classmethod
    def add_play(cls,data):
        query = """
                INSERT INTO plays (user_id, game_id, date, num_players, winner)
                VALUES (%(user_id)s, %(game_id)s, %(date)s, %(num_players)s, %(winner)s);
                """
        return connectToMySQL(DATABASE).query_db(query,data)
    
    @classmethod
    def edit_play(cls,data):
        query = """
                UPDATE plays
                SET date=%(date)s, num_players=%(num_players)s, winner=%(winner)s
                WHERE id = %(id)s;
                """
        return connectToMySQL(DATABASE).query_db(query,data)
    
    @classmethod
    def delete_play(cls,data):
        query = """
                DELETE from plays where id = %(id)s;
                """
        return connectToMySQL(DATABASE).query_db(query,data)
    
    @classmethod
    def get_plays(cls,data):
        query = """
                SELECT * from plays
                JOIN games ON plays.game_id=games.id
                WHERE user_id = %(user_id)s
                ORDER BY plays.date desc;
                """
        results = connectToMySQL(DATABASE).query_db(query,data)
        # if len(results)<1:
        #     return False
        plays = []
        for row in results:
            this_play = cls(row)
            game_data = {
                **row,
                'id':row['games.id'],
                'created_at':row['games.created_at'],
                'updated_at':row['games.updated_at']
            }
            game = games_model.Game(game_data)
            this_play.game = game
            plays.append(this_play)
        return plays
        
    @classmethod
    def get_play_by_id(cls,data):
        query = """
                SELECT * FROM plays where id = %(id)s;
                """
        result = connectToMySQL(DATABASE).query_db(query,data)
        return cls(result[0])

    @staticmethod
    def count_plays(data):
        query = """
                SELECT user_id, game_id, count(id) 
                FROM plays where user_id=%(user_id)s and game_id=%(game_id)s
                GROUP BY game_id, user_id;
                """
        result = connectToMySQL(DATABASE).query_db(query,data)
        if len(result)<1:
            return 0
        else:
            return (result[0]['count(id)'])
        
    @staticmethod
    def get_plays_count(data):
        query = """
                SELECT user_id, game_id, games.title, games.api_id, count(plays.id) 
                FROM plays JOIN games ON plays.game_id=games.id
                where user_id=%(user_id)s
                GROUP BY game_id, user_id
                ORDER BY count(plays.id) desc;
                """
        return connectToMySQL(DATABASE).query_db(query,data)
    
    @staticmethod
    def validate_play(data):
        is_valid=True
        if len(data['date'])<1:
            flash("Date is a required field", "play")
            is_valid=False
        if data['num_players'] != "":
            if int(data['num_players'])<1:
                flash("# of players must be at least 1","play")
                is_valid=False
        return is_valid
