import datetime
import calendar
import time
import comparable

class EDTime(object, comparable.ComparableMixin):
    @staticmethod
    def js_epoch_now():
        return 1000 * calendar.timegm(time.gmtime())
    
    @staticmethod
    def immersive_delta():
        return 1286 # Elite Dangerous is set 1286 years in the future

    @staticmethod
    def t_minus(js_epoch_then, short=False):
        ago = int((EDTime.js_epoch_now() - js_epoch_then) / 1000)
        if short:
            return u"-{}".format(EDTime.pretty_print_timespan(ago, short=True))
        return u"T-{}".format(EDTime.pretty_print_timespan(ago))

    @staticmethod
    def pretty_print_timespan(timespan, short=False, verbose=False):
        if timespan < 0:
            raise ValueError('Invalid input')
        remaining = timespan
        days = remaining / 86400
        remaining -= days * 86400

        hours = (remaining / 3600) % 24
        remaining -= hours * 3600

        minutes = (remaining / 60) % 60
        remaining -= minutes * 60

        seconds = (remaining % 60)

        readable = ""
        if days > 0:
            suffix = (u" days" if days > 1 else u" day") if verbose else "d"            
            readable = u"{}{}".format(days, suffix)
            if hours > 0 and not short:
                suffix = (u" hours" if hours > 1 else u" hour") if verbose else "h"
                readable += u":{}{}".format(hours, suffix)
        elif hours > 0:
            suffix = (u" hours" if hours > 1 else u" hour") if verbose else "h"
            readable = u"{}{}".format(hours, suffix)
            if minutes > 0 and not short:
                suffix = (u" minutes" if minutes > 1 else u" minute") if verbose else "m"
                readable += u":{}{}".format(minutes, suffix)
        elif minutes > 0:
            suffix = (u" minutes" if minutes > 1 else u" minute") if verbose else "m"
            readable = u"{}{}".format(minutes, suffix)
            if seconds > 0 and not short:
                suffix = (u" seconds" if seconds > 1 else u" second") if verbose else "s"
                readable += u":{}{}".format(seconds, suffix)
        else:
            suffix = (u" seconds" if seconds > 1 else u" second") if verbose else "s"
            readable = u"{}{}".format(seconds, suffix)

        return readable

    @staticmethod
    def from_js_epoch(js_epoch):
        a_datetime = datetime.datetime.fromtimestamp(js_epoch / 1000)
        return EDTime(a_datetime)

    @staticmethod
    def from_journal_timestamp(journal_timestamp):
        a_datetime = datetime.datetime.strptime(journal_timestamp, '%Y-%m-%dT%H:%M:%SZ')
        return EDTime(a_datetime)

    def __immmersive(self):
        d = self._datetime
        try:
            return d.replace(year = d.year + EDTime.immersive_delta())
        except ValueError:
            return d + (datetime.date(d.year + EDTime.immersive_delta(), 1, 1) - datetime.date(d.year, 1, 1))

    def __init__(self, a_datetime=None):
        if datetime:
            self._datetime = a_datetime
        else:
            self._datetime = datetime.datetime.now()

         
    def as_js_epoch(self):
        return int(calendar.timegm(self._datetime.timetuple()) * 1000)

    def as_py_epoch(self):
        return int(calendar.timegm(self._datetime.timetuple()))

    def as_datetime(self):
        return self._datetime

    def as_journal_timestamp(self):
        return self._datetime.strftime('%Y-%m-%dT%H:%M:%SZ')
        
    def as_immersive_date(self):
        immersive_datetime = self.__immmersive()
        return immersive_datetime.strftime('%Y-%m-%d')

    def is_upcoming(self, time_horizon_days):
        if self.is_past():
            return False
        delta  = self._datetime - datetime.datetime.now()
        return delta <= datetime.timedelta(days=time_horizon_days)

    def is_past(self):
        return self._datetime < datetime.datetime.now()

    def is_future(self):
        return self._datetime > datetime.datetime.now()

    def __lt__(self, other):
        if isinstance(other, EDTime):
            return self._datetime < other._datetime
        else:
            return NotImplemented

    def elapsed_threshold(self, journal_timestamp, threshold_timedelta):
        edt= EDTime.from_journal_timestamp(journal_timestamp)

        if edt < self:
            return False

        return (edt._datetime - self._datetime) >= threshold_timedelta

    def __str__(self):
        return str(self.as_journal_timestamp())

    def t_notation(self, short=False):
        delta = int((EDTime.js_epoch_now() - self.as_js_epoch()) / 1000)
        prefix = u"+" if delta < 0 else u"-"
        if short:
            return u"{}{}".format(prefix, EDTime.pretty_print_timespan(abs(delta), short=True))
        return u"T{}{}".format(prefix, EDTime.pretty_print_timespan(abs(delta)))

    __repr__ = __str__ 