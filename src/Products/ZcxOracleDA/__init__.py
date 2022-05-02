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
__doc__ = "ZcxOracle Database Adaptor Registration."
__version__ = '$Revision: 0.6 $'[11:-2]

import DA
import os.path
import Shared.DC.ZRDB


def initialize(context):
    context.registerClass(
        DA.Connection,
        permission='Add Z cxOracle Database Connections',
        constructors=(DA.manage_addZcxOracleConnectionForm,
                      DA.manage_addZcxOracleConnection),
        icon=os.path.join(os.path.dirname(
            Shared.DC.ZRDB.__file__), 'www', 'DBAdapterFolder_icon.gif')
    )
