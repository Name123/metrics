import aiosqlite
from tornado.options import options

ARGS_TO_TABLE_DESCRS = {
    'channel' : {
        'col' : 'id_channel',
        'table' : 'channels'
    },
    'campaign' : {
        'col' : 'id_campaign',
        'table' : 'campaigns'
    },
    'country' : {
        'col' : 'id_country',
        'table' : 'countries'
    },
    'os' : {
        'col' : 'id_os',
        'table' : 'operating_systems'
    },
    'date' : {
        'col ' : 'record_date'
    }
}


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

async def count(groups):
    cols = ",".join([ "%s.name as %s_name" % (t['table'], t['table']) for t in groups ])
    group_by = " GROUP BY %s" % ",".join([t['col'] for t in groups ])
    sql = "SELECT COUNT(*) as cnt," + cols + """
         FROM
            records
         JOIN
            channels USING (id_channel)
         JOIN
            campaigns USING (id_campaign)
         JOIN
            countries USING (id_country)
         JOIN
            operating_systems USING (id_os)
    """ + group_by
    async with aiosqlite.connect(options.db) as conn:
        conn.row_factory = dict_factory
        cursor = await conn.execute(sql)
        rows = await cursor.fetchall()
        await cursor.close()
        return rows
    
async def list(date_min, date_max, filters, sort):
    sql = """
          SELECT
              impressions, clicks, installs, revenue, spend,
              record_date,
              channels.name as channel_name,
              campaigns.name as campaign_name,
              countries.name as country_name,
              operating_systems.name as os_name,
              spend / CAST (installs as FLOAT) as cpi
          FROM
              records
          JOIN
              channels USING (id_channel)
          JOIN
              campaigns USING (id_campaign)
          JOIN
              countries USING (id_country)
          JOIN
              operating_systems USING (id_os)
    """
    args = []
    if date_min or date_max or filters:
        sql += " WHERE "
        date_min_clause, date_max_clause = '1', '1'
        if date_min:
            date_min_clause = "record_date >= ?"
            args.append(date_min.strftime('%D %T'))
        if date_max:
            date_max_clause = "record_date <= ?"
            args.append(date_max.strftime('%D %T'))
        date_clause = " AND ".join([date_min_clause, date_max_clause])
        sql += date_clause
        for t in filters:
            table, vals = t
            sql += " AND %s.name IN (%s)" % (table, ','.join(["?" for _ in range(len(vals)) ]))
            args.extend(vals)
            
    if sort:
        sql += ' ORDER BY %s' % sort

    async with aiosqlite.connect(options.db) as conn:
        conn.row_factory = dict_factory
        cursor = await conn.execute(sql, args)
        rows = await cursor.fetchall()
        await cursor.close()
        return rows
