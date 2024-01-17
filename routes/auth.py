# region Imports

from gameteca import app

from flask import render_template, redirect, request, flash, session, url_for

from models.users import Users

# endregion

"""
    Creates a route for the login page.

    Parameters:
        None

    Returns:
        The rendered login.html template with the next_page parameter.
"""
@app.route('/login')
def login():
    next_page = request.args.get('next_page')

    return render_template("login.html", next_page=next_page)


"""
    Logs out the user by setting the 'user_is_logged' session variable to None.
    Displays a flash message indicating that the user has been successfully logged out.
    Redirects the user to the 'login' page.

    Parameters:
        None

    Returns:
        None
"""
@app.route('/logout')
def logout():
    session['user_is_logged'] = None

    flash('Usuário deslogado com sucesso!')

    return redirect(url_for('login'))


"""
    Authenticates a user by checking their credentials and logs them in if the
    credentials are valid.

    Parameters:
        None

    Returns:
        None
"""
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