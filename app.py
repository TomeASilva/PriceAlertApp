import os
import json
from flask import Flask, render_template, request, current_app
from models.item import Item
from views.stores import store_blueprint
from views.alerts import alerts_blueprint
from views.user import user_blueprint
from libs.mailgun import Mailgun
from dotenv import load_dotenv


app = Flask(__name__)
app.secret_key = "asdf1234"
app.config.update(
    ADMIN=os.environ.get('ADMIN')
)


@app.route('/')
def home_page():
    return render_template("home.html")


app.register_blueprint(store_blueprint, url_prefix="/stores")
app.register_blueprint(alerts_blueprint, url_prefix="/alerts")
app.register_blueprint(user_blueprint, url_prefix="/users")

if __name__ == "__main__":
    app.run(debug=True)
