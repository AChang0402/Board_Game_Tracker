from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import plays_model

DATABASE = "board_game_tracker_schema"

class Game:
    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.api_id = data['api_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # @classmethod
    # def get_game_by_API(cls,data):
    #     if not Game.game_in_DB(data):
    #         return False

    @classmethod
    def get_game_by_api(cls, data):
        query = """
                SELECT * from games WHERE api_id = %(api_id)s;
                """
        result = connectToMySQL(DATABASE).query_db(query,data)
        if len(result)<1:
            return False
        return cls(result[0])

    @classmethod
    def create_game(cls, data):
        id = Game.game_in_DB(data)
        if id:
            return id
        query = """
                INSERT INTO games (title, api_id)
                VALUES (%(title)s, %(api_id)s);
                """
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def game_in_DB(cls, data):
        query = """
                SELECT * from games where api_id=%(api_id)s;
                """
        result = connectToMySQL(DATABASE).query_db(query,data)
        if len(result)<1:
            return False
        else:
            return result[0]['id']
        
    @classmethod
    def add_collection(cls,data):
        query = """
                INSERT INTO collection (user_id, game_id)
                VALUES (%(user_id)s,%(game_id)s);
                """
        return connectToMySQL(DATABASE).query_db(query,data)
    
    @classmethod
    def remove_collection(cls,data):
        query = """
                DELETE FROM collection WHERE user_id=%(user_id)s AND game_id=%(game_id)s
                """
        return connectToMySQL(DATABASE).query_db(query,data)
    
    @classmethod
    def add_tracked(cls,data):
        query = """
                INSERT INTO tracked (user_id, game_id)
                VALUES (%(user_id)s,%(game_id)s);
                """
        return connectToMySQL(DATABASE).query_db(query,data)
    
    @classmethod
    def remove_tracked(cls,data):
        query = """
                DELETE FROM tracked WHERE user_id=%(user_id)s AND game_id=%(game_id)s;
                """
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def add_rating(cls,data):
        query = """
                INSERT INTO ratings (user_id, game_id, rating)
                VALUES (%(user_id)s, %(game_id)s, %(rating)s);
                """
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def edit_rating(cls,data):
        query = """
                UPDATE ratings
                SET rating=%(rating)s
                WHERE user_id=%(user_id)s AND game_id=%(game_id)s;
                """
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def delete_rating(cls,data):
        query = """
                DELETE FROM ratings WHERE user_id=%(user_id)s AND game_id=%(game_id)s;
                """
        return connectToMySQL(DATABASE).query_db(query,data)
    

    @classmethod
    def get_collection(cls,data):
        query = """
                SELECT * FROM collection 
                join games on collection.game_id = games.id
                where user_id = %(user_id)s
                order by games.title asc;
                """
        results = connectToMySQL(DATABASE).query_db(query,data)
        games=[]
        for row in results:
            this_game=cls(row)
            this_game.rating= Game.in_ratings(row)
            this_game.count_plays = plays_model.Play.count_plays(row)
            games.append(this_game)
        return games
    
    @classmethod
    def get_tracked(cls,data):
        query = """
                SELECT * FROM games
                JOIN tracked on games.id=tracked.game_id
                WHERE user_id=%(user_id)s
                ORDER BY tracked.created_at desc;
                """
        results = connectToMySQL(DATABASE).query_db(query,data)
        games=[]
        for row in results:
            this_game=cls(row)
            this_game.own = Game.in_collection(row)
            games.append(this_game)
        return games
    
    @classmethod
    def get_ratings(cls,data):
        query = """
                SELECT * FROM games
                JOIN ratings on games.id=ratings.game_id
                WHERE user_id=%(user_id)s
                ORDER BY ratings.rating desc;
                """
        results = connectToMySQL(DATABASE).query_db(query,data)
        games=[]
        for row in results:
            this_game=cls(row)
            this_game.rating = row['rating']
            games.append(this_game)
        return games
    
    @classmethod
    def get_highest_rated(cls):
        query = """
                SELECT games.*, avg(ratings.rating) 
                FROM games join ratings on games.id = ratings.game_id
                GROUP BY games.id
                order by avg(ratings.rating) desc
                """
        results = connectToMySQL(DATABASE).query_db(query)
        games=[]
        print(results)
        for row in results:
            this_game=cls(row)
            this_game.avgrating = row['avg(ratings.rating)']
            games.append(this_game)
        return games

    @staticmethod
    def in_collection(data):
        query = """
                SELECT * FROM collection
                JOIN games ON collection.game_id=games.id
                WHERE collection.user_id=%(user_id)s AND games.api_id=%(api_id)s;
                """
        result = connectToMySQL(DATABASE).query_db(query,data)
        if len(result)<1:
            return False
        else:
            return True
        
    @staticmethod
    def in_tracked(data):
        query = """
                SELECT * FROM tracked
                JOIN games ON tracked.game_id=games.id
                WHERE tracked.user_id=%(user_id)s AND games.api_id=%(api_id)s;
                """
        result = connectToMySQL(DATABASE).query_db(query,data)
        if len(result)<1:
            return False
        else:
            return True
        
    @staticmethod
    def in_ratings(data):
        query = """
                SELECT * FROM ratings
                JOIN games ON ratings.game_id=games.id
                WHERE ratings.user_id=%(user_id)s AND games.api_id=%(api_id)s;
                """
        result = connectToMySQL(DATABASE).query_db(query,data)
        if len(result)<1:
            return False
        else:
            return result[0]['rating']
        
    @staticmethod
    def validate_rating(data):
        is_valid=True
        if len(data['rating'])<1:
            flash("Enter rating (0-10)", "rating")
        elif float(data['rating'])> 10 or float(data['rating'])<0:
            flash("Rating must be between 0-10", "rating")
            is_valid=False
        return is_valid
