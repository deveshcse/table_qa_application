from flask import Blueprint, render_template, request, flash, redirect, url_for
import os
from werkzeug.utils import secure_filename
from authentication import update_session_time, get_session_expiry


pdf_processing_bp = Blueprint('pdf_processing', __name__)

# Ensure the uploads directory exists
if not os.path.exists('uploads'):
    os.makedirs('uploads')


@pdf_processing_bp.route('/upload', methods=['GET', 'POST'])
def upload_pdf():
    if request.method == 'POST':
        if 'pdf_file' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)

        file = request.files['pdf_file']
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)

        if file and file.filename.endswith('.pdf'):
            filename = secure_filename(file.filename)
            file_path = os.path.join('uploads', filename)
            file.save(file_path)

            # Call existing PDF processing function here
            # result = process_pdf(file_path)

            flash('File successfully uploaded and processed!', 'success')
            # return redirect(url_for('pdf_processing.upload_pdf'))
        else:
            flash('Only PDF files are allowed', 'danger')

    return render_template('upload.html')
