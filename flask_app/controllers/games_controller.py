from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.users_model import User
from flask_app.models.games_model import Game
from flask_app.models.plays_model import Play

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game/<string:api_id>')
def view_game(api_id):
    if 'id' not in session:
        return render_template('view_game.html', api_id=api_id)
    game = Game.get_game_by_api({'api_id':api_id})
    data={
        'user_id':session['id'],
        'api_id': api_id,
    }
    in_collection = Game.in_collection(data)
    in_tracking = Game.in_tracked(data)
    in_ratings = Game.in_ratings(data)
    if not game:
        plays = 0
    else:
        data['game_id']=game.id
        plays = Play.count_plays(data)
    return render_template('view_game.html',api_id=api_id, in_collection=in_collection, in_tracking=in_tracking, in_ratings=in_ratings, plays=plays)

@app.route('/collection/add/<string:api_id>', methods=['post'])
def collection_add(api_id):
    if 'id' not in session:
        flash("Register/Login to access all features!", "user")
        return redirect('/login_register')
    game_id = Game.create_game(request.form)
    data = {
        'user_id':session['id'],
        'game_id':game_id
    }
    Game.add_collection(data)
    return redirect('/game/'+api_id)

@app.route('/collection/remove/<string:api_id>', methods=['post'])
def collection_remove(api_id):
    if 'id' not in session:
        flash("Register/Login to access all features!", "user")
        return redirect('/login_register')
    game = Game.get_game_by_api({'api_id':api_id})
    data = {
        'user_id':session['id'],
        'game_id': game.id
    }
    Game.remove_collection(data)
    return redirect('/game/'+api_id)

@app.route('/tracked/add/<string:api_id>', methods=['post'])
def tracked_add(api_id):
    if 'id' not in session:
        flash("Register/Login to access all features!", "user")
        return redirect('/login_register')
    game_id = Game.create_game(request.form)
    data = {
        'user_id':session['id'],
        'game_id':game_id
    }
    Game.add_tracked(data)
    return redirect('/game/'+api_id)

@app.route('/tracked/remove/<string:api_id>', methods=['post'])
def tracked_remove(api_id):
    if 'id' not in session:
        flash("Register/Login to access all features!", "user")
        return redirect('/login_register')
    game = Game.get_game_by_api({'api_id':api_id})
    data = {
        'user_id':session['id'],
        'game_id': game.id
    }
    Game.remove_tracked(data)
    return redirect('/game/'+api_id)

@app.route('/rating/add/<string:api_id>', methods=['post'])
def rating_add(api_id):
    if 'id' not in session:
        flash("Register/Login to access all features!", "user")
        return redirect('/login_register')
    if not Game.validate_rating(request.form):
        return redirect('/game/'+api_id)
    game_id = Game.create_game(request.form)
    data = {
        **request.form,
        'user_id':session['id'],
        'game_id':game_id
    }
    Game.add_rating(data)
    return redirect('/game/'+api_id)

@app.route('/rating/edit/<string:api_id>', methods=['post'])
def rating_edit(api_id):
    if 'id' not in session:
        flash("Register/Login to access all features!", "user")
        return redirect('/login_register')
    if not Game.validate_rating(request.form):
        return redirect('/game/'+api_id)
    game = Game.get_game_by_api({'api_id':api_id})
    data = {
        **request.form,
        'user_id':session['id'],
        'game_id': game.id
    }
    Game.edit_rating(data)
    return redirect('/game/'+api_id)

@app.route('/rating/delete/<string:api_id>', methods=['post'])
def rating_delete(api_id):
    if 'id' not in session:
        flash("Register/Login to access all features!", "user")
        return redirect('/login_register')
    game = Game.get_game_by_api({'api_id':api_id})
    data = {
        'user_id':session['id'],
        'game_id': game.id
    }
    Game.delete_rating(data)
    return redirect('/game/'+api_id)


@app.route('/collection')
def view_collection():
    if 'id' not in session:
        flash("Register/Login to access all features!", "user")
        return redirect('/login_register')
    games = Game.get_collection({'user_id':session['id']})
    return render_template('collection.html', games=games)

@app.route('/tracking')
def tracking():
    if 'id' not in session:
        flash("Register/Login to access all features!", "user")
        return redirect('/login_register')
    games = Game.get_tracked({'user_id':session['id']})
    return render_template('tracked.html', games=games)

@app.route('/ratings')
def ratings():
    if 'id' not in session:
        flash("Register/Login to access all features!", "user")
        return redirect('/login_register')
    games = Game.get_ratings({'user_id':session['id']})
    return render_template('ratings.html', games=games)

@app.route('/games/highestrated')
def highest_rated():
    games = Game.get_highest_rated()
    return render_template('highest_rated.html', games=games)