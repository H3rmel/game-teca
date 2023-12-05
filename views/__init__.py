# region Imports

from gameteca import app

from flask import render_template, request

from models.games import Games

from utils.check_session import check_session_and_render

# endregion


@app.route('/')
def home():
    gamesList = Games.query.order_by(Games.id)

    return check_session_and_render('home', 'list.html', title='Jogos', games=gamesList)


@app.route('/new_game')
def new_game():
    return check_session_and_render('new_game', 'new.html', title='Novo jogo')


@app.route('/login')
def login():
    next_page = request.args.get('next_page')

    return render_template("login.html", next_page=next_page)
