from flask import Blueprint, redirect, url_for,render_template
lab8 = Blueprint('lab8', __name__)


@lab8.route("/lab8")
def lab():
    return render_template('lab8/lab8.html')