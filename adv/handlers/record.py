import tornado
from datetime import datetime

import adv.model.record as model

DATETIME_FMT = '%Y.%m.%dT%H:%M:%S'

def parse_datetime(timestr):
    return timestr and datetime.strptime(timestr, DATETIME_FMT)

def fmt_response(data):
    return {
        'data' : data
    }

class RecordListHandler(tornado.web.RequestHandler):
    async def get(self):
        date_min, date_max = [ parse_datetime(self.get_argument(s, None)) for s in ['date_min', 'date_max' ] ]
        sort = (model.ARGS_TO_TABLE_DESCRS.get(self.get_argument("sort", None)) or {}).get('col')
        filters = [ (model.ARGS_TO_TABLE_DESCRS[s]['table'], self.get_arguments(s)) for s in model.ARGS_TO_TABLE_DESCRS.keys() if self.get_arguments(s) ]
        res = await model.list(date_min, date_max, filters, sort)
        self.write(fmt_response(res))


class RecordCountHandler(tornado.web.RequestHandler):
    async def get(self):
        groups = [ model.ARGS_TO_TABLE_DESCRS[s] for s in self.get_arguments('group') if model.ARGS_TO_TABLE_DESCRS.get(s)  ]
        if not groups:
            raise tornado.web.HTTPError(400)
        res = await model.count(groups)
        self.write(fmt_response(res))
