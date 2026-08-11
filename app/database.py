import sqlite3, random, pandas as pd
from datetime import datetime, timedelta
from.config import settings

class BatchRepository:
    def get_connection(self):
        conn = sqlite3.connect(settings.SQLITE_PATH, check_same_thread=False)
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS batch_jobs (
            job_id TEXT PRIMARY KEY, job_name TEXT, status TEXT,
            batch_type TEXT, start_time TIMESTAMP, end_time TIMESTAMP,
            duration_seconds INT, error_code TEXT, error_message TEXT,
            sla_breach BOOLEAN, retry_count INT
        )''')
        cur.execute("SELECT COUNT(*) FROM batch_jobs")
        if cur.fetchone()[0] == 0:
            self._seed(conn)
        return conn

    def _seed(self, conn):
        types = ['PAYMENT','SETTLEMENT','EOD','CASA','LOANS','RECON','NOSTRO','SWIFT']
        errors = {
            'DB_TIMEOUT': 'Snowflake connection timeout after 300s',
            'FILE_MISSING': 'Inbound file not found',
            'DUPLICATE': 'Duplicate batch ID - checksum failed',
            'AUTH_FAIL': 'Vault token expired - auth failed',
            'SLA_BREACH': 'Batch exceeded SLA 1200s'
        }
        jobs=[]
        for i in range(1247):
            status = random.choices(['SUCCESS','FAILED','RUNNING','DELAYED'], weights=[82,8,6,4])[0]
            btype = random.choice(types)
            start = datetime.now() - timedelta(hours=random.randint(0,72))
            dur = random.randint(30, 2600)
            sla = 1 if dur > 1200 else 0
            code, msg = (random.choice(list(errors.items())) if status=='FAILED' else (None,None))
            jobs.append((f"ENT_{btype}_{10000+i}", f"ENT_{btype}_JOB_{i}", status, btype, start, start+timedelta(seconds=dur), dur, code, msg, sla, random.randint(0,2)))
        conn.executemany("INSERT OR REPLACE INTO batch_jobs VALUES (?,?,?,?,?,?,?,?,?,?,?)", jobs)
        conn.commit()
        print(f"Seeded {len(jobs)} batches for Enterprise Platform")

repo = BatchRepository()