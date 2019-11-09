from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import home
from ..models import Events
from .forms import EventForm
from .. import db


@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    return render_template('home/index.html', title="Welcome")


@home.route('/dashboard')
@login_required
def dashboard():
    """
    Render the dashboard template on the /dashboard route
    """
    print("hi")


    return render_template('home/dashboard.html', title="Dashboard")

# add admin dashboard view
@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # prevent non-admins from accessing the page
    if not current_user.is_admin:
        abort(403)

    return render_template('home/admin_dashboard.html', title="Dashboard")


@home.route('/events', methods=['GET', 'POST'])
@login_required
def list_events():
    """
    List all events
    """

    print("hi")

    events = Events.query.all()

    return render_template('home/events/events.html',
                           events=events, title="Events")

@home.route('/events/add', methods=['GET', 'POST'])
@login_required
def add_event():
    """
    Add a event to the database
    """

    add_event = True

    form = EventForm()
    if form.validate_on_submit():
        event = Events(name=form.name.data,
                                description=form.description.data, date=form.date.data, time=form.time.data, location=form.location.data)
        try:
            # add university to the database
            db.session.add(event)
            db.session.commit()
            flash('You have successfully added a new event.')
        except:
            # in case university name already exists
            flash('Error: event name already exists.')

        # redirect to universities page
        return redirect(url_for('home.list_events'))

    # load university template
    return render_template('home/events/event.html', action="Add",
                           add_event=add_event, form=form,
                           title="Add Event")

@home.route('/events/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_event(id):
    """
    Edit a university
    """

    add_event = False

    event = Events.query.get_or_404(id)
    form = EventForm(obj=event)
    if form.validate_on_submit():
        event.name = form.name.data
        event.description = form.description.data
        db.session.commit()
        flash('You have successfully edited the event.')

        # redirect to the universities page
        return redirect(url_for('home.list_events'))

    form.description.data = event.description
    form.name.data = event.name
    return render_template('home/events/event.html', action="Edit",
                           add_event=add_event, form=form,
                           even=event, title="Edit Event")


@home.route('/events/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_event(id):
    """
    Delete a university from the database
    """

    event = Events.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()
    flash('You have successfully deleted the event.')

    # redirect to the universities page
    return redirect(url_for('home.list_events'))

    return render_template(title="Delete Event")