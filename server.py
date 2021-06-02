# This file contains the main web application server
# START front
from flask import Flask, render_template, session, redirect, flash, url_for, Markup, request, Response
from flask_bootstrap import Bootstrap, WebCDN
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from movr.movr import MovR
from web.forms import CredentialForm, RegisterForm, VehicleForm, StartRideForm, EndRideForm, RemoveUserForm, RemoveVehicleForm
from web.config import Config
from sqlalchemy.exc import DBAPIError
# END front

# START init
DEFAULT_ROUTE_AUTHENTICATED = "vehicles"
DEFAULT_ROUTE_NOT_AUTHENTICATED = "login_page"

# Initialize the app
app = Flask(__name__)
app.config.from_object(Config)
Bootstrap(app)
login = LoginManager(app)
protocol = ('https', 'http')[app.config.get('DEBUG') == 'True']
# END init

# Initialize the db connection
# START connect
conn_string = app.config.get('DB_URI')
movr = MovR(conn_string)
# END connect

region = app.config.get('REGION')
cities = app.config.get('CITY_MAP')[region]

# Update Bootstrap from v3.3.7 to v4.5
app.extensions['bootstrap']['cdns']['bootstrap'] = WebCDN(
    '//getbootstrap.com/docs/4.5/dist/'
)

# Define user_loader function for LoginManager
# START user_loader
@login.user_loader
def load_user(user_id):
    return movr.get_user(user_id=user_id)
# END user_loader


# ROUTES

# Index
# START index
@app.route('/', methods=['GET'])
def index():
    session['region'] = region
    session['cities'] = cities
    session['riding'] = None
    if current_user.is_authenticated:
        session['city'] = current_user.city
        return redirect(url_for(DEFAULT_ROUTE_AUTHENTICATED, _external=True, _scheme=protocol))
    else:
        session['city'] = cities[0]
        return redirect(url_for(DEFAULT_ROUTE_NOT_AUTHENTICATED, _external=True, _scheme=protocol))
# END index


# Login page
# START login_page
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for(DEFAULT_ROUTE_AUTHENTICATED, _external=True, _scheme=protocol))
    else:
        form = CredentialForm()
        if form.validate_on_submit():
            try:
                user = movr.get_user(username=form.username.data)
                if user is None or not check_password_hash(
                        user.password_hash, form.password.data):
                    flash(
                        Markup(
                            'Invalid user credentials.<br>If you aren\'t registered with MovR, go <a href="{0}">Sign Up</a>!'
                        ).format(
                            url_for('register',
                                    _external=True,
                                    _scheme=protocol)))
                    return redirect(
                        url_for('login_page', _external=True,
                                _scheme=protocol))
                login_user(user)
                return redirect(
                    url_for(DEFAULT_ROUTE_AUTHENTICATED, _external=True, _scheme=protocol))
            except Exception as error:
                flash('{0}'.format(error))
                return redirect(
                    url_for('login_page', _external=True, _scheme=protocol))
        return render_template('login.html',
                               title='Log In',
                               form=form,
                               available=session['region'])
# END login_page


# Logout route
@login_required
@app.route('/logout')
def logout():
    logout_user()
    session['riding'] = None
    flash('You have successfully logged out.')
    return redirect(url_for('login_page', _external=True, _scheme=protocol))


# Registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for(DEFAULT_ROUTE_AUTHENTICATED, _external=True, _scheme=protocol))
    else:
        form = RegisterForm()
        if form.validate_on_submit():
            try:
                movr.add_user(city=form.city.data,
                              first_name=form.first_name.data,
                              last_name=form.last_name.data,
                              email=form.email.data,
                              username=form.username.data,
                              password=form.password.data)
                flash('Registration successful! You can now log in as {0}.'.
                      format(form.username.data))
                return redirect(
                    url_for('login_page', _external=True, _scheme=protocol))
            except DBAPIError as sql_error:
                flash(
                    '{0}\n Registration failed. Make sure that you choose a unique username!'
                        .format(sql_error))
                return redirect(
                    url_for('register', _external=True, _scheme=protocol))
            except Exception as error:
                flash('{0}'.format(error))
                return redirect(
                    url_for('register', _external=True, _scheme=protocol))
        return render_template('register.html',
                               title='Sign Up',
                               form=form,
                               available=session['region'])


# Users page
@login_required
@app.route('/users', methods=['GET'])
def users():
    if current_user.is_authenticated:
        users = movr.get_users(session['city'])
        return render_template('users.html',
                               title='Users',
                               users=users,
                               available=session['region'])
    else:
        flash('You need to log in to see active users in your city!')
        return redirect(url_for('login_page', _external=True,
                                _scheme=protocol))


# User page
@login_required
@app.route('/users/<user_id>', methods=['GET'])
def user(user_id):
    v = movr.get_vehicles(city=current_user.city)
    form_u = RemoveUserForm()
    form_v = RemoveVehicleForm()
    if current_user.is_authenticated and user_id == current_user.id:
        return render_template('user.html',
                               title='My Profile',
                               form_u=form_u,
                               form_v=form_v,
                               vehicles=v,
                               available=session['region'],
                               API_KEY=app.config.get('API_KEY'))
    else:
        flash('You need to log in to see your profile!')
        return redirect(url_for('login_page', _external=True,
                                _scheme=protocol))


# Remove user route
@login_required
@app.route('/users/remove/<user_id>', methods=['POST'])
def remove_user(user_id):
    movr.remove_user(user_id=user_id)
    logout_user()
    session['riding'] = None
    flash('You have successfully deleted your account.')
    return redirect(url_for(DEFAULT_ROUTE_NOT_AUTHENTICATED, _external=True, _scheme=protocol))


# Vehicles page
@login_required
@app.route('/vehicles', methods=['GET'])
def vehicles():
    form = StartRideForm()
    vehicles = movr.get_vehicles(session['city'])
    return render_template('vehicles.html',
                           title='Vehicles',
                           vehicles=vehicles,
                           form=form,
                           available=session['region'],
                           API_KEY=app.config.get('API_KEY'))


# Add vehicles route
@login_required
@app.route('/vehicles/add', methods=['GET', 'POST'])
def add_vehicle():
    form = VehicleForm()
    if form.validate_on_submit():
        try:
            movr.add_vehicle(city=current_user.city,
                             owner_id=current_user.id,
                             last_location=form.location.data,
                             type=form.type.data,
                             color=form.color.data,
                             brand=form.brand.data,
                             status='available',
                             is_owner=current_user.is_owner)
            flash('Vehicle added in {0}!'.format(current_user.city.title()))
            return redirect(
                url_for('vehicles', _external=True, _scheme=protocol))
        except Exception as error:
            flash('{0}'.format(error))
            return redirect(
                url_for('vehicles', _external=True, _scheme=protocol))
    if session['city'] != current_user.city:
        session['city'] = current_user.city
        flash('You can only add vehicles in your home city, {0}.'.format(current_user.city.title()))
    return render_template('vehicles-add.html',
                           title='Add a vehicle',
                           form=form,
                           available=session['region'])


# Remove vehicle route
@login_required
@app.route('/vehicles/remove/<vehicle_id>', methods=['POST'])
def remove_vehicle(vehicle_id):
    movr.remove_vehicle(vehicle_id=vehicle_id)
    flash('You have successfully removed a vehicle.')
    return redirect('{0}{1}{2}'.format(
        url_for('users', _external=True, _scheme=protocol), '/',
        current_user.id))


# Rides page
@login_required
@app.route('/rides', methods=['GET'])
def rides():
    form = EndRideForm()
    rides = movr.get_rides(rider_id=current_user.id)
    for ride in rides:
        if current_user.id == ride['rider_id']:
            if ride['end_time'] is None:
                session['riding'] = True
                pass
    return render_template('rides.html',
                           title='Rides',
                           rides=reversed(rides),
                           form=form,
                           riding=session['riding'],
                           available=session['region'])


# Start ride route
@login_required
@app.route('/rides/start/<vehicle_id>', methods=['POST'])
def start_ride(vehicle_id):
    try:
        if session['riding']:
            flash(
                'You are already riding. End your current ride before starting a new one!'
            )
            return redirect(url_for('rides', _external=True, _scheme=protocol))
        else:
            rides = movr.get_rides(rider_id=current_user.id)
            for r in rides:
                if r['end_time'] is None:
                    session['riding'] = True
                    pass
        movr.start_ride(city=session['city'],
                        rider_id=current_user.id,
                        vehicle_id=vehicle_id)
        session['riding'] = True
        flash('Ride started.')
        return redirect(url_for('rides', _external=True, _scheme=protocol))
    except Exception as error:
        flash('{0}'.format(error))
        return redirect(url_for('vehicles', _external=True, _scheme=protocol))


# End ride route
@login_required
@app.route('/rides/end/<ride_id>', methods=['POST'])
def end_ride(ride_id):
    try:
        form = EndRideForm()
        movr.end_ride(ride_id=ride_id,
                      location=form.location.data)
        session['riding'] = False
        flash('Ride ended.')
        return redirect(url_for('rides', _external=True, _scheme=protocol))
    except Exception as error:
        flash('{0}'.format(error))
        return redirect(url_for('rides', _external=True, _scheme=protocol))

# Set new city route
@login_required
@app.route('/city/<city>', methods=['POST'])
def set_city(city):
    try:
        session['city'] = city
    except Exception as error:
        flash('{0}'.format(error))
        session['city'] = current_user.city
    finally:
        flash('Now using {0} as your current city.'.format(session['city'].title()))
        return redirect(url_for('vehicles', _external=True, _scheme=protocol))


if __name__ == '__main__':
    app.run()
