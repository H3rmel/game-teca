# region Imports

import mysql.connector

from mysql.connector import errorcode

from flask_bcrypt import generate_password_hash

# endregion

# region Connection

print('Conectando...')

try:
    connection = mysql.connector.connect(
        host='127.0.0.1',
        user='gameteca',
        password='12345678'
    )

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print('Existe algo de errado com o usuário e senha.')
    else:
        print(err)

cursor = connection.cursor()

# Some commands to make sure of the integrity of the database
cursor.execute("DROP DATABASE IF EXISTS gameteca;")
cursor.execute("CREATE DATABASE gameteca;")
cursor.execute("USE gameteca;")

# endregion

# region Adding Tables

TABLES = {}

TABLES['Games'] = ('''
    CREATE TABLE `gameteca`.`games` (
      `id` INT NOT NULL AUTO_INCREMENT,
      `name` VARCHAR(50) NOT NULL,
      `category` VARCHAR(40) NOT NULL,
      `platform` VARCHAR(20) NOT NULL,
      PRIMARY KEY (`id`))
    ENGINE = InnoDB
    DEFAULT CHARACTER SET = utf8
    COLLATE = utf8_bin; ''')

TABLES['Users'] = ('''
    CREATE TABLE `gameteca`.`users` (      
      `name` VARCHAR(50) NOT NULL,
      `nickname` VARCHAR(20) NOT NULL,
      `password` VARCHAR(100) NOT NULL,
      PRIMARY KEY (`nickname`))
    ENGINE = InnoDB
    DEFAULT CHARACTER SET = utf8
    COLLATE = utf8_bin;  ''')

for table_name in TABLES:
    table_sql = TABLES[table_name]
    try:
        print(f'Criando tabela... {table_name}')
        cursor.execute(table_sql)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print('table já existe!')
        else:
            print(err.msg)
    else:
        print('Criado!')

# endregion

# region Adding Users

user_sql = 'INSERT INTO users (name, nickname, password) values (%s, %s, %s)'

# Confer models/user.py
users = [
    ('isaachermel', 'lovelace', generate_password_hash('12345678').decode('utf-8')),
]

cursor.executemany(user_sql, users)

cursor.execute('select * from gameteca.users')

print('---------------- Usuários ----------------')
for user in cursor.fetchall():
    print(user[0])

# endregion

# region Adding Games

game_sql = 'INSERT INTO games (name, category, platform) values (%s, %s, %s)'

# Confer models/game.py
games = [
    ('Tetris', 'Puzzle', 'Atari'),
    ('Sonic Frontiers', 'Aventura', 'Diversos'),
    ('Devil May Cry 5', 'Hack n Slash', 'Diversos')
]

cursor.executemany(game_sql, games)

cursor.execute('select * from gameteca.games')
print('---------------- Jogos ----------------')
for game in cursor.fetchall():
    print(game[1])

# endregion

# Commit changes and close connections
connection.commit()

cursor.close()
connection.close()
