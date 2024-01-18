from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators

class GameForm(FlaskForm):
    name = StringField('Nome do jogo', [validators.DataRequired(), validators.Length(min=1, max=50)])
    category = StringField('Categoria do jogo', [validators.DataRequired(), validators.Length(min=1, max=40)])
    platform = StringField('Plataforma do jogo', [validators.DataRequired(), validators.Length(min=1, max=20)])
    save = SubmitField('Salvar')
    

class UserForm(FlaskForm):
    nickname = StringField('Nickname', validators=[validators.DataRequired(), validators.Length(min=1, max=20)])
    password =  StringField('Senha', validators=[validators.DataRequired(), validators.Length(min=1, max=100)])
    save = SubmitField('Login')