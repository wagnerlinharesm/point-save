import logging

from datetime import time

from app.src.adapter.point_adapter import PointAdapter
from app.src.adapter.point_period_adapter import PointPeriodAdapter
from app.src.core.domain.point import Point
from app.src.core.domain.point_period import PointPeriod
from app.src.util.singleton_meta import SingletonMeta

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class SavePointWithFirstPeriodUseCase(metaclass=SingletonMeta):
    _point_adapter = PointAdapter()
    _point_period_adapter = PointPeriodAdapter()

    def execute(self, employee_id, situations, now) -> None:
        situation = next(filter(lambda element: element.description == 'ABERTO', situations))

        logging.info('situations: %s', situations)

        init_time = time(0, 0, 0)
        formatted_date = now.strftime('%Y-%m-%d')

        self._point_adapter.save(
            Point(
                None,
                employee_id,
                situation.id_situation_point,
                formatted_date,
                init_time
            )
        )

        point = self._point_adapter.fetch_one(employee_id, formatted_date)

        self._point_period_adapter.save(
            PointPeriod(
                None,
                point.id_ponto,
                now.time(),
                None,
                init_time
            )
        )
