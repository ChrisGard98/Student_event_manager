from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField, SelectField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields.html5 import DateField
from wtforms_components import TimeField


from ..models import Events, Rso, University


class EventForm(FlaskForm):
    """
    Form for admin to add or edit a university
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()], format='%Y-%m-%d')
    time = TimeField('Time(H:M)', validators=[DataRequired()], format='%H:%M')
    location = StringField('Location', validators=[DataRequired()])
    event_type = SelectField(u'Type', choices=[('Public', 'Public'), ('Private', 'Private'), ('RSO', 'RSO') ])
    university = QuerySelectField(query_factory=lambda: University.query.all(),
                                  get_label="name")
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    """
    Form for admin to add or edit a university
    """
    comment = StringField('Comment', validators=[DataRequired()])
    rating = StringField('Rating', validators=[DataRequired()])
    #date = DateField('Date', validators=[DataRequired()], format='%Y-%m-%d')
    #time = DateTimeField('Time(H:M)', validators=[DataRequired()], format='%H:%M')
    #location = StringField('Location', validators=[DataRequired()])
    submit = SubmitField('Submit')

class RsoForm(FlaskForm):
    """
    Form for admin to add or edit a university
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    university = QuerySelectField(query_factory=lambda: University.query.all(),
                                  get_label="name")
    submit = SubmitField('Submit')


class StudentAssignForm(FlaskForm):
    """
    Form for admin to assign universities and roles to students
    """
    university = QuerySelectField(query_factory=lambda: University.query.all(),
                                  get_label="name")
    role = QuerySelectField(query_factory=lambda: Role.query.all(),
                            get_label="name")
    submit = SubmitField('Submit')