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

from pokeview import models
from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import LoginManager, UserMixin,login_user,login_required, logout_user, current_user
from flask import flash


bp = Blueprint('pokedex', __name__)

@bp.route("/")
@login_required
def list_pokemon():
    POKEMON_COUNT = 151

    pokedex = models.db.session.query(models.Pokemon).order_by(models.Pokemon.id).all()

    catch_list = [False] * POKEMON_COUNT
    user = models.User.query.filter_by(username=current_user.username).first()

    # Query for all the pokemon of current user
    caught_pokemon = models.db.session.query(models.users_pokemons).filter(models.User.id == models.users_pokemons.c.user_id, models.User.username == user.username).all()

    for pokemon in caught_pokemon:
       catch_list[pokemon.pokemon_id - 1] = True

    return render_template(
        "list_pokemon.html",
        pokedex=pokedex,
        catch_list=catch_list,
        name=current_user.username,
        )


@bp.route('/<id>')
def view(id):
    pokemon = models.db.session.query(models.Pokemon).get(id)
    return render_template("view.html", pokemon=pokemon)


@bp.route('/add/<string:username>/<int:pokemon_id>', methods=["POST"])
def add(username, pokemon_id):
    user = models.User.query.filter_by(username=username).first()
    pokemon = models.Pokemon.query.filter_by(id=pokemon_id).first()
    pokemon.trainers.append(user)
    models.db.session.commit()
    return redirect(url_for('pokedex.list_pokemon'))


@bp.route('/delete/<string:username>/<int:pokemon_id>', methods=["POST"])
def delete(username, pokemon_id):
    user = models.User.query.filter_by(username=username).first()
    pokemon = models.Pokemon.query.filter_by(id=pokemon_id).first()
    pokemon.trainers.remove(user)
    models.db.session.commit()
    return redirect(url_for('pokedex.list_pokemon'))
