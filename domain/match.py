import datetime as _dt
import typing as _t
import zoneinfo as _zi

import core.match as _c_match


class Match:
    """All services use this class to store match data"""

    def __init__(
        self,
        sport: str,
        home: str,
        away: str,
        start: _t.Union[str, _dt.datetime],
        league: str,
        details: str = "",
        id=None,
    ):
        self.id = id
        self.sport = sport
        self.league = league
        self.sport_abr = "FOT" if self.sport == "football" else self.league
        self.home = home
        self.away = away
        self.start = self.format_date(start)
        self.details = details

        self.date = self.start.date()
        self.time = f"{self.start.time().hour}:{self.start.time().minute}"
        self.day_of_week = self.start.strftime("%a").upper()

        now = _dt.datetime.now()
        now_date, start_date = now.date(), self.start.date()
        current_week_start = now_date - _dt.timedelta(days=now.weekday())
        current_week_end = current_week_start + _dt.timedelta(days=6)
        next_week_start = current_week_end + _dt.timedelta(days=1)
        next_week_end = current_week_end + _dt.timedelta(days=6)

        self.in_current_week = current_week_start <= start_date <= current_week_end
        self.in_next_week = next_week_start <= start_date <= next_week_end
        self.in_next_7_days = now_date <= start_date <= now_date + _dt.timedelta(7)
        self.in_next_15_days = now_date <= start_date <= now_date + _dt.timedelta(15)

        self.is_old = now_date > start_date
        self.is_recent = True if self.in_current_week or self.in_next_week else False
        self.is_later = start_date > next_week_end

    def meets_time_frame(self, time_frame: str = "all"):
        """Checks if the match meets the requested time frame

        Args
            time_frame(str): one of 'old, this week, next_week, later'
                             also accepts 'recent' = 'this_week' + 'next_week'
                             and 'all' = 'old' + 'this week' + 'next_week' + 'later'
        """
        if time_frame == "all":
            return True
        if time_frame == "old":
            return self.is_old
        if time_frame == "this_week":
            return self.in_current_week and not self.is_old
        if time_frame == "next_week":
            return self.in_next_week
        if time_frame == "recent":
            return (self.in_next_week or self.in_current_week) and not self.is_old
        if time_frame == "later":
            return self.is_later
        return True

    def __str__(self) -> str:
        return f"{self.home} vs {self.away} at {self.start}"

    @staticmethod
    def format_date(date: str | _dt.datetime) -> _dt.datetime:
        """Converts date to expected format"""
        if isinstance(date, str):
            date.replace("Z", "+00:00")
            date = _dt.datetime.fromisoformat(date)
        local_timezone = _zi.ZoneInfo("America/New_York")
        return date.astimezone(local_timezone)

    def get_match_card(self, show_time_label=False):
        time_label = ""
        if show_time_label:
            if self.in_current_week:
                time_label = "--next"
            elif self.in_next_week:
                time_label = "--next_week"
            elif self.is_old:
                time_label = "--is_old"
            else:
                time_label = "--later ->"
        return f"{time_label} {self.day_of_week} -> {self}, ({self.sport_abr})"

    @classmethod
    def from_entity(cls, entity):
        """Convert from core Match (SQLAlchemy model) to domain model."""
        return cls(
            id=entity.id,
            sport=entity.sport,
            league=entity.league,
            home=entity.home,
            away=entity.away,
            start=entity.start,
            details=entity.details,
        )

    def to_entity(self):
        """Convert from domain model to core Match (SQLAlchemy model)."""
        return _c_match.Match(
            sport=self.sport,
            league=self.league,
            home=self.home,
            away=self.away,
            start=self.start,
            details=self.details,
        )

    def save(self, db):
        self.to_entity().save(db)

    @staticmethod
    def delete_all(db):
        _c_match.Match.delete_all(db)
