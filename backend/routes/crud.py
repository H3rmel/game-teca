# region Imports

from gameteca import app, db

from flask import render_template, redirect, request, flash, url_for, session, send_from_directory

from models.games import Games

from utils.check_session import check_session_and_render
from utils.forms import GameForm
from utils.images import delete_image, get_image
import time

# endregion

"""
    Renders the home page of the application.

    :return: A rendered HTML template with the home page content.
    :rtype: str
"""
@app.route('/')
def home():
    games_list = Games.query.order_by(Games.id)

    return check_session_and_render('home', 'list.html', title='Jogos', games=games_list)


"""
    A route decorator that handles requests to the '/new' endpoint.

    Returns:
        The result of the 'check_session_and_render' function.

    Raises:
        None.
"""
@app.route('/new')
def new():
    form = GameForm()
    
    return check_session_and_render('new', 'new.html', title='Novo jogo', form=form)


"""
    Create a new game in the database.

    Parameters:
    None

    Returns:
    - If the request method is POST and the game does not already exist in the database, it creates a new game entry with the provided name, category, and platform. It saves the uploaded cover image file and redirects the user to the home page.
    - If the request method is not POST, it renders the error.html template.

    Raises:
    None
"""
@app.route('/create', methods=["POST"])
def create():
    if request.method == "POST":
        form = GameForm(request.form);
        
        if not form.validate_on_submit():
            flash('Falha na validação do formulário!')
            return redirect(url_for('new'))
        
        name = form.name.data
        category = form.category.data
        platform = form.platform.data

        game = Games.query.filter_by(name=name).first()

        if game:
            flash('Este jogo já existe!')

            return redirect(url_for('home'))

        new_game = Games(name=name, category=category, platform=platform)

        db.session.add(new_game)
        db.session.commit()

        upload_path = app.config['UPLOAD_PATH']
        
        timestamp = time.time()

        archive = request.files['archive']
        archive.save(f'{upload_path}/cover{new_game.id}-{timestamp}.jpg')

        return redirect(url_for('home'))
    else:
        return render_template("error.html")


"""
    A route decorator for handling GET requests to the '/edit/<int:id>' URL.

    Parameters:
    - id (int): The ID of the game to be edited.

    Returns:
    - str: The rendered template for editing the game with the specified ID.
"""
@app.route('/edit/<int:id>')
def edit(id):
    game_to_edit = Games.query.filter_by(id=id).first()
    
    form = GameForm()
    
    form.name.data = game_to_edit.name
    form.category.data = game_to_edit.category
    form.platform.data = game_to_edit.platform
    
    game_cover = get_image(id)
    
    return check_session_and_render('edit', 'edit.html', title='Editando jogo', id=game_to_edit.id, game_cover=game_cover, form=form)


"""
    Updates a game in the database based on the provided form data.

    Parameters:
    - None

    Returns:
    - None

    Side Effects:
    - Modifies the name, category, and platform of the game with the provided ID in the database.
    - Commits the changes to the database.
    - Redirects the user to the home page if the request method is POST.
    - Renders the error.html template if the request method is not POST.
"""
@app.route('/update', methods=["POST"])
def update():
    if request.method == "POST":
        game_to_update = Games.query.filter_by(id=request.form['id']).first()

        form = GameForm(request.form)
        
        if not form.validate_on_submit():
            flash('Falha na validação do formulário!')
            return redirect(url_for('new'))

        game_to_update.name = form.name.data
        game_to_update.category = form.category.data
        game_to_update.platform = form.platform.data

        db.session.add(game_to_update)
        db.session.commit()
        
        upload_path = app.config['UPLOAD_PATH']

        timestamp = time.time()
        
        delete_image(game_to_update.id)

        archive = request.files['archive']
        archive.save(f'{upload_path}/cover{game_to_update.id}-${timestamp}.jpg')

        return redirect(url_for('home'))
    else:
        return render_template("error.html")


"""
    Delete a game from the database based on its ID.

    Parameters:
        id (int): The ID of the game to be deleted.

    Returns:
        str: A redirect to the home page if the game is deleted successfully,
        otherwise a rendered error template.
"""
@app.route('/delete/<int:id>', methods=["POST"])
def delete(id):
    if request.method == "POST":
        if 'user_is_logged' not in session or session['user_is_logged'] == None:
            return redirect(url_for('login'))

        Games.query.filter_by(id=id).delete()

        delete_image(id)

        db.session.commit()

        flash('Jogo removido com sucesso!')

        return redirect(url_for('home'))
    else:
        return render_template("error.html")


"""
   A function that handles the route '/uploads/<name_archive>' and returns the file specified by 'name_archive' from the 'uploads' directory.

   Parameters:
   - name_archive (str): The name of the file to be retrieved.

   Returns:
   - The file specified by 'name_archive' from the 'uploads' directory.
"""
@app.route('/uploads/<name_archive>')
def image(name_archive):
   return send_from_directory('uploads', name_archive)
