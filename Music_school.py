from db import CourseDB, UsersDB, DeletingDB, FindId, Authenticate, EnrollmentDB
from flask import Flask, render_template, redirect, request, url_for, flash, session
from models import Course, Users, Edit_Users_Access_Level, Edit_Users_Pass, Enrollment, ACCESS_LEVEL
from passlib.hash import sha256_crypt


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/')
def index():
    logout()
    return redirect('home')

@app.route('/home/')
def home():
    return render_template('index.html')


# <--- Course routes beginning --->
@app.route('/course')
def course():
    if session['username'] == '' or 'username' not in session:
        flash('You must be logged for navigation')
        return render_template('index.html')
    else:
        course_list = CourseDB.course_list()
        return render_template('course.html', title='Course List', course=course_list)


@app.route('/CourseRegistry', methods=['POST',])
def course_registry():
    name = str(request.form['name']).strip().title()
    if name == '':
        flash('Blank field not accepted')
    elif CourseDB.course_new(name):
        flash('Already registered, please check below')
    else:
        flash('Successfully created')
    return redirect(url_for('course'))


@app.route('/CourseEdit/<category>/<int:id>')
def course_edit(category, id):
    data = CourseDB.course_find_id(category, id)
    return render_template('edit_course.html', data=data, category=category)


@app.route('/CourseUpdate', methods=['POST',])
def course_update():
    id = request.form['id']
    name = str(request.form['name']).strip().title()
    course = Course(id, name)
    if name == '':
        flash('Blank field not accepted')
    elif CourseDB.course_update(course.id, course.name):
        flash('Already registered, please check below')
    else:
        flash('Successfully updated')
    return redirect(url_for('course'))

# <--- Course routes ending --->


# <--- Users routes beginning --->

@app.route('/users')
def users():
    if session['username'] == '' or 'username' not in session:
        flash('You must be logged for navigation')
        return render_template('index.html')
    else:
        users_list = UsersDB.users_list()
        return render_template('users.html', title='Users List', users=users_list, ACCESS_LEVEL=ACCESS_LEVEL)


@app.route('/UsersRegistry', methods=['POST',])
def users_registry():
    username = str(request.form['username']).strip().lower()
    name = str(request.form['name']).strip().title()
    password = 'pass'  # First login will force to change
    course = 0
    access_level = request.form['access_level']

    if username == '' or name == '' or access_level == '':
        flash('Blank field not accepted')
    elif UsersDB.users_new(username, name, password, course, access_level):
        flash('Already registered, please check below')
    else:
        flash("Successfully created. User the password 'pass' to login for the first time.")
    return redirect(url_for('users'))


@app.route('/UsersEdit/<category>/<int:id>')
def users_edit(category, id):
    data = UsersDB.users_find_id(id)
    return render_template('edit_users.html', data=data, category=category, ACCESS_LEVEL=ACCESS_LEVEL)


@app.route('/UsersUpdate', methods=['POST',])
def users_update():
    id = request.form['id']
    username = str(request.form['username']).strip().lower()
    name = str(request.form['name']).strip().title()
    access_level = request.form['access_level']
    users = Edit_Users_Access_Level(id, username, name, access_level)
    if username == '' or name == '':
        flash('Blank field not accepted')
    elif UsersDB.users_update(users.id, users.username, users.name, users.access_level):
        flash('Already registered, please check below')
    else:
        flash('Successfully updated')
    return redirect(url_for('users'))


@app.route('/usercourse/<int:id>')
def usercourse(id):
    course_list = CourseDB.course_list()
    data = UsersDB.users_find_id(id)
    enrolled = EnrollmentDB.enrolled_find_user_id(id)
    enrolled_list = []
    if enrolled is not None:
        for c in enrolled:
            enrolled_list.append(c.course_id)

    return render_template('usercourse.html', course_list=course_list, data=data, enrolled=enrolled_list)


@app.route('/update_enrolled_courses', methods=['POST',])
def update_enrolled_courses():
    EnrollmentDB.enroled_deleting_by_id(request.form['id'])
    for list in request.form:
        if list != 'id':
            course = request.form[list]
            EnrollmentDB.insert_enrolled_courses(request.form['id'], course)

    return redirect(url_for('users'))

# <--- Users routes ending --->


# <--- Classes routes beginning --->
@app.route('/classes')
def classes():
    if session['username'] == '' or 'username' not in session:
        flash('You must be logged for navigation')
        return render_template('index.html')
    else:
        return render_template('classes.html', title='Classes')

@app.route('/Delete/<int:id>/<category>')
def Delete(category, id):
    DeletingDB(category, id)
    flash('Successfully removed')
    return redirect(url_for(f'{category}'))


@app.route('/authenticate', methods=['POST',])
def authenticate():
    user = Authenticate.authenticate(request.form['username'])
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
            return redirect(url_for('change_pass'))
        else:
            flash(f'Welcome {user.name}')
            return redirect(url_for('home'))
    else:
        flash('Login failed, please try again')
        return redirect(url_for('home'))


@app.route('/logout')
def logout():
    session['id'] = ''
    session['username'] = ''
    session['name'] = ''
    session['access_level'] = ''
    return redirect(url_for('home'))


@app.route('/change_pass')
def change_pass():
    id = session['id']
    return render_template('change_pass.html', data=id)


@app.route('/update_pass_db', methods=['POST',])
def update_pass_db():
    id = session['id']
    password = sha256_crypt.encrypt(str(request.form['password']))
    new_pass = Edit_Users_Pass(id, password)
    UsersDB.users_password_update(new_pass.id, new_pass.password)
    print(new_pass.id, new_pass.password)
    flash('Password successfully updated')
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
