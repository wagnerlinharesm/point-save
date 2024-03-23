import logging

from app.src.adapter.helper.database_helper import DatabaseHelper
from app.src.util.singleton_meta import SingletonMeta
from app.src.core.domain.point import Point


class PointAdapter(metaclass=SingletonMeta):
    _db_helper = DatabaseHelper()

    def fetch_one(self, employee_id, date):
        query = """
                    SELECT * FROM ponto WHERE id_funcionario = %s AND data = %s
                    """

        row_dict = self._db_helper.fetch_one(query, (employee_id, date,))

        if row_dict is None:
            return None

        point = Point(
            row_dict['id_ponto'],
            row_dict['id_funcionario'],
            row_dict['id_situacao_ponto'],
            row_dict['data'],
            row_dict['horas_trabalhadas']
        )

        return point

    def save(self, point):
        query = """
                    INSERT INTO ponto (id_funcionario, id_situacao_ponto, data, horas_trabalhadas)
                    VALUES (%s, %s, %s, %s)
                """

        self._db_helper.insert_or_update(query, (
            point.employee_id,
            point.situation_id,
            point.date,
            point.work_time,))

    def update(self, point_id, situation_id):
        query_sum = """
                                    SELECT sum(horas_periodo) as worktime
                                    FROM periodo_ponto pp
                                    WHERE id_ponto = %s;
                                """

        row_dict = self._db_helper.fetch_one(query_sum, (point_id,))

        query = """
                UPDATE ponto
                SET horas_trabalhadas = %s, id_situacao_ponto = %s
                WHERE id_ponto = %s
                """

        self._db_helper.insert_or_update(query, (row_dict['worktime'], situation_id, point_id,))
