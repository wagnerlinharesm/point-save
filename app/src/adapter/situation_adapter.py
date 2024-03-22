import logging

from app.src.adapter.helper.database_helper import DatabaseHelper
from app.src.core.domain.situation import Situation
from app.src.util.singleton_meta import SingletonMeta


class SituationAdapter(metaclass=SingletonMeta):
    _db_helper = DatabaseHelper()

    def fetch_all(self):
        query = """SELECT * FROM situacao_ponto"""

        rows_dict = self._db_helper.fetch_all(query)

        situations = []

        for row_dict in rows_dict:
            situation = Situation(
                row_dict['id_situacao_ponto'],
                row_dict['situacao']
            )

            situations.append(situation)

        return situations
