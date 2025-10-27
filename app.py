from flask import Flask, render_template, request, redirect, url_for
from file_scanner import scan_file_vt
from url_scanner import scan_url_vt

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files or request.files['file'].filename == '':
            return render_template('upload.html', error="No file selected.")
        file = request.files['file']
        result = scan_file_vt(file)
        if result:
            return render_template('scan_result.html', result=result)
        else:
            return render_template('upload.html', error="Error scanning file. Please try again.")
    return render_template('upload.html')

@app.route('/scan_url_endpoint', methods=['POST'])
def scan_url_endpoint():
    url = request.form.get('url')
    if not url:
        return render_template('index.html', error="Please enter a URL to scan.")
    result = scan_url_vt(url)
    if result:
        return render_template('scan_result.html', result=result, url=url)
    else:
        return render_template('index.html', error="Error scanning URL. Please try again.")

if __name__ == '__main__':
    app.run(debug=True)
