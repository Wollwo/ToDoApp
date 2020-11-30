from datetime import datetime
import calendar


class GetCurrentDatetime:
    def __init__(self):
        self.today = datetime.now()
        self.week_num = self.today.date().isocalendar()[1]
        self.time_now = self.today.time().strftime("%H:%M:%S")

        self.current_weekday = calendar.day_name[self.today.weekday()].upper()[0:3]
        self.current_year = self.today.date().strftime("%Y")
        self.current_month = self.today.date().strftime("%m")
        self.current_day = self.today.date().strftime("%d")
        self.current_week = self.week_num

        self.current_hour = self.today.time().strftime("%H")
        self.current_min = self.today.time().strftime("%M")
        self.current_sec = self.today.time().strftime("%S")

        self.current_full_date = f"{self.current_week} {self.current_weekday} {self.current_year}.{self.current_month}.{self.current_day}"
        self.current_full_time = f"{self.current_hour}:{self.current_min}:{self.current_sec}"
        self.current_full_datetime = f"{self.current_full_date} {self.current_full_time}"

    def get_fullcurrent_time(self):
        return self.current_full_time

    def get_fullcurrent_date(self):
        return self.current_full_date

    def get_fullcurrent_datetime(self):
        return self.current_full_datetime

    def get_compact_datetime(self):
        return f"{self.current_year}{self.current_month}{self.current_day}{self.current_hour}{self.current_min}{self.current_sec}"
