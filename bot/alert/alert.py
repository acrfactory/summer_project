import logging
from datetime import datetime, timedelta, timezone
from typing import List

from discord.ext import commands

from bot.alert.event import Event
from bot.common.user_custom import UserCustom
from conf import Conf
from utils.datetime_sup import make_aware
from utils.log import log


class Alert:
    def __init__(self):
        self.lead_time = 60
        self.data: List[Event] = []
        self._next_event = None
        self._next_alert_target = None
        self.next_id = 0
        self.def_tz = Conf.Alert.DEF_TZ

    def create(self, user: UserCustom, repeat_interval: int, name: str,
               next_time: datetime):
        next_time = make_aware(next_time, self.def_tz)
        if repeat_interval < 0:
            raise commands.errors.UserInputError(
                f'Repeat interval must be 0 for once only or greater but '
                f'{repeat_interval} received')
        self.data.append(
            Event(self.get_next_id(), user,
                  timedelta(days=repeat_interval), name,
                  next_time))
        self.find_next_event()

    def remove(self, id_):
        element_to_rem = None
        for event in self.data:
            if event.id_ is id_:
                element_to_rem = event
                break
        if element_to_rem is None:
            raise commands.errors.UserInputError(
                f'No event found with id {id_}')
        else:
            self.data.remove(element_to_rem)
            if element_to_rem == self.next_event:
                self.find_next_event()

    def set_lead_time(self, value: int):
        self.lead_time = value

    def find_next_event(self):
        if len(self.data) <= 0:
            self.next_event = None
        else:
            next_event = self.data[0]
            for event in self.data:
                if event < next_event:
                    next_event = event
            self.next_event = next_event

    async def check_next_event(self, bot) -> bool:
        """
        Checks to see if the next event should be alerted now
        :param bot: handle to the bot to use to send the message
        :return: True if an alert was fired else false
        """
        result = False
        try:
            if self._next_alert_target is not None:
                if datetime.now(self.def_tz) > self._next_alert_target:
                    channel = bot.get_channel(Conf.Alert.ALERT_CHANNEL_ID)
                    await channel.send(self.next_event.alert_text())
                    result = True
                    self.next_event.advance_alert_time()
                    if self.next_event.expired:
                        log(f'Event Expired: {self.next_event}')
                        self.remove(self.next_event.id_)
                    self.find_next_event()
            return result
        except Exception as e:
            log(f'Exception checking next event: {e}', logging.ERROR)
            return False

    def get_next_id(self):
        result = self.next_id
        self.next_id += 1
        return result

    def __str__(self):
        result = f"Bot's time in default timezone is " \
                 f"{datetime.now(self.def_tz)}\n\n"
        if self.next_event is not None:
            time_to_target = self._next_alert_target - datetime.now(
                self.def_tz)
            result += f'Next alert at {self._next_alert_target}' \
                      f' for event ID: {self.next_event.id_}' \
                      f' in {time_to_target}\n\n'
        result += f'Events:\n'
        for event in self.data:
            result += f'- {event}\n'
        result += '---'
        return result

    @property
    def next_event(self):
        return self._next_event

    @next_event.setter
    def next_event(self, value):
        self._next_event = value
        if value is None:
            self._next_alert_target = None
        else:
            self._next_alert_target = self.next_event.next_time \
                                      - timedelta(minutes=self.lead_time)

    def set_def_tz(self, tz_offset_hours, tz_offset_minutes):
        if abs(tz_offset_hours) >= 24:
            raise commands.errors.UserInputError(
                f'Hours must be in range -23 to 23 but {tz_offset_hours} '
                f'received')
        if abs(tz_offset_minutes) >= 60:
            raise commands.errors.UserInputError(
                f'Minutes must be in range -59 to 59 but {tz_offset_minutes} '
                f'received')
        self.def_tz = timezone(
            timedelta(hours=tz_offset_hours, minutes=tz_offset_minutes))
