from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import data_required


# START CredentialForm
class CredentialForm(FlaskForm):
    """Login form class.
    """
    username = StringField('Username: ', validators=[data_required()])
    password = PasswordField('Password: ', validators=[data_required()])
    submit = SubmitField('Sign In')
# END CredentialForm


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


# START VehicleForm
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
# END VehicleForm


class RemoveVehicleForm(FlaskForm):
    """Remove vehicle form class.
    """
    submit = SubmitField('Remove vehicle')


class RegisterForm(FlaskForm):
    """User registration form class.
    """
    city = SelectField('City: ',
                       choices=[('new york', 'New York'), ('boston', 'Boston'),
                                ('washington dc', 'Washington DC'),
                                ('san francisco', 'San Francisco'),
                                ('seattle', 'Seattle'),
                                ('los angeles', 'Los Angeles'),
                                ('chicago', 'Chicago'), ('detroit', 'Detroit'),
                                ('minneapolis', 'Minneapolis'),
                                ('amsterdam', 'Amsterdam'), ('paris', 'Paris'),
                                ('rome', 'Rome')])
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
