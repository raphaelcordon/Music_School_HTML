from repository.athenticate import AuthenticateRepository
from repository.users import UsersRepository
from flask import Blueprint, render_template, redirect, request, url_for, flash, session
from passlib.hash import sha256_crypt

log = Blueprint('log', __name__)


@log.route('/login/')
def login():
    return render_template('login.html')


@log.route('/authenticate', methods=['POST', 'GET'])
def authenticate():
    user = AuthenticateRepository().auth(request.form['username'])
    print(user)
    try:
        check_pass = sha256_crypt.verify(request.form['pass'], user.password)
    except:
        check_pass = request.form['pass'], user.password

    if check_pass:
        session['id'] = user.id
        session['username'] = user.username
        session['name'] = user.name
        session['password'] = user.password
        session['access_level'] = user.access_level

        if user.password == 'pass':
            return redirect(url_for('log.change_pass'))
        else:
            flash(f'Welcome {user.name}', 'success')
            return redirect(url_for('ind.home'))
    else:
        flash('Login failed, please try again', 'danger')
        return redirect(url_for('log.login'))


@log.route('/logout')
def logout():
    session['id'] = ''
    session['username'] = ''
    session['name'] = ''
    session['access_level'] = ''
    return redirect(url_for('ind.home'))


@log.route('/change_pass')
def change_pass():
    id = session['id']
    return render_template('change_pass.html', data=id)


@log.route('/update_pass_db', methods=['POST',])
def update_pass_db():
    id = session['id']
    password = sha256_crypt.encrypt(str(request.form['password']))
    UsersRepository().PasswordUpdate(id, password)
    flash('Password successfully updated', 'success')
    return redirect(url_for('ind.home'))