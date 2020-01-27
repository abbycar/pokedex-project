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

from pokeview import models, forms
from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import LoginManager, UserMixin,login_user,login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask import flash

bp = Blueprint('account', __name__)


# Add a sign in page
@bp.route("/signin", methods=['GET', 'POST'])
def signin():
    form = forms.SigninForm()

    if form.validate_on_submit():
        user = models.User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash('Sign in successful.')
                return redirect(url_for('pokedex.list_pokemon'))
        flash('Invalid username or password')

    return render_template("signin.html", form=form, nav=False)


# Add a user signup page
@bp.route("/signup", methods=['GET', 'POST'])
def signup():
    form = forms.SignupForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = models.User(username = form.username.data, email = form.email.data, password = hashed_password)
        models.db.session.add(new_user)
        models.db.session.commit()
        flash('Account created! Please sign in.')
        return redirect(url_for('account.signin'))
    return render_template("signup.html", form=form, nav=False)

# Add a user signup page
@bp.route("/signout")
@login_required
def signout():
    logout_user()
    flash('You\'re signed out.')
    return redirect(url_for('index'))