from flask import Blueprint, render_template, flash, session

cla = Blueprint('cla', __name__)


# <--- Classes routes beginning --->
@cla.route('/classes')
def classes():
    if session['username'] == '' or 'username' not in session:
        flash('You must be logged for navigation', 'danger')
        return render_template('index.html')
    else:
        return render_template('classes.html', title='Classes')
