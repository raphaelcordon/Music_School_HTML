from flask import Blueprint, render_template, redirect, url_for
from views.login import logout

ind = Blueprint('ind', __name__)


@ind.route('/')
def index():
    return render_template('index.html')


@ind.route('/music_school')
def music_school():
    logout()
    return redirect(url_for('ind.home'))


@ind.route('/home/')
def home():
    return render_template('music_school.html')

@ind.route('/about/')
def about():
    return render_template('about.html')
