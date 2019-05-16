from flask import Flask, request, redirect, url_for, render_template
from process import background_process, conversion, fetch_job

upload_file = './upload_files'
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        # Run the file conversion process in the background
        job_id = background_process(file)
        return redirect(url_for('found', job_id=job_id))
    return render_template('index.html')

@app.route('/found', methods=['GET', 'POST'])
def found():
    job_id = request.args.get('job_id')
    # Get the details of the current job
    job_details = fetch_job(job_id)
    return job_details


if __name__ == '__main__':
    app.run(debug=True)