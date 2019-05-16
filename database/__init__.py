import MySQLdb

class JobDb():
    def __init__(self):
        self.conn = MySQLdb.connect(host="localhost", user = "root", passwd = "1998", db = "sample")


    def insert_job(self, job_id, job_status):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO job(job_id, job_status) VALUES(%s, %s)", (job_id, job_status, ))
        self.conn.commit()
        cur.close()

    def update_job(self, job_id, job_status):
        cur = self.conn.cursor()
        cur.execute("UPDATE job SET job_status = (%s) WHERE job_id = (%s)", (job_status, job_id, ))
        self.conn.commit()
        cur.close()