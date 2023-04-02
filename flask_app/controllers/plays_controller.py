from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.users_model import User
from flask_app.models.games_model import Game
from flask_app.models.plays_model import Play

@app.route('/plays/addplay/<string:api_id>')
def add_play(api_id):
    if 'id' not in session:
        flash("Register/Login to access all features!", "user")
        return redirect('/login_register')
    return render_template('add_play.html',api_id=api_id)

@app.route('/plays/addplay/<string:api_id>/submit', methods=['post'])
def add_play_submit(api_id):
    if 'id' not in session:
        flash("Register/Login to access all features!", "user")
        return redirect('/login_register')
    if not Play.validate_play(request.form):
        return redirect('/plays/addplay/'+api_id)
    game_id = Game.create_game(request.form)
    data = {
        **request.form,
        'user_id':session['id'],
        'game_id':game_id
    }
    Play.add_play(data)
    return redirect('/game/'+api_id)

@app.route('/plays/editplay/<int:play_id>/<string:api_id>')
def edit_play(play_id,api_id):
    if 'id' not in session:
        flash("Register/Login to access all features!", "user")
        return redirect('/login_register')
    play = Play.get_play_by_id({'id':play_id})
    return render_template('edit_play.html', api_id=api_id, play=play)

@app.route('/plays/editplay/<int:play_id>/submit', methods=['post'])
def edit_play_submit(play_id):
    if 'id' not in session:
        flash("Register/Login to access all features!", "user")
        return redirect('/login_register')
    if not Play.validate_play(request.form):
        return redirect('/plays/editplay/'+str(play_id)+'/'+request.form['api_id'])
    data={
        **request.form,
        'id':play_id
    }
    Play.edit_play(data)
    print(request.form)
    return redirect('/plays/log')

@app.route('/plays/deleteplay/<int:play_id>')
def delete_play(play_id):
    if 'id' not in session:
        flash("Register/Login to access all features!", "user")
        return redirect('/login_register')
    Play.delete_play({'id':play_id})
    return redirect('/plays/log')

@app.route('/plays/log')
def play_log():
    if 'id' not in session:
        flash("Register/Login to access all features!", "user")
        return redirect('/login_register')
    plays = Play.get_plays({'user_id':session['id']})
    return render_template('play_log.html',plays=plays)

@app.route('/plays/bygame')
def plays():
    if 'id' not in session:
        flash("Register/Login to access all features!", "user")
        return redirect('/login_register')
    plays = Play.get_plays_count({'user_id':session['id']})
    return render_template('plays.html', plays=plays)