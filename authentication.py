from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, Response, current_app
from flask_mysqldb import MySQL
import MySQLdb.cursors
import os
import hashlib
import uuid
from datetime import datetime, timedelta
import logging
from logging.handlers import RotatingFileHandler


authentication_bp = Blueprint('authentication', __name__)
# Configure logging
log_file_path = 'app.log'
handler = RotatingFileHandler(log_file_path, maxBytes=10000, backupCount=1)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

# Additionally, log to console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

# config = ConfigParser()
# config.read('config.ini')
# _host = config.get('MySQL', 'host')
# _port = config.getint('MySQL', 'port')
# _database = config.get('MySQL', 'database')
# _user = config.get('MySQL', 'user')
# _password = config.get('MySQL', 'password')
#
# app.config['MYSQL_HOST'] = _host
# app.config['MYSQL_USER'] = _user
# app.config['MYSQL_PASSWORD'] = _password
# app.config['MYSQL_DB'] = _database
# app.config['MYSQL_PORT'] = _port


# # Get MySQL configuration from the app context
# mysql = MySQL()
# mysql.init_app(current_app)

mysql = MySQL(app)

SESSION_TIMEOUT_MINUTES = 1


def log_unsuccessful_attempt(client_ip, reason):
    cursor = mysql.connection.cursor()
    cursor.execute('INSERT INTO audit_table (client_ip, reason_of_failure) VALUES (%s, %s)', (client_ip, reason))
    mysql.connection.commit()
    logger.warning(f"Unsuccessful attempt from {client_ip}: {reason}")


def create_session(user_id, client_ip):
    session_id = str(uuid.uuid4())
    cursor = mysql.connection.cursor()
    cursor.execute(
        'INSERT INTO user_session_table (user_id, session_id, session_created, session_updated, client_remote_ip, is_valid) VALUES (%s, %s, %s, %s, %s, %s)',
        (user_id, session_id, datetime.now(), datetime.now(), client_ip, True))
    mysql.connection.commit()
    logger.info(f"Session created: user_id={user_id}, session_id={session_id}, client_ip={client_ip}")
    return session_id


def update_session_time(session_id):
    cursor = mysql.connection.cursor()
    cursor.execute('UPDATE user_session_table SET session_updated = %s WHERE session_id = %s',
                   (datetime.now(), session_id))
    mysql.connection.commit()
    logger.info(f"Session updated: session_id={session_id}")


def get_session_expiry():
    return datetime.now() + timedelta(minutes=SESSION_TIMEOUT_MINUTES)


@authentication_bp.route('/')
def home():
    session_id = request.cookies.get('session_id')
    if session_id:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_session_table WHERE session_id = %s AND is_valid = %s', (session_id, True))
        session_record = cursor.fetchone()
        if session_record:
            now = datetime.now()
            last_updated = session_record['session_updated']

            # Log the initial session_updated time
            logger.debug(f"Initial session_updated time: {last_updated}")

            if now - last_updated > timedelta(minutes=SESSION_TIMEOUT_MINUTES):
                flash('Session timed out due to inactivity. Please log in again.', 'danger')
                logger.info(f"Session timed out: session_id={session_id}")
                return redirect(url_for('authentication.logout'))
            else:
                cursor.execute('UPDATE user_session_table SET session_updated = %s WHERE session_id = %s',
                               (now, session_id))
                mysql.connection.commit()

                # Log the updated session_updated time
                cursor.execute('SELECT session_updated FROM user_session_table WHERE session_id = %s', (session_id,))
                updated_record = cursor.fetchone()
                logger.debug(f"Updated session_updated time: {updated_record['session_updated']}")
                logger.debug(f"The current session {session_id} for user id {session_record['user_id']} will be expired on {updated_record['session_updated'] + timedelta(minutes=SESSION_TIMEOUT_MINUTES)}")

                # Retrieve user role from the database
                cursor.execute('SELECT user_role_id FROM users WHERE id = %s', (session_record['user_id'],))
                user_role = cursor.fetchone()
                user_role_id = user_role['user_role_id'] if user_role else None
                logger.info(f"User logged in: user_id={session_record['user_id']}, user_role_id={user_role_id}")
                return render_template('home.html', userid=session_record['user_id'], user_role_id=user_role_id)
                # response = Response(status=302, headers={'Location': url_for('pdf_processing.upload_pdf')})
                # return response
    logger.info("No valid session found, redirecting to login.")
    return redirect(url_for('authentication.login'))


@authentication_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'userid' in request.form and 'password' in request.form:
        userid = request.form['userid']
        password = request.form['password']
        client_ip = request.remote_addr
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE userid = %s', (userid,))
        account = cursor.fetchone()
        if account:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            if hashed_password == account['password']:
                session_id = create_session(account['id'], client_ip)
                cookie_expires = get_session_expiry()
                response = Response(status=302, headers={'Location': url_for('authentication.home')})

                response.set_cookie(key="session_id", value=session_id, expires=cookie_expires.strftime("%Y-%m-%d %H:%M:%S"), path='/')
                flash('Logged in successfully!', 'success')
                logger.info(f"User logged in successfully: user_id={account['id']}, session_id={session_id}")
                return response
            else:
                log_unsuccessful_attempt(client_ip, 'Incorrect password')
                flash('Incorrect password!', 'danger')
        else:
            log_unsuccessful_attempt(client_ip, 'User not found')
            flash('User not found!', 'danger')
    return render_template('login.html')


@authentication_bp.route('/register', methods=['GET', 'POST'])
def register():
    session_id = request.cookies.get('session_id')
    if not session_id:
        flash('You must be logged in to register a new user!', 'danger')
        logger.warning("Attempt to register without being logged in.")
        return redirect(url_for('authentication.login'))

    if request.method == 'POST' and 'userid' in request.form and 'password' in request.form and 'user_role' in request.form:
        userid = request.form['userid']
        password = request.form['password']
        user_role_id = request.form['user_role']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE userid = %s', (userid,))
        account = cursor.fetchone()
        if account:
            flash('User already exists!', 'danger')
            logger.warning(f"Registration attempt for existing user: userid={userid}")
        else:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            cursor.execute('INSERT INTO users (userid, password, user_role_id) VALUES (%s, %s, %s)',
                           (userid, hashed_password, user_role_id))
            mysql.connection.commit()
            flash('You have successfully registered!', 'success')
            logger.info(f"New user registered: userid={userid}, user_role_id={user_role_id}")
            return redirect(url_for('authentication.login'))
    return render_template('register.html')


@authentication_bp.route('/logout')
def logout():
    session_id = request.cookies.get('session_id')
    if session_id:
        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE user_session_table SET is_valid = %s, session_closed_time = %s WHERE session_id = %s',
                       (False, datetime.now(), session_id))
        mysql.connection.commit()
        response = Response(status=302, headers={'Location': url_for('authentication.login')})
        response.delete_cookie('session_id')
        flash('You have successfully logged out!', 'success')
        logger.info(f"User logged out: session_id={session_id}")
        return response
    logger.info("Logout attempt without a valid session.")
    return redirect(url_for('authentication.login'))


if __name__ == '__main__':
    app.run(debug=True)
