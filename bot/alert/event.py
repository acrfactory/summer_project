from dataclasses import dataclass
from datetime import datetime, timedelta, tzinfo
from math import ceil

from bot.common.user_custom import UserCustom
from conf import Conf


@dataclass
class Event:
    id_: int
    created_by: UserCustom
    repeat_interval: timedelta  # Interval in days
    name: str
    next_time: datetime

    def __lt__(self, other):
        if isinstance(other, Event):
            return self.next_time < other.next_time
        return NotImplemented

    def alert_text(self):
        return Conf.Alert.ALERT_MSG.substitute(
            event_name=self.name,
            next_time=self.next_time,
            time_delta=self.next_time - datetime.now(self.tz),
            final_notice=
            '' if not self.expired else
            ' (FINAL OCCURRENCE)')

    def advance_alert_time(self):
        if not self.expired:
            self.next_time += self.repeat_interval
            if self.next_time < datetime.now(self.tz):
                diff = datetime.now(self.tz) - self.next_time
                multiple = ceil(
                    diff.total_seconds() /
                    self.repeat_interval.total_seconds())
                temp = self.repeat_interval * multiple
                self.next_time += temp
                assert self.next_time > datetime.now(self.tz)

    @property
    def expired(self):
        return self.repeat_interval.total_seconds() == 0

    @property
    def tz(self) -> tzinfo:
        return None if self.next_time is None else self.next_time.tzinfo

    def __str__(self):
        return f'ID: {self.id_}, "{self.name}" every ' \
               f'{self.repeat_interval.days} days. Next occurs at ' \
               f'{self.next_time}'
