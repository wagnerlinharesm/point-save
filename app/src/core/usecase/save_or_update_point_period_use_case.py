import logging
from datetime import datetime, time

from app.src.adapter.point_adapter import PointAdapter
from app.src.adapter.point_period_adapter import PointPeriodAdapter
from app.src.util.singleton_meta import SingletonMeta
from app.src.core.domain.point_period import PointPeriod


class SaveOrUpdatePointPeriodUseCase(metaclass=SingletonMeta):
    _point_adapter = PointAdapter()
    _point_period_adapter = PointPeriodAdapter()

    def execute(self, point, situations, now, time_now):
        point_period = self._point_period_adapter.fetch_one(point.point_id)

        if point_period:
            situation = next(filter(lambda element: element.description == 'FECHADO', situations))
            point_period.work_time = self.get_work_time(point_period.begin_time, time_now, now)

            logging.info(f'begin_time: {point_period.begin_time}, end_time: {point_period.end_time}')

            self._point_period_adapter.update(point_period, time_now)
        else:
            situation = next(filter(lambda element: element.description == 'ABERTO', situations))
            point_period = PointPeriod(
                None,
                point.point_id,
                time_now,
                None,
                time(0, 0, 0)
            )

            self._point_period_adapter.save(point_period)

        self._point_adapter.update(point.point_id, situation.situation_id)

    def get_work_time(self, begin_time, end_time, now):
        logging.info(f'begin_time: {begin_time}')
        logging.info(f'end_time: {end_time}')

        entry_date = datetime.combine(now, begin_time)
        exit_date = datetime.combine(now, end_time)

        date_diff = exit_date - entry_date

        time2 = self.timedelta_to_time(date_diff)

        logging.info(f'time2: {time2}')

        return time2

    def timedelta_to_time(self, delta):
        total_seconds = int(delta.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return time(hours, minutes, seconds)
