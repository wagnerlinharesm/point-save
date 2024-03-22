import logging

from app.src.adapter.helper.database_helper import DatabaseHelper
from app.src.core.domain.point_period import PointPeriod
from app.src.util.singleton_meta import SingletonMeta


class PointPeriodAdapter(metaclass=SingletonMeta):
    _db_helper = DatabaseHelper()

    def fetch_one(self, point_id):
        query = """SELECT * FROM periodo_ponto WHERE id_ponto = %s AND hora_saida is null"""

        row_dict = self._db_helper.fetch_one(query, (point_id,))

        if row_dict is None:
            return None

        point_period = PointPeriod(
            row_dict['id_periodo_ponto'],
            row_dict['id_ponto'],
            row_dict['hora_entrada'],
            row_dict['hora_saida'],
            row_dict['horas_periodo']
        )

        return point_period

    def fetch_all(self, point_id):

        query = """
                    SELECT * 
                    FROM periodo_ponto 
                    WHERE id_ponto = %s 
                    AND hora_saida IS NOT NULL
                """

        rows_dict = self._db_helper.fetch_all(query, (point_id,))

        point_periods = []

        for row_dict in rows_dict:
            point_period = PointPeriod(
                row_dict['id_periodo_ponto'],
                row_dict['id_ponto'],
                row_dict['hora_entrada'],
                row_dict['hora_saida'],
                row_dict['horas_periodo']
            )

            point_periods.append(point_period)

        return point_periods

    def save(self, point_period):
        query = """
            INSERT INTO periodo_ponto (id_ponto, hora_entrada, hora_saida, horas_periodo)
            VALUES (%s, %s, %s, %s)
            """

        self._db_helper.insert_or_update(query, (
            point_period.point_id,
            point_period.begin_time,
            point_period.end_time,
            point_period.work_time,))


    def update(self, point_period):
        query = """
                UPDATE periodo_ponto
                SET hora_saida = %s, horas_periodo = %s
                WHERE id_periodo_ponto = %s
            """

        self._db_helper.insert_or_update(query, (
            point_period.end_time,
            point_period.work_time,
            point_period.point_period_id,))
