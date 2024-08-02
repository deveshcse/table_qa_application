from flask import Blueprint, request, redirect, url_for, flash, render_template
from flask_mysqldb import MySQL
import os
from werkzeug.utils import secure_filename
from datetime import datetime
import logging




processing_bp = Blueprint('processing', __name__)
mysql = MySQL()

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}


# Check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@processing_bp.route('/upload', methods=['GET', 'POST'])
def upload():
    session_id = request.cookies.get('session_id')
    if not session_id:
        flash('You must be logged in to upload a PDF!', 'danger')
        return redirect(url_for('authentication.login'))

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT user_id FROM user_session_table WHERE session_id = %s AND is_valid = %s', (session_id, True))
    session_record = cursor.fetchone()
    if not session_record:
        flash('Session invalid or expired. Please log in again.', 'danger')
        return redirect(url_for('authentication.login'))

    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)

            flash('PDF uploaded successfully!', 'success')
            return redirect(url_for('processing.upload'))
        else:
            flash('Invalid file format. Please upload a PDF file.', 'danger')

    return render_template('upload.html')
