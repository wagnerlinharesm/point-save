import json
import logging

from app.src.entity.situacao_ponto import SituacaoPonto


def buscar(conn):
    logging.info('f=busca_situacao_pontos, m=inciando a busca das situações')

    sql = """SELECT * FROM situacao_ponto"""

    cursor = conn.cursor()

    cursor.execute(sql)
    situacoes_ponto_data = cursor.fetchall()

    if situacoes_ponto_data:
        situacao_pontos = []

        for situacao_ponto_data in situacoes_ponto_data:
            situacao_ponto = SituacaoPonto(situacao_ponto_data[0], situacao_ponto_data[1])
            situacao_pontos.append(situacao_ponto)

        logging.info(f'f=busca_situacao_pontos, m=situações encontradas {json.dumps(situacao_pontos)}')
        return situacao_pontos

    logging.info(f'f=busca_situacao_pontos, m=situações não encontradas')
    return None
