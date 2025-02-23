from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
import sys
import math

from werkzeug.utils import secure_filename
import os
from flask import get_flashed_messages
from database import DBhandler
import hashlib
import sys

application = Flask(__name__)
application.config["SECRET_KEY"] = "shortWiki"
DB=DBhandler()

application.config['TEMPLATES_AUTO_RELOAD'] = True

@application.route("/", methods=["GET", "POST"])
def hello():
    return render_template("index.html")