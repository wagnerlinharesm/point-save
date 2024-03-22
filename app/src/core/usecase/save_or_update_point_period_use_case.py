import logging

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
            point_period.work_time = self.add_times(now, point_period.begin_time, point_period.end_time)
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

        total_work_time = self.get_total_work_time(point_period, point.work_time, now)
        self._point_adapter.update(point.point_id, situation.situation_id, total_work_time)

    def get_total_work_time(self, point_period, point_work_time, now):
        point_periods = self._point_period_adapter.fetch_all(point_period.point_id)

        total_work_time = None

        logging.info(f'f=get_work_time, point_periods={point_periods}')

        for point_period in point_periods:
            logging.info(f'f=get_work_time, point_period_id={point_period.point_id}, end_time={point_period.end_time}')

            logging.info(f'f=add_times, work_time={point_period.work_time}')

            if total_work_time is None:
                total_work_time = point_work_time
            else:
                total_work_time = self.add_times(now, point_period.work_time, total_work_time)

            logging.info(f'f=add_times, total_work_time={total_work_time}')

        return total_work_time

    def get_work_time(self, point_period, now):

        logging.info(
            f'f=get_work_time, begin_time={point_period.begin_time}, end_time={point_period.end_time}, now={now} .')

        entry_date = datetime.combine(now, point_period.begin_time)
        exit_date = datetime.combine(now, point_period.end_time)

        date_diff = exit_date - entry_date

        logging.info(f'f=get_work_time, date_diff={date_diff}.')

        time2 = time(date_diff.seconds // 3600, (date_diff.seconds // 60) % 60, date_diff.seconds % 60)

        logging.info(f'f=get_work_time, time2={time2}.')

        return time2

    def add_times(self, now, first_time, second_time):
        first_datetime = datetime.combine(now, first_time)
        second_datetime = datetime.combine(now, second_time)

        difference_time = ((second_datetime - datetime(1970, 1, 1)) +
                           (first_datetime - datetime(1970, 1, 1)))

        return (datetime(1970, 1, 1) + difference_time).time()
