from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields.html5 import DateField


from ..models import Events


class EventForm(FlaskForm):
    """
    Form for admin to add or edit a university
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()], format='%Y-%m-%d')
    time = DateTimeField('Time(H:M)', validators=[DataRequired()], format='%H:%M')
    location = StringField('Location', validators=[DataRequired()])
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


class StudentAssignForm(FlaskForm):
    """
    Form for admin to assign universities and roles to students
    """
    university = QuerySelectField(query_factory=lambda: University.query.all(),
                                  get_label="name")
    role = QuerySelectField(query_factory=lambda: Role.query.all(),
                            get_label="name")
    submit = SubmitField('Submit')