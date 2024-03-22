import logging

from app.src.adapter.helper.database_helper import DatabaseHelper
from app.src.core.domain.point_period import PointPeriod
from app.src.util.singleton_meta import SingletonMeta


class PointPeriodAdapter(metaclass=SingletonMeta):
    _db_helper = DatabaseHelper()

    def fetch_one(self, point_id):
        logging.info('f=buscar_ponto_periodo_aberto, m=inciando a verificação para ver se existe ponto periodo aberto')

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

        logging.info('f=buscar_periodo_ponto_aberto, m=ponto periodo encontrado')

        return point_period

    def fetch_all(self, point_id):
        logging.info('f=buscar_ponto_periodos, m=inciando a busca dos pontos periodos')

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

        logging.info('f=buscar_ponto_periodos, m=pontos periodos encontrados')

        return point_periods

    def save(self, point_period):
        logging.info('f=salvar_ponto_periodo, m=iniciando processo para salvar ponto periodo')

        query = """
            INSERT INTO periodo_ponto (id_ponto, hora_entrada, hora_saida, horas_periodo)
            VALUES (%s, %s, %s, %s)
            """

        logging.info(f'point_period_id={point_period.point_period_id}, point_id={point_period.point_id}, begin_time={point_period.begin_time}, end_time={point_period.end_time}, work_time={point_period.work_time}')

        self._db_helper.insert_or_update(query, (
            point_period.point_id,
            point_period.begin_time,
            point_period.end_time,
            point_period.work_time,))

        logging.info(f'f=salvar_ponto_periodo, m=ponto periodo salvo com sucesso')

    def update(self, end_time, work_time, point_period_id):
        logging.info('f=atualizar_ponto_periodo, m=iniciando processo para atualizar ponto periodo')

        logging.info(
            f'end_time={end_time}, work_time={work_time}, point_period_id={point_period_id}')

        query = """
                UPDATE periodo_ponto
                SET hora_saida = %s, horas_periodo = %s
                WHERE id_periodo_ponto = %s
            """

        self._db_helper.insert_or_update(query, (
            end_time,
            work_time,
            point_period_id,))

        logging.info(f'f=atualizar_ponto_periodo, m=ponto periodo atualizado com sucesso')
