from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
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
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('File uploaded successfully!', 'success')
        # Process further or redirect
        return redirect(url_for('home'))
    else:
        flash('Invalid file type. Only .pdf or .docx are allowed.', 'error')
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
