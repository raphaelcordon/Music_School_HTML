from repository.users import UsersRepository
from repository.enrollment import EnrollmentRepository
from repository.course import CourseRepository
from flask import Blueprint, render_template, redirect, request, url_for, flash, session
from models.users import Edit_Users_Access_Level
from models.common import ACCESS_LEVEL


use = Blueprint('use', __name__)


# <--- Users routes beginning --->

@use.route('/users')
def users():
    if session['username'] == '' or 'username' not in session:
        flash('You must be logged for navigation', 'danger')
        return render_template('music_school.html')
    else:
        users_list = UsersRepository().List()
        return render_template('users.html', users=users_list, ACCESS_LEVEL=ACCESS_LEVEL)


@use.route('/UsersRegistry', methods=['POST', 'GET'])
def usersRegistry():
    username = str(request.form['username']).strip().lower()
    name = str(request.form['name']).strip().title()
    access_level = request.form['access_level']

    if username == '' or name == '' or access_level == '':
        flash('Blank field not accepted')
    else:
        if UsersRepository().checkDuplication(username):
            flash('Username already in use, please check below', 'warning')
        else:
            UsersRepository().New(username, name, access_level)
            flash("Successfully created. Use the password -->' pass '<-- to login for the first time.", 'info')
    return redirect(url_for('use.users'))


@use.route('/usersEdit/<int:id>')
def usersEdit(id):
    data = UsersRepository().FindId(id)
    return render_template('usersEdit.html', data=data, ACCESS_LEVEL=ACCESS_LEVEL)


@use.route('/UsersUpdate', methods=['POST',])
def users_update():
    id = request.form['id']
    username = str(request.form['username']).strip().lower()
    name = str(request.form['name']).strip().title()
    access_level = request.form['access_level']
    users = Edit_Users_Access_Level(id, username, name, access_level)
    if username == '' or name == '':
        flash('Blank field not accepted', 'warning')
    elif UsersRepository().Update(id, username, name, access_level):
        flash('Already registered, please check below', 'warning')
    else:
        flash('Successfully updated', 'success')
    return redirect(url_for('use.users'))


@use.route('/Delete/<int:id>', methods=['GET', 'POST'])
def Delete(id):
    UsersRepository().Delete(id)
    if not UsersRepository().FindId(id):
        flash('Successfully Deleted', 'success')
    else:
        flash('Something went wrong', 'danger')
    return redirect(url_for('use.users'))


@use.route('/usersCourse/<int:id>')
def usersCourse(id):
    course_list = CourseRepository().List()
    data = UsersRepository().FindId(id)
    enrolled = EnrollmentRepository().FindUserId(id)
    enrolled_list = []
    if enrolled is not None:
        for item in enrolled:
            enrolled_list.append(item.course_id)
    return render_template('usersCourse.html', course_list=course_list, data=data, enrolled=enrolled_list)


@use.route('/update_enrolled_courses', methods=['POST', 'GET'])
def update_enrolled_courses():
    EnrollmentRepository().DeleteById(request.form['id'])
    for list in request.form:
        if list != 'id':
            course = request.form[list]
            EnrollmentRepository().New(request.form['id'], course)
    flash(f"Enrollment list updated", 'success')
    return redirect(url_for('use.users'))
