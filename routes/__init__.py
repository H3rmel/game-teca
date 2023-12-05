# region Imports

from gameteca import app, db

from flask import render_template, redirect, request, flash, url_for, session

from models.games import Games
from models.users import Users

# endregion


@app.route('/create', methods=["POST"])
def create():
    if request.method == "POST":
        name = request.form['name']
        category = request.form['category']
        platform = request.form['platform']

        game = Games.query.filter_by(name=name).first()

        if game:
            flash('Este jogo já existe!')

            return redirect(url_for('home'))

        new_game = Games(name=name, category=category, platform=platform)

        db.session.add(new_game)
        db.session.commit()

        return redirect(url_for('home'))
    else:
        return render_template("error.html")


@app.route('/auth', methods=["POST"])
def auth():
    user = Users.query.filter_by(nickname=request.form['user']).first()

    if request.method == "POST":
        if user:
            if request.form['password'] == user.password:
                session['user_is_logged'] = user.nickname

                flash(user.nickname + ' logado com sucesso!')

                next_page = request.form['next_page']

                if next_page != 'None':
                    return redirect(next_page)
                else:
                    return redirect(url_for('home'))
            else:
                flash('Senha inválida!')

                return redirect(url_for('login'))
        else:
            flash('Usuário inválido')

            return redirect(url_for('login'))
    else:
        render_template('error.html')


@app.route('/logout')
def logout():
    session['user_is_logged'] = None

    flash('Usuário deslogado com sucesso!')

    return redirect(url_for('login'))
