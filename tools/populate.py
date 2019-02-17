#!/usr/bin/env python3

import argparse
import random
import time
import itertools
import sqlite3

MAX_DATE_DIFF = 36000
MAX_ID_CHANNEL = 3
MAX_ID_CAMPAIGN = 3
MAX_ID_COUNTRY = 3
MAX_ID_OS = 3
MAX_METRIC_VAL = 100

def make_record():
    while True:
        r = [ random.randint(0, MAX_METRIC_VAL) for _ in range(5) ]
        r.extend([ random.randint(1, m) for m in [MAX_ID_CHANNEL, MAX_ID_CAMPAIGN, MAX_ID_COUNTRY, MAX_ID_OS] ])
        r.append(time.strftime('%D %T', time.localtime(time.time() - random.randint(0, MAX_DATE_DIFF))))
        yield r
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", help="Size of the records to create", type=int, dest='size', required=True)
    parser.add_argument("-db", help="Path to the database file", dest='db', required=True)
    args = parser.parse_args()
    conn = sqlite3.connect(args.db)
    conn.executemany("""
       INSERT INTO records(
              impressions, clicks, installs, spend, revenue,
              id_channel, id_campaign, id_country, id_os,
              record_date
       )  VALUES(
           ?, ?, ?, ?, ?,
           ?, ?, ?, ?,
           ?
       )
    """, itertools.islice(make_record(), args.size)
    )
    conn.commit()
    


    

