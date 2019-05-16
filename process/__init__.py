from redis import Redis
from werkzeug.utils import secure_filename
import camelot
from rq import Queue, get_current_job
from rq.job import Job
import time
from PIL import Image 
import pytesseract 
from pdf2image import convert_from_path
import os
from database import JobDb

# Queue initialisation
q = Queue(connection=Redis())
q.empty()
# Database initialisation
db = JobDb()

def background_process(file):
        PDF_file = secure_filename(file.filename)
        file.save(os.path.join('./upload_files/', PDF_file))
        result = q.enqueue(conversion, PDF_file, job_timeout=3600)
        job_id = result.id
        job = Job.fetch(job_id, connection=Redis())
        job_status = job.get_status()
        # Insert the job details into the database
        db.insert_job(job_id, job_status)
        return(job_id)

def conversion(file_name):
        job = get_current_job()
        job_id = job.id
        file_path = './upload_files/'+file_name
        tables = camelot.read_pdf(file_path)
        # Check for any tabular content in PDF file
        if tables:
                filename = './download_files/'+job_id+'.csv'
                tables.export(filename, f='csv', compress=True)
                tables[0].to_csv(filename)
        pages = convert_from_path(file_path, 500)
        image_counter = 1
        for page in pages: 
                # Separate the pages of the PDF file into images
                filename = "./photo/"+job_id+"_"+str(image_counter)+".jpg"
                page.save(filename, 'JPEG') 
                image_counter = image_counter + 1
        outfile = './download_files/'+job_id+'.txt'
        f = open(outfile, 'w')
        for i in range(1, image_counter):
                filename = "./photo/"+job_id+"_"+str(i)+".jpg"
                # Get the text content in the PDF file
                text = str(pytesseract.image_to_string(Image.open(filename)))
                text = text.replace('-\n','')
                f.write(text) 

def fetch_job(job_id):
        job = Job.fetch(job_id, connection=Redis())
        job_status = job.get_status()
        # Update the job details into the database
        db.update_job(job_id, job_status)
        # Check whether the job is finshed
        if job.is_finished:
                job_details = 'File conversion  '+job_status 
                return job_details
        else:
                job_details = 'File conversion  '+job_status 
                return job_details