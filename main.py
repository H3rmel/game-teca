# region Imports

from flask import Flask, render_template, request, redirect, session, flash, url_for

from models.game import Game
from models.user import User

from utils.check_session import check_session_and_render

# endregion

# App Instance
app = Flask(__name__)
app.secret_key = 'alura'

# region Views


@app.route('/')
def home():
    return check_session_and_render('home', 'list.html', title='Jogos', games=gamesList)


@app.route('/new_game')
def new_game():
    return check_session_and_render('new_game', 'new.html', title='Novo jogo')


@app.route('/login')
def login():
    next_page = request.args.get('next_page')

    return render_template("login.html", next_page=next_page)

# endregion

# region Methods


@app.route('/create', methods=["POST"])
def create():
    if request.method == "POST":
        name = request.form['name']
        category = request.form['category']
        platform = request.form['platform']

        new_game = Game(name, category, platform)
        gamesList.append(new_game)

        return redirect(url_for('home'))
    else:
        return render_template("error.html")


@app.route('/auth', methods=["POST"])
def auth():
    if request.method == "POST":
        if request.form['user'] in users:
            user = users[request.form['user']]

            if request.form['password'] == user.password:
                session['user_is_logged'] = user.nickname

                flash(user.nickname + ' logado com sucesso!')

                next_page = request.form['next_page']

                if next_page == 'None':
                    return redirect(next_page)
                else:
                    return redirect(url_for('home'))
            else:
                flash('Senha inválida!')

                return redirect(url_for('login'))
        else:
            flash('Senha inválida!')

            return redirect(url_for('login'))
    else:
        return render_template("error.html")


@app.route('/logout')
def logout():
    session['user_is_logged'] = None

    flash('Usuário deslogado com sucesso!')

    return redirect(url_for('login'))

# endregion


if __name__ == "__main__":
    app.run(debug=True)
