import json

from flask import Blueprint, render_template, request, redirect, url_for, session
from models.alert import Alert
from models.store import Store
from models.item import Item
from models.user import requires_login



alerts_blueprint = Blueprint("alerts", __name__)


@alerts_blueprint.route("/")
@requires_login
def index():
    alerts = Alert.find_many_by('user_email', session['email'])
    return render_template("alerts/index.html", alerts=alerts)


@alerts_blueprint.route("/new", methods=["GET", "POST"])
@requires_login
def new_alert():
    if request.method == 'POST':
        alert_name = request.form["alert_name"]
        item_url = request.form['item_url']
        price_limit = request.form["price_limit"]

        store = Store.get_by_url(item_url)  # What if this store is not database
        item = Item(item_url, store.tag_name, store.query)
        item.load_price()
        item.save_to_database()
        alert = Alert(alert_name, item._id, float(price_limit), session["email"])
        alert.save_to_database()

    return render_template("alerts/new_alert.html")


@alerts_blueprint.route("/edit/<string:alert_id>", methods=['GET', 'POST'])
@requires_login
def edit_alert(alert_id):
    alert = Alert.get_element_by_id(alert_id)

    if request.method == "POST":
        price_limit = float(request.form['price_limit'])
        alert.price_limit = price_limit
        alert.save_to_database()

        return redirect(url_for('.index'))  # this changes to the index endpoint defined within this blueprint the dot means within the current blueprint

    return render_template('alerts/edit_alert.html', alert=alert)


@alerts_blueprint.route("/delete/<string:alert_id>", methods=['GET', 'POST'])
@requires_login
def delete_alert(alert_id):
    alert = Alert.get_element_by_id(alert_id)
    if alert.user_email == session['email']:
        alert.remove_from_database()

    return redirect(url_for(".index"))
