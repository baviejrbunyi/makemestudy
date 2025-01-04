from flask import Flask, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
from study_plan import summarize_book, create_study_plan  # Assuming your functions are in study_plan.py

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'downloads'  # Folder to store uploaded files
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'docx'}
app.secret_key = 'your_secret_key'

# Check if the file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def home():
    return render_template('html/index.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Validate form fields
    number_of_days = request.form.get('number-of-days')
    start_time = request.form.get('start-time')
    end_time = request.form.get('end-time')
    
    if not (number_of_days and start_time and end_time):
        flash('All fields are required!', 'error')
        return redirect(url_for('home'))

    # Handle file upload
    file = request.files.get('file')
    if file and allowed_file(file.filename):
        # Ensure the 'downloads' directory exists
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        # Secure the filename
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Summarize the uploaded book (file)
        try:
            material = summarize_book(file_path)
        except Exception as e:
            flash(f"Error summarizing the file: {e}", 'error')
            return redirect(url_for('home'))

        # Create a study plan based on the summarized content
        try:
            study_plan = create_study_plan(material, int(number_of_days), start_time, end_time)
        except Exception as e:
            flash(f"Error creating study plan: {e}", 'error')
            return redirect(url_for('home'))

        # Pass the study plan to the template to display it
        return render_template('html/study_plan.html', study_plan=study_plan)

    else:
        flash('Invalid file type. Only .pdf or .docx are allowed.', 'error')
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
