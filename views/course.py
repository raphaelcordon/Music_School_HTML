from repository.course import CourseRepository
from flask import Blueprint, render_template, redirect, request, url_for, flash, session

cou = Blueprint('cou', __name__)


# <--- Course routes beginning --->
@cou.route('/course')
def course():
    if session['username'] == '' or 'username' not in session:
        flash('You must be logged for navigation', 'danger')
        return render_template('music_school.html')
    else:
        course_list = CourseRepository().List()
        return render_template('course.html', title='Course List', courses=course_list)


@cou.route('/CourseRegistry', methods=['GET', 'POST'])
def course_registry():
    name = str(request.form['name']).strip().title()

    if name == '':
        flash('Blank field not accepted', 'warning')
    elif CourseRepository().checkDuplication(name):
        flash('Already registered, please check below', 'warning')
    else:
        CourseRepository().New(name)
        if CourseRepository().checkDuplication(name):
            flash('Successfully created', 'success')
        else:
            flash('Something wrong, check logs', 'danger')

    return redirect(url_for('cou.course'))


@cou.route('/courseEdit/<int:id>', methods=['GET', 'POST'])
def courseEdit(id):
    data = CourseRepository().FindId(id)

    return render_template('courseEdit.html', data=data)


@cou.route('/CourseUpdate', methods=['GET', 'POST'])
def courseUpdate():
    id = request.form['id']
    name = str(request.form['name']).strip().title()
    if name == '':
        flash('Blank field not accepted', 'warning')
    elif CourseRepository().ListPerName(name):
        flash('Already registered, please check below', 'warning')
    else:
        CourseRepository().Update(id, name)
        if CourseRepository().FindId(id).name == name:
            flash('Successfully updated')
        else:
            flash('Not updated, please check for eventual duplications', 'danger')

    return redirect(url_for('cou.course'))


@cou.route('/CourseDelete/<int:id>', methods=['GET', 'POST'])
def CourseDelete(id):
    CourseRepository().Delete(id)
    if not CourseRepository().FindId(id):
        flash('Successfully Deleted', 'success')
    else:
        flash('Something went wrong', 'danger')
    return redirect(url_for('cou.course'))
