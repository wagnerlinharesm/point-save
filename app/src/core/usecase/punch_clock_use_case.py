from app.src.adapter.point_adapter import PointAdapter
from app.src.adapter.point_period_adapter import PointPeriodAdapter
from app.src.adapter.situation_adapter import SituationAdapter
from app.src.core.usecase.save_or_update_point_period_use_case import SaveOrUpdatePointPeriodUseCase
from app.src.core.usecase.save_point_with_first_period_use_case import SavePointWithFirstPeriodUseCase
from app.src.util.singleton_meta import SingletonMeta


class PunchClockUseCase(metaclass=SingletonMeta):
    _point_adapter = PointAdapter()
    _situation_adapter = SituationAdapter()
    _point_period_adapter = PointPeriodAdapter()

    _save_point_with_first_period_use_case = SavePointWithFirstPeriodUseCase()
    _save_or_update_point_period_use_case = SaveOrUpdatePointPeriodUseCase()

    def execute(self, employee_id, now):
        situations = self._situation_adapter.fetch_all()
        point = self._point_adapter.fetch_one(employee_id, now)

        if not point:
            self._save_point_with_first_period_use_case.execute(employee_id, situations, now)
        else:
            self._save_or_update_point_period_use_case.execute(point.id_ponto, situations, now)
