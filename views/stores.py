from flask import Blueprint, render_template, request, redirect, url_for
from models.store import Store
from models.user.decorators import requires_admin
import json

store_blueprint = Blueprint("stores", __name__)


@store_blueprint.route("/")
def index():
    stores = Store.all()
    return render_template("/stores/index.html", stores=stores)


@store_blueprint.route("/new_store", methods=['GET', 'POST'])
@requires_admin
def new_store():

    if request.method == "POST":
        name = request.form["store_name"]
        tag_name = request.form["tag_name"]
        url_prefix = request.form["store_url"]
        query = json.loads(request.form["query"])
        Store(name, url_prefix, tag_name, query).save_to_database()

    return render_template("/stores/new_store.html")


@store_blueprint.route("/delete/<string:store_id>", methods=["GET", "POST"])
@requires_admin
def delete_store(store_id):
    store = Store.get_element_by_id(store_id)
    store.remove_from_database()

    return redirect(url_for(".index"))
