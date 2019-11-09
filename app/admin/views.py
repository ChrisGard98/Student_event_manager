from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from .forms import UniversityForm, StudentAssignForm, RoleForm
from .. import db
from ..models import University, Student, Role


def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)


# University Views


@admin.route('/universities', methods=['GET', 'POST'])
@login_required
def list_universities():
    """
    List all universities
    """
    check_admin()

    

    universities = University.query.all()

    return render_template('admin/universities/universities.html',
                           universities=universities, title="Universities")


@admin.route('/universities/add', methods=['GET', 'POST'])
@login_required
def add_university():
    """
    Add a university to the database
    """
    check_admin()

    add_university = True

    form = UniversityForm()
    if form.validate_on_submit():
        university = University(name=form.name.data,
                                description=form.description.data)
        try:
            # add university to the database
            db.session.add(university)
            db.session.commit()
            flash('You have successfully added a new university.')
        except:
            # in case university name already exists
            flash('Error: university name already exists.')

        # redirect to universities page
        return redirect(url_for('admin.list_universities'))

    # load university template
    return render_template('admin/universities/university.html', action="Add",
                           add_university=add_university, form=form,
                           title="Add University")


@admin.route('/universities/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_university(id):
    """
    Edit a university
    """
    check_admin()

    add_university = False

    university = University.query.get_or_404(id)
    form = UniversityForm(obj=university)
    if form.validate_on_submit():
        university.name = form.name.data
        university.description = form.description.data
        db.session.commit()
        flash('You have successfully edited the university.')

        # redirect to the universities page
        return redirect(url_for('admin.list_universities'))

    form.description.data = university.description
    form.name.data = university.name
    return render_template('admin/universities/university.html', action="Edit",
                           add_university=add_university, form=form,
                           university=university, title="Edit University")


@admin.route('/universities/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_university(id):
    """
    Delete a university from the database
    """
    check_admin()

    university = University.query.get_or_404(id)
    db.session.delete(university)
    db.session.commit()
    flash('You have successfully deleted the university.')

    # redirect to the universities page
    return redirect(url_for('admin.list_universities'))

    return render_template(title="Delete University")

@admin.route('/roles')
@login_required
def list_roles():
    check_admin()
    """
    List all roles
    """
    roles = Role.query.all()
    return render_template('admin/roles/roles.html',
                           roles=roles, title='Roles')


@admin.route('/roles/add', methods=['GET', 'POST'])
@login_required
def add_role():
    """
    Add a role to the database
    """
    check_admin()

    add_role = True

    form = RoleForm()
    if form.validate_on_submit():
        role = Role(name=form.name.data,
                    description=form.description.data)

        try:
            # add role to the database
            db.session.add(role)
            db.session.commit()
            flash('You have successfully added a new role.')
        except:
            # in case role name already exists
            flash('Error: role name already exists.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    # load role template
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title='Add Role')


@admin.route('/roles/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_role(id):
    """
    Edit a role
    """
    check_admin()

    add_role = False

    role = Role.query.get_or_404(id)
    form = RoleForm(obj=role)
    if form.validate_on_submit():
        role.name = form.name.data
        role.description = form.description.data
        db.session.add(role)
        db.session.commit()
        flash('You have successfully edited the role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    form.description.data = role.description
    form.name.data = role.name
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title="Edit Role")


@admin.route('/roles/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_role(id):
    """
    Delete a role from the database
    """
    check_admin()

    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    flash('You have successfully deleted the role.')

    # redirect to the roles page
    return redirect(url_for('admin.list_roles'))

    return render_template(title="Delete Role")


@admin.route('/students')
@login_required
def list_students():
    """
    List all students
    """
    check_admin()

    students = Student.query.all()
    return render_template('admin/students/students.html',
                           students=students, title='Students')


@admin.route('/students/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_student(id):
    """
    Assign a university and a role to an student
    """
    check_admin()

    student = Student.query.get_or_404(id)

    # prevent admin from being assigned a university or role
    if student.is_admin:
        abort(403)

    form = StudentAssignForm(obj=student)
    if form.validate_on_submit():
        student.university = form.university.data
        student.role = form.role.data
        db.session.add(student)
        db.session.commit()
        flash('You have successfully assigned a university and role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_students'))

    return render_template('admin/students/student.html',
                           student=student, form=form,
                           title='Assign Student')