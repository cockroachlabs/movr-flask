from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import data_required


class CredentialForm(FlaskForm):
    """Login form class.
    """
    username = StringField('Username: ', validators=[data_required()])
    password = PasswordField('Password: ', validators=[data_required()])
    submit = SubmitField('Sign In')


class StartRideForm(FlaskForm):
    """Start ride form class.
    """
    submit = SubmitField('Start ride')


class EndRideForm(FlaskForm):
    """End ride form class.
    """
    location = StringField(label='Where are you leaving the vehicle?',
                           validators=[data_required()])
    submit = SubmitField('End ride')


class VehicleForm(FlaskForm):
    """Vehicle registration form class.
    """
    type = SelectField(label='Type',
                       choices=[('bike', 'Bike'), ('scooter', 'Scooter'),
                                ('skateboard', 'Skateboard')])
    color = StringField(label='Color', validators=[data_required()])
    brand = StringField(label='Brand')
    location = StringField(label='Current location: ',
                           validators=[data_required()])
    submit = SubmitField('Add vehicle')


class RemoveVehicleForm(FlaskForm):
    """Remove vehicle form class.
    """
    submit = SubmitField('Remove vehicle')


class RegisterForm(FlaskForm):
    """User registration form class.
    """
    city = StringField('City: ', validators=[data_required()])
    first_name = StringField('First name: ', validators=[data_required()])
    last_name = StringField('Last name: ', validators=[data_required()])
    email = StringField('Email', validators=[data_required()])
    username = StringField('Username: ', validators=[data_required()])
    password = PasswordField('Password: ', validators=[data_required()])
    submit = SubmitField('Register')


class RemoveUserForm(FlaskForm):
    """Remove user form class.
    """
    submit = SubmitField('Delete my account')
