"""
Json object
===========
"""

import json
from datetime import datetime


class Json(object):
    @staticmethod
    def pretty(obj):
        return json.dumps(obj=obj, indent=2, default=Json._default)

    @staticmethod
    def compact(obj):
        return json.dumps(obj=obj, default=Json._default)

    @staticmethod
    def _default(obj):
        if isinstance(obj, datetime):
            obj.isoformat()
        return obj.__dict__ if "__dict__" in dir(obj) else "{}".format(obj)
