# Copyright 2020 Google Inc.	
#	
# Licensed under the Apache License, Version 2.0 (the "License");	
# you may not use this file except in compliance with the License.	
# You may obtain a copy of the License at	
#	
#     http://www.apache.org/licenses/LICENSE-2.0	
#	
# Unless required by applicable law or agreed to in writing, software	
# distributed under the License is distributed on an "AS IS" BASIS,	
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.	
# See the License for the specific language governing permissions and	
# limitations under the License.

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin,login_user,login_required, logout_user, current_user
from sqlalchemy.dialects import mysql

db = SQLAlchemy()

def init_app(app):
    # Disable track modifications, as it unnecessarily uses memory.
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    db.init_app(app)


users_pokemons = db.Table('users_pokemons',
    db.Column('user_id', mysql.INTEGER(6, zerofill=True), db.ForeignKey('users.id')),
    db.Column('pokemon_id', mysql.INTEGER(3, zerofill=True), db.ForeignKey('pokemons.id')),
    db.UniqueConstraint('user_id', 'pokemon_id', name='uix_1')
)

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(mysql.INTEGER(6, zerofill=True), primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    caught_pokemon = db.relationship('Pokemon', secondary=users_pokemons,backref=db.backref('trainers', lazy='dynamic'))


class Pokemon(db.Model):
    __tablename__ = 'pokemons'

    id = db.Column(mysql.INTEGER(3, zerofill=True), primary_key=True)
    name = db.Column(db.String(35), unique=True)
    imageUrl = db.Column(db.String(120))
    type1 = db.Column(db.String(15))
    type2 = db.Column(db.String(15))

    def __repr__(self):
        return "<Pokemon(id='%s', name=%s)" % (self.id, self.name)



def _create_database():
    """
    If this script is run directly, create all the tables necessary to run the
    application.
    """
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')
    init_app(app)
    with app.app_context():
        db.create_all()
    print("All tables created")


if __name__ == '__main__':
    _create_database()
