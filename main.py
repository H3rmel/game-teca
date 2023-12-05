# region Imports

from flask import Flask, render_template, request, redirect, session, flash, url_for

from flask_sqlalchemy import SQLAlchemy

from utils.check_session import check_session_and_render

# endregion

# region App Instance

app = Flask(__name__)
app.secret_key = 'alura'

app.config['SQLALCHEMY_DATABASE_URI'] = \
    '{SGBD}://{user}:{password}@{host}/{db}'.format(
        SGBD = 'mysql+mysqlconnector',
        user = 'wsl_root',
        password = 'capreo9709',
        host = '127.0.0.1',
        db = 'gameteca'
    )

db = SQLAlchemy(app)

class Games(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(40), nullable=False)
    platform = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<Name %s>' % self.name

class Users(db.Model):
    name = db.Column(db.String(50), primary_key=True)
    nickname = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name


# endregion

# region Views


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

# endregion

# region Methods


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
    user = Users.query.filter_by(nickname = request.form['user']).first()

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

# endregion


if __name__ == "__main__":
    app.run(debug=True)
