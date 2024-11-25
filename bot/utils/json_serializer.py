from datetime import datetime, date, time


class JsonSerializer:
    @staticmethod
    def default(obj):
        if isinstance(obj, datetime):
            return obj.strftime("%d.%m.%Y %H:%M")
        elif isinstance(obj, date):
            return obj.strftime("%d.%m.%Y")
        elif isinstance(obj, time):
            return obj.strftime("%H:%M")
        raise TypeError(
            f"Object of type {obj.__class__.__name__} is not JSON serializable"
        )
