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
__doc__ = """Database Connection adaptor for cxOracle"""
__version__ = '4.0'

import Shared.DC.ZRDB.Connection


class Connection(Shared.DC.ZRDB.Connection.Connection):
    _isAnSQLConnection = 1

    manage_options = Shared.DC.ZRDB.Connection.Connection.manage_options

    info = None

    def tpValues(self):
        return []

    def __getitem__(self, name):
        raise KeyError(name)
