# region Imports

from gameteca import app, db

from flask import render_template, redirect, request, flash, url_for, session, send_from_directory

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

        upload_path = app.config['UPLOAD_PATH']

        archive = request.files['archive']
        archive.save(f'{upload_path}/thumbnail{new_game.id}.jpg')

        return redirect(url_for('home'))
    else:
        return render_template("error.html")


@app.route('/update', methods=["POST"])
def update():
    if request.method == "POST":
        game_to_update = Games.query.filter_by(id=request.form['id']).first()

        game_to_update.name = request.form['name']
        game_to_update.category = request.form['category']
        game_to_update.platform = request.form['platform']

        db.session.add(game_to_update)
        db.session.commit()

        return redirect(url_for('home'))
    else:
        return render_template("error.html")


@app.route('/delete/<int:id>', methods=["POST"])
def delete(id):
    if request.method == "POST":
        if 'user_is_logged' not in session or session['user_is_logged'] == None:
            return redirect(url_for('login'))

        Games.query.filter_by(id=id).delete()

        db.session.commit()

        flash('Jogo removido com sucesso!')

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


@app.route('/content/<name_archive>')
def image(name_archive):
   return send_from_directory(app.static_folder, 'content/' + name_archive, as_attachment=True)


@app.route('/logout')
def logout():
    session['user_is_logged'] = None

    flash('Usuário deslogado com sucesso!')

    return redirect(url_for('login'))
