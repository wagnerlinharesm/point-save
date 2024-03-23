from datetime import datetime, time

from app.src.adapter.point_adapter import PointAdapter
from app.src.adapter.point_period_adapter import PointPeriodAdapter
from app.src.util.singleton_meta import SingletonMeta
from app.src.core.domain.point_period import PointPeriod


class SaveOrUpdatePointPeriodUseCase(metaclass=SingletonMeta):
    _point_adapter = PointAdapter()
    _point_period_adapter = PointPeriodAdapter()

    def execute(self, point, situations, now):
        point_period = self._point_period_adapter.fetch_one(point.point_id)

        if point_period:
            situation = next(filter(lambda element: element.description == 'FECHADO', situations))
            point_period.end_time = now.time()
            point_period.work_time = self.get_work_time(point_period, now)
            self._point_period_adapter.update(point_period)
        else:
            situation = next(filter(lambda element: element.description == 'ABERTO', situations))
            point_period = PointPeriod(
                None,
                point.point_id,
                now.time(),
                None,
                time(0, 0, 0)
            )

            self._point_period_adapter.save(point_period)

        total_work_time = self.get_total_work_time(point_period, point.work_time)
        self._point_adapter.update(point.point_id, situation.situation_id, total_work_time)

    def get_total_work_time(self, point_period, point_work_time):
        point_periods = self._point_period_adapter.fetch_all(point_period.point_id)

        total_work_time = None

        for point_period in point_periods:
            if total_work_time is None:
                total_work_time = point_work_time
            else:
                total_work_time = self.sum_times(total_work_time, point_period.work_time)

        return total_work_time

    def get_work_time(self, point_period, now):
        entry_date = datetime.combine(now, point_period.begin_time)
        exit_date = datetime.combine(now, point_period.end_time)

        date_diff = exit_date - entry_date

        time2 = self.timedelta_to_time(date_diff)

        return time2

    def timedelta_to_time(self, delta):
        total_seconds = int(delta.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return time(hours, minutes, seconds)

    def sum_times(self, start_time, final_time):
        total_seconds = (start_time.hour + final_time.hour) * 3600 + \
                         (start_time.minute + final_time.minute) * 60 + \
                         start_time.second + final_time.second

        result_hours, resto = divmod(total_seconds, 3600)

        result_minutes, result_seconds = divmod(resto, 60)

        return time(result_hours, result_minutes, result_seconds)
