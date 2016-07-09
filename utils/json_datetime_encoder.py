import json
import datetime


class DatetimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%dT%H:%M:%SZ')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


class ComplexEncoder(DatetimeEncoder):
    def default(self, obj):
        if hasattr(obj, '__dict__'):
            return obj.__dict__

        return super().default(obj)





