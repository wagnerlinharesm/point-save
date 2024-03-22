from datetime import datetime, time

from app.src.adapter.point_adapter import PointAdapter
from app.src.adapter.point_period_adapter import PointPeriodAdapter
from app.src.util.singleton_meta import SingletonMeta
from app.src.core.domain.point_period import PointPeriod


class SaveOrUpdatePointPeriodUseCase(metaclass=SingletonMeta):

    _point_adapter = PointAdapter()
    _point_period_adapter = PointPeriodAdapter()

    def execute(self, point_id, situations, now):
        point_period = self._point_period_adapter.fetch_one(point_id)

        if point_period:
            situation = next(filter(lambda element: element.description == 'FECHADO', situations))
            point_period.end_time = now.time()
            point_period.work_time = self.get_work_time(point_period, now)
            self._point_period_adapter.update(point_period.end_time, point_period.work_time, situation.situation_id)
        else:
            situation = next(filter(lambda element: element.description == 'ABERTO', situations))
            self._point_period_adapter.save(
                PointPeriod(
                    None,
                    point_id,
                    now.time(),
                    None,
                    time(0, 0, 0)
                )
            )

        total_work_time = self.get_total_work_time(point_period, now)
        self._point_period_adapter.update(point_id, total_work_time, situation.situation_id)

    def get_total_work_time(self, point_period, now):
        point_periods = self._point_period_adapter.fetch_all(point_period.point_id)

        total_work_time = None

        for point_period in point_periods:
            if point_period.end_time is not None:

                work_time = self.get_work_time(point_period, now)

                if total_work_time is None:
                    total_work_time = work_time
                else:
                    total_work_time = time(
                        total_work_time[0] + work_time[0],
                        total_work_time[1] + work_time[1],
                        total_work_time[2] + work_time[2]
                    )

        return total_work_time

    def get_work_time(self, point_period, now):
        entry_date = datetime.combine(now, point_period.begin_time)
        exit_date = datetime.combine(now, point_period.end_time)

        date_diff = exit_date - entry_date

        return time(date_diff.seconds // 3600, (date_diff.seconds // 60) % 60, date_diff.seconds % 60)
