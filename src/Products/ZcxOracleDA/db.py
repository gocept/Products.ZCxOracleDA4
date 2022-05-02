##############################################################################
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.0 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE
#
##############################################################################
__version__ = '4.0'

from DateTime import DateTime
from logging import getLogger
from Shared.DC.ZRDB.dbi_db import QueryError
from Shared.DC.ZRDB.TM import TM
from string import split
from string import strip
import cx_Oracle
import datetime


LOG = getLogger('ZRDB.Connection')

# TODO: Add code in to handle db server going away
#   Very minm. unset self.db and reopen at start of this method

CONVERSION_TIMEZONE = 'UTC'


class DB(TM):

    _p_oid = _p_changed = _registered = None

    Database_Connection = cx_Oracle.connect
    Database_Error = cx_Oracle.DatabaseError

    def __init__(self, connection):
        self.connection = connection
        self.db = self.Database_Connection(connection)
        self.cursor = self.db.cursor()

    def _begin(self):
        # print "_begin executed"
        pass

    def _finish(self):
        # print "_finish executed"
        self.db.commit()

    def _abort(self, restarted=False):
        # print "_abort executed"
        try:
            self.db.rollback()
        except:   # noqa: E722 do not use bare 'except'
            pass

    def str(self, v, StringType=type('')):
        if v is None:
            return ''
        r = str(v)
        if r[-1:] == 'L' and type(v) is not StringType:
            r = r[:-1]
        return r

    def _datetime_convert(self, dt, val):
        if dt and val:
            # Currently we don't do timezones. Everything is UTC.
            # Ideally we'd get the current Oracle timezone and use that.
            x = val.timetuple()[:6] + (CONVERSION_TIMEZONE,)
            return DateTime(*x)
        return val

    def _munge_datetime_results(self, items, results):
        if not results or not items:
            return results
        dtmap = [i['type'] == 'd' for i in items]
        nr = []
        for row in results:
            r = tuple([self._datetime_convert(*r) for r in zip(dtmap, row)])
            nr.append(r)
        return nr

    # cxOracle curs.description returns stuff like:
    # [('WAREHOUSE_ID', <type 'cx_Oracle.NUMBER'>, 127, 22, 0, -127, 0),
    #  ('COUNTRY', <type 'cx_Oracle.STRING'>, 30, 30, 0, 0, 1),
    #  ('CITY', <type 'cx_Oracle.STRING'>, 30, 30, 0, 0, 1)]

    def query(self, query_string, max_rows=9999999, query_data=None,
              restarted=False):
        self._register()
        c = self.cursor
        queries = filter(None, map(strip, split(query_string, '\0')))
        if not queries:
            raise QueryError('empty query')
        result = []
        desc = None
        for qs in queries:
            # print "query executing %s"%qs
            try:
                if query_data:
                    r = c.execute(qs, query_data)
                else:
                    r = c.execute(qs)
            except Exception as e:
                # If the connection was stale, we need to restart it.
                if not restarted:
                    # Go back up the chain so that everybody agrees that we are
                    # reconnected.
                    LOG.warning(
                        "Database connection is stale."
                        "  Attempting to re-open.")
                    self._Connection.connect(
                        self._Connection.connection_string)
                    self.db = self.Database_Connection(self.connection)
                    self.cursor = self.db.cursor()
                    # Make sure we don't have more than one level of recursion.
                    # The database may actually be down, not just stale.
                    return self.query(query_string, max_rows, query_data, True)
                else:
                    LOG.error("Failed to reopen stale database connection.")
                    self._Connection.manage_close_connection(None)
                    raise e

            if not r:
                continue
            d = c.description
            if d is None:
                continue
            if desc is None:
                desc = d
            elif d != desc:
                raise QueryError('Multiple select schema are not allowed')
            if not result:
                result = c.fetchmany(max_rows)
            elif len(result) < max_rows:
                result = result+c.fetchmany(max_rows-len(result))

        if desc is None:
            return (), ()

        items = []
        has_datetime = False
        for name, type, width, ds, p, scale, null_ok in desc:
            if type == cx_Oracle.NUMBER:
                if scale == 0:
                    type = 'i'
                else:
                    type = 'n'
            elif type == datetime.datetime:
                has_datetime = True
                type = 'd'
            else:
                type = 's'
            items.append({
                'name': name,
                'type': type,
                'width': width,
                'null': null_ok,
            })
        if has_datetime:
            result = self._munge_datetime_results(items, result)
        return items, result

    def close(self):
        try:
            self.db.close()
        except:   # noqa: E722 do not use bare 'except'
            pass
