#!/bin/python3
import flask, flask_login
import random, string
from datetime import datetime
from base import app,load_info,ajax,DBDict

# -- Info for every Hack-A-Day project --
load_info({
    "project_name": "Hack-A-Link",
    "source_url": "https://github.com/za3k/day02_link",
    "subdir": "/hackaday/link"
})

# -- Routes specific to this Hack-A-Day project --
links = DBDict("link")
def random_id():
    LETTERS=string.ascii_letters + string.digits
    return "".join(random.choice(LETTERS) for letter in range(10))

@app.route("/")
def index():
    return flask.render_template('index.html')

@app.route("/create", methods=["POST"])
def create():
    url = flask.request.form.get('url', '')
    if url == '':
        return flask.redirect(flask.url_for("index"))
    if "://" not in url:
        url = "http://" + url
    key = random_id()
    links[key] = url
    return flask.redirect(flask.url_for("view", link_id=key))

@app.route("/view/<link_id>")
def view(link_id):
    return flask.render_template('view.html', link_id=link_id, url=links[link_id])

@app.route("/<link_id>")
def visit(link_id):
    if link_id not in links:
        return "Bad link", 404
    return flask.redirect(links[link_id])
