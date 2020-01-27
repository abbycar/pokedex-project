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

import logging

from flask import current_app, Flask, redirect, url_for, render_template
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField,PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin,login_user,login_required, logout_user, current_user
from pokeview import models, forms

login_manager = LoginManager()


def create_app(config, debug=False, testing=False, config_overrides=None):
    app = Flask(__name__)
    app.config.from_object(config)
    Bootstrap(app)
    app.debug = debug
    app.testing = testing



    if config_overrides:
        app.config.update(config_overrides)

    # Configure logging
    if not app.testing:
        logging.basicConfig(level=logging.INFO)

    # Setup the data model.
    with app.app_context():
        # Disable track modifications, as it unnecessarily uses memory.
        app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
        models.db.init_app(app)
        login_manager.init_app(app)
        login_manager.login_view = 'account.signin'
        
        @login_manager.user_loader
        def load_user(user_id):
            return models.User.query.get(int(user_id))

    # Register the pokeview blueprints.
    from pokeview.views import account
    from pokeview.views import pokedex
    app.register_blueprint(pokedex.bp, url_prefix='/pokedex')
    app.register_blueprint(account.bp, url_prefix='/account')


    # Add a default root route.
    @app.route("/")
    def index():
        return render_template("home.html", nav=False, user=current_user)


    # Add an error handler. This is useful for debugging the live application,
    # however, you should disable the output of the exception for production
    # applications.
    # @app.errorhandler(500)
    # def server_error(e):
    #     return """
    #     An internal error occurred: <pre>{}</pre>
    #     See logs for full stacktrace.
    #     """.format(e), 500

    return app


