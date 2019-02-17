#!/usr/bin/env python3

import sys
import os
import argparse

sys.path.insert(1, os.path.join(sys.path[0], '..', 'lib'))

import db.sync.misc as db
import db.sync.buildings as buildings
import arcgis.request as arcgis

import config
import log

from log import info


def fetch_all(id_obj_start, batch_size):
    while True:
        id_obj_end = id_obj_start + batch_size
        info('Fetching next batch: from %d to %d' % (id_obj_start, id_obj_end))
        response = arcgis.fetch_range(id_obj_start, id_obj_end)
        yield response
        info('Fetched %d records' % len(response))
        if len(response) < batch_size:
            info('All data fetched')
            raise StopIteration
        id_obj_start = id_obj_end


def load_data(conn, id_obj_start, batch_size):
    for response in fetch_all(id_obj_start, batch_size):
        buildings.add_from_arcgis(conn, response)

def run():
    parser = argparse.ArgumentParser()

    parser.add_argument("-d", help="Log level DEBUG", dest='debug', action="store_true")
    parser.add_argument("-c", help="Config file path", dest='conf_file')
    parser.add_argument("-b", help="Batch size for fetching", dest='batch_size', default=1000, type=int)

    args = parser.parse_args()

    log.init(debug=args.debug)
    conf = config.load(args.conf_file)
    conn = db.connect(conf['db_path'])
    response = arcgis.fetch_row(1) # use this response to build tables from schema, discard the data
    buildings.init_from_arcgis(conn, response)
    last_id = buildings.get_last_id(conn, response.primary_key)
    info("Starting from object id %d" % last_id)
    load_data(conn, last_id, args.batch_size)
    
    

if __name__ == '__main__':
    run()
