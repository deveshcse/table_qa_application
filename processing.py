# from flask import Blueprint, request, redirect, url_for, flash, render_template
# from flask_mysqldb import MySQL
# import os
# from werkzeug.utils import secure_filename
# from datetime import datetime, timedelta
# import logging
# import MySQLdb.cursors
#
#
# # Logging configuration
# logging.basicConfig(level=logging.DEBUG,  # Change to logging.INFO in production
#                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                     handlers=[
#                         logging.FileHandler('app.log'),  # Log to a file
#                         logging.StreamHandler()  # Log to console
#                     ])
#
# logger = logging.getLogger(__name__)
#
# processing_bp = Blueprint('processing', __name__)
# mysql = MySQL()
#
# UPLOAD_FOLDER = 'uploads'
# ALLOWED_EXTENSIONS = {'pdf'}
#
# SESSION_TIMEOUT_MINUTES = 1
# # Check if the file extension is allowed
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
#
#
# @processing_bp.route('/upload', methods=['GET', 'POST'])
# def upload():
#     session_id = request.cookies.get('session_id')
#     # if not session_id:
#     #     flash('You must be logged in to upload a PDF!', 'danger')
#     #     return redirect(url_for('authentication.login'))
#     if session_id:
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute('SELECT * FROM user_session_table WHERE session_id = %s AND is_valid = %s', (session_id, True))
#         session_record = cursor.fetchone()
#         if session_record:
#             now = datetime.now()
#             last_updated = session_record['session_updated']
#
#             # Log the initial session_updated time
#             logger.debug(f"Initial session_updated time at upload route: {last_updated}")
#
#             if now - last_updated > timedelta(minutes=SESSION_TIMEOUT_MINUTES):
#                 flash('Session timed out due to inactivity. Please log in again.', 'danger')
#                 logger.info(f"Session timed out: session_id={session_id}")
#                 return redirect(url_for('authentication.logout'))
#             else:
#                 cursor.execute('UPDATE user_session_table SET session_updated = %s WHERE session_id = %s',
#                                (now, session_id))
#                 mysql.connection.commit()
#
#                 # Log the updated session_updated time
#                 cursor.execute('SELECT session_updated FROM user_session_table WHERE session_id = %s', (session_id,))
#                 updated_record = cursor.fetchone()
#                 logger.debug(f"Updated session_updated time: {updated_record['session_updated']}")
#                 logger.debug(f"The current session {session_id} for user id {session_record['user_id']} will be expired on {updated_record['session_updated'] + timedelta(minutes=SESSION_TIMEOUT_MINUTES)}")
#
#
#     # cursor = mysql.connection.cursor()
#     # cursor.execute('SELECT user_id FROM user_session_table WHERE session_id = %s AND is_valid = %s', (session_id, True))
#     # session_record = cursor.fetchone()
#     # if not session_record:
#     #     flash('Session invalid or expired. Please log in again.', 'danger')
#     #     return redirect(url_for('authentication.login'))
#
#                 if request.method == 'POST':
#                     if 'file' not in request.files:
#                         flash('No file part', 'danger')
#                         return redirect(request.url)
#
#                     file = request.files['file']
#                     if file.filename == '':
#                         flash('No selected file', 'danger')
#                         return redirect(request.url)
#
#                     if file and allowed_file(file.filename):
#                         filename = secure_filename(file.filename)
#                         file_path = os.path.join(UPLOAD_FOLDER, filename)
#                         file.save(file_path)
#
#                         flash('PDF uploaded successfully!', 'success')
#                         return redirect(url_for('processing.upload'))
#                     else:
#                         flash('Invalid file format. Please upload a PDF file.', 'danger')
#
#     return render_template('upload.html')



from flask import Blueprint, request, redirect, url_for, flash, render_template
from flask_mysqldb import MySQL
import os
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import logging
import MySQLdb.cursors

# Logging configuration
logging.basicConfig(level=logging.DEBUG,  # Change to logging.INFO in production
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler('app.log'),  # Log to a file
                        logging.StreamHandler()  # Log to console
                    ])

logger = logging.getLogger(__name__)

processing_bp = Blueprint('processing', __name__)
mysql = MySQL()

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

SESSION_TIMEOUT_MINUTES = 1

# Check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @processing_bp.route('/upload', methods=['GET', 'POST'])
# def upload():
#     session_id = request.cookies.get('session_id')
#     if session_id:
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute('SELECT * FROM user_session_table WHERE session_id = %s AND is_valid = %s', (session_id, True))
#         session_record = cursor.fetchone()
#         if session_record:
#             now = datetime.now()
#             last_updated = session_record['session_updated']
#
#             # Log the initial session_updated time
#             logger.debug(f"Initial session_updated time at upload route: {last_updated}")
#
#             if now - last_updated > timedelta(minutes=SESSION_TIMEOUT_MINUTES):
#                 flash('Session timed out due to inactivity. Please log in again.', 'danger')
#                 logger.info(f"Session timed out: session_id={session_id}")
#                 return redirect(url_for('authentication.logout'))
#             else:
#                 cursor.execute('UPDATE user_session_table SET session_updated = %s WHERE session_id = %s', (now, session_id))
#                 mysql.connection.commit()
#
#                 # Log the updated session_updated time
#                 cursor.execute('SELECT session_updated FROM user_session_table WHERE session_id = %s', (session_id,))
#                 updated_record = cursor.fetchone()
#                 logger.debug(f"Updated session_updated time: {updated_record['session_updated']}")
#                 logger.debug(f"The current session {session_id} for user id {session_record['user_id']} will be expired on {updated_record['session_updated'] + timedelta(minutes=SESSION_TIMEOUT_MINUTES)}")
#
#                 if request.method == 'POST':
#                     if 'file' not in request.files:
#                         flash('No file part', 'danger')
#                         logger.error('No file part in request')
#                         return redirect(request.url)
#
#                     file = request.files['file']
#                     if file.filename == '':
#                         flash('No selected file', 'danger')
#                         logger.error('No selected file')
#                         return redirect(request.url)
#
#                     if file and allowed_file(file.filename):
#                         filename = secure_filename(file.filename)
#                         file_path = os.path.join(UPLOAD_FOLDER, filename)
#                         try:
#                             file.save(file_path)
#                             logger.info(f"File {filename} saved to {file_path}")
#                         except Exception as e:
#                             logger.error(f"Failed to save file: {e}")
#                             flash('Failed to upload file.', 'danger')
#                             return redirect(request.url)
#
#                         flash('PDF uploaded successfully!', 'success')
#                         return redirect(url_for('processing.upload'))
#                     else:
#                         flash('Invalid file format. Please upload a PDF file.', 'danger')
#                         logger.error('Invalid file format')
#
#     return render_template('upload.html')


@processing_bp.route('/upload', methods=['GET', 'POST'])
def upload():
    session_id = request.cookies.get('session_id')
    if session_id:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_session_table WHERE session_id = %s AND is_valid = %s', (session_id, True))
        session_record = cursor.fetchone()
        if session_record:
            now = datetime.now()
            last_updated = session_record['session_updated']

            # Log the initial session_updated time
            logger.debug(f"Initial session_updated time at upload route: {last_updated}")

            if now - last_updated > timedelta(minutes=SESSION_TIMEOUT_MINUTES):
                flash('Session timed out due to inactivity. Please log in again.', 'danger')
                logger.info(f"Session timed out: session_id={session_id}")
                return redirect(url_for('authentication.logout'))
            else:
                cursor.execute('UPDATE user_session_table SET session_updated = %s WHERE session_id = %s', (now, session_id))
                mysql.connection.commit()

                # Log the updated session_updated time
                cursor.execute('SELECT session_updated FROM user_session_table WHERE session_id = %s', (session_id,))
                updated_record = cursor.fetchone()
                logger.debug(f"Updated session_updated time: {updated_record['session_updated']}")
                logger.debug(f"The current session {session_id} for user id {session_record['user_id']} will be expired on {updated_record['session_updated'] + timedelta(minutes=SESSION_TIMEOUT_MINUTES)}")

            if request.method == 'POST':
                logger.debug(f"Request files: {request.files}")
                if 'file' not in request.files:
                    flash('No file part', 'danger')
                    logger.error('No file part in request')
                    return redirect(request.url)

                file = request.files['file']
                if file.filename == '':
                    flash('No selected file', 'danger')
                    logger.error('No selected file')
                    return redirect(request.url)

                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(UPLOAD_FOLDER, filename)
                    try:
                        file.save(file_path)
                        logger.info(f"File {filename} saved to {file_path}")
                    except Exception as e:
                        logger.error(f"Failed to save file: {e}")
                        flash('Failed to upload file.', 'danger')
                        return redirect(request.url)

                    flash('PDF uploaded successfully!', 'success')
                    return redirect(url_for('processing.upload'))
                else:
                    flash('Invalid file format. Please upload a PDF file.', 'danger')
                    logger.error('Invalid file format')

    return render_template('upload.html')


