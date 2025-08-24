import os
import logging
from flask import Flask, render_template, send_file, abort

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

@app.route('/')
def index():
    """Main portfolio page"""
    return render_template('index.html')

@app.route('/resume')
def download_resume():
    """Download resume PDF"""
    try:
        resume_path = os.path.join(app.static_folder or 'static', 'resume', 'Vedant_Kulkarni_Resume.pdf')
        if os.path.exists(resume_path):
            return send_file(resume_path, as_attachment=True, download_name='Vedant_Kulkarni_Resume.pdf')
        else:
            abort(404)
    except Exception as e:
        app.logger.error(f"Error serving resume: {e}")
        abort(500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
