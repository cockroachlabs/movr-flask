from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, HiddenField
from wtforms.validators import data_required


class CredentialForm(FlaskForm):
    username = StringField('Username: ', validators=[data_required()])
    password = PasswordField('Password: ', validators=[data_required()])
    submit = SubmitField('Sign In')


class StartRideForm(FlaskForm):
    submit = SubmitField('Start ride')


class EndRideForm(FlaskForm):
    location = StringField(label='Where are you leaving the vehicle?', validators=[data_required()])
    submit = SubmitField('End ride')


class VehicleForm(FlaskForm):
    type = SelectField(label='Type', choices=[('bike', 'Bike'), ('scooter', 'Scooter'), ('skateboard', 'Skateboard')])
    color = StringField(label='Color', validators=[data_required()])
    brand = StringField(label='Brand')
    location = StringField(label='Current location: ', validators=[data_required()])
    submit = SubmitField('Add vehicle')


class RemoveVehicleForm(FlaskForm):
    submit = SubmitField('Remove vehicle')


class RegisterForm(FlaskForm):
    city = SelectField('City: ',  choices=[('new york', 'New York'), ('boston', 'Boston'), ('washington dc', 'Washington DC'),
                ('san francisco', 'San Francisco'), ('seattle', 'Seattle'), ('los angeles', 'Los Angeles'),
                ('chicago', 'Chicago'), ('detroit', 'Detroit'), ('minneapolis', 'Minneapolis'),
                ('amsterdam', 'Amsterdam'), ('paris', 'Paris'), ('rome', 'Rome')])
    first_name = StringField('First name: ', validators=[data_required()])
    last_name = StringField('Last name: ', validators=[data_required()])
    email = StringField('Email', validators=[data_required()])
    username = StringField('Username: ', validators=[data_required()])
    password = PasswordField('Password: ', validators=[data_required()])
    submit = SubmitField('Register')


class RemoveUserForm(FlaskForm):
    submit = SubmitField('Delete my account')
    
    