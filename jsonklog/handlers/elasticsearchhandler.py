# -*- coding: utf-8 -*-
#
#   Copyright [2012] [Patrick Ancillotti]
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#

import logging
import datetime

import requests
import pytz

from jsonklog.handlers.basehandler import RequireJSONFormatter


class ElasticSearchHandler(RequireJSONFormatter):

    def __init__(self, host="localhost", index="logs", port=9200,
                 doc_type="logs", date_based_index=False, date_format="%Y.%m.%d", date_timezone="UTC"):
        if date_based_index:
            tz = pytz.timezone(date_timezone)
            now = tz.localize(datetime.datetime.now())
            index = "{}{}".format(index, now.strftime(date_format))
        logging.Handler.__init__(self)
        self.url = 'http://%s:%s/%s/%s' % (host, port, index, doc_type)

    def emit(self, record):
        msg = self.format(record)

        requests.post(self.url, data=msg)
