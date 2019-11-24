from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import home
from ..models import Events, Comments, University, Rso
from .forms import EventForm, CommentForm, RsoForm
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
                                description=form.description.data, date=form.date.data, time=form.time.data, location=form.location.data, event_type=form.event_type.data)
        event.univeristy = form.university.data

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

@home.route('/events/<int:id>/comments/', methods=['GET', 'POST'])
@login_required
def event_comments(id):
    """
    Delete a university from the database
    """

    comments = Comments.query.filter(Comments.event_id==id)

    # redirect to the universities page

    return render_template('home/events/comments.html',
                           comments=comments, event_id=id, title="Comments")

@home.route('/events/<int:eventid>/comments/add', methods=['GET', 'POST'])
@login_required
def add_comment(eventid):
    """
    Add a event to the database
    """

    add_comment = True

    form = CommentForm()
    if form.validate_on_submit():
        comment = Comments(comment=form.comment.data,
                                rating=form.rating.data, event_id=eventid)

        try:
            # add university to the database
            db.session.add(comment)
            db.session.commit()
            flash('You have successfully added a new comment.')
        except:
            # in case university name already exists
            flash('Error: comment name already exists.')

        # redirect to universities page
        return redirect(url_for('home.event_comments', id=eventid))

    # load university template
    return render_template('home/events/comment.html', action="Add",
                           add_comment=add_comment, form=form,
                           title="Add Comment")

@home.route('/events/<int:eventid>/comments/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_comment(id, eventid):
    """
    Edit a university
    """

    add_comment = False

    comment = Comments.query.get_or_404(id)
    form = CommentForm(obj=comment)
    if form.validate_on_submit():
        comment.comment = form.comment.data
        comment.rating = form.rating.data
        db.session.commit()
        flash('You have successfully edited the comment.')

        # redirect to the universities page
        return redirect(url_for('home.event_comments', id=eventid))

    form.rating.data = comment.rating
    form.comment.data = comment.comment
    return render_template('home/events/comment.html', action="Edit",
                           add_comment=add_comment, form=form,
                           comment=comment, title="Edit Comment")

@home.route('/events/<int:eventid>/comments/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_comment(id, eventid):
    """
    Delete a university from the database
    """

    comment = Comments.query.get_or_404(id)
    db.session.delete(comment)
    db.session.commit()
    flash('You have successfully deleted the comment.')

    # redirect to the universities page
    return redirect(url_for('home.event_comments', id=eventid))

    return render_template(title="Delete Comment")


@home.route('/rsos', methods=['GET', 'POST'])
@login_required
def list_rsos():
    """
    List all rsos
    """

    print("hi")

    rsos = Rso.query.all()

    return render_template('home/rsos/rsos.html',
                           rsos=rsos, title="Rsos")

@home.route('/rsos/add', methods=['GET', 'POST'])
@login_required
def add_rso():
    """
    Add a rso to the database
    """

    add_rso = True

    form = RsoForm()
    if form.validate_on_submit():
        uname = form.university.data
        uid = db.select([University.id]).where(University.name.in_([str(uname)]))
        rso = Rso(name=form.name.data,
                                description=form.description.data,university_id=uid)
        try:
            # add university to the database
            db.session.add(rso)
            db.session.commit()
            flash('You have successfully added a new rso.')
        except ValueError as e:
            print(e)
            # in case university name already exists
            flash('Error: rso name already exists.')

        # redirect to universities page
        return redirect(url_for('home.list_rsos'))

    # load university template
    return render_template('home/rsos/rso.html', action="Add",
                           add_rso=add_rso, form=form,
                           title="Add Rso")

@home.route('/rsos/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_rso(id):
    """
    Edit a university
    """

    add_rso = False

    rso = Rso.query.get_or_404(id)
    form = RsoForm(obj=rso)
    if form.validate_on_submit():
        rso.name = form.name.data
        rso.description = form.description.data
        db.session.commit()
        flash('You have successfully edited the rso.')

        # redirect to the universities page
        return redirect(url_for('home.list_rsos'))

    form.description.data = rso.description
    form.name.data = rso.name
    return render_template('home/rsos/rso.html', action="Edit",
                           add_rso=add_rso, form=form,
                           even=rso, title="Edit Rso")
                                                   
@home.route('/rsos/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_rso(id):
    """
    Delete a university from the database
    """

    rso = Rso.query.get_or_404(id)
    db.session.delete(rso)
    db.session.commit()
    flash('You have successfully deleted the rso.')

    # redirect to the universities page
    return redirect(url_for('home.list_rsos'))

    return render_template(title="Delete Rso")