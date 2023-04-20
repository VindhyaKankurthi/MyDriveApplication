from flask import Blueprint, render_template

myViews = Blueprint('myViews', __name__)
auth = Blueprint('auth', __name__)

#defining routes for home page
@myViews.route('/')
def home():
    return render_template("homePage.html")




