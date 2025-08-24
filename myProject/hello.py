from flask import Flask, render_template
from flask import send_from_directory

# # name of the application module
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/projects/')
def projects():
    return 'The project page'

@app.route('/about/')
def about():
    return 'The about page'
    
@app.route('/download')
def download_pdf():
    return send_from_directory('static', 'res.pdf', as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
 