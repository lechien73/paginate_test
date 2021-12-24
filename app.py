import os
from flask import Flask, render_template, request
from flask_pymongo import PyMongo
import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)

@app.route("/")
def index():

    content = mongo.db.artists.find()

    page_num = int(request.args["page"]) if "page" in request.args else 1

    num_per_page = 5

    lists = list(content.clone())

    is_paginated = True if len(lists) > num_per_page else False

    if len(lists) % num_per_page == 0:
        num_pages = int(len(lists) / num_per_page)
    else:
        num_pages = int((len(lists) / num_per_page) + 1)

    if num_pages > page_num:
        page_num = 1

    start = (num_per_page * page_num) - num_per_page
    end = (num_per_page * page_num) - 1

    recordset = content[start:end]

    return render_template("index.html", is_paginated=is_paginated, active_page=page_num, data=recordset, num_pages=num_pages)

if __name__ == "__main__":
    app.run(host=os.getenv("IP", "0.0.0.0"), port=int(
        os.getenv("PORT", "5000")), debug=True)