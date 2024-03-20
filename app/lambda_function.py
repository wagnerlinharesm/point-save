import logging
import os

import psycopg2

from app.src.repository.ponto_repository import (
    buscar as buscar_ponto,
)
from app.src.repository.situacao_ponto_repository import buscar as busca_situacao_pontos
from app.src.usecase.salva_ou_atualiza_periodo_pedido import execute as salva_ou_atualiza_periodo_pedido
from app.src.usecase.salva_ponto_com_primeiro_periodo import execute as salva_ponto_com_primeiro_periodo

logger = logging.getLogger()
logger.setLevel(logging.INFO)

host = os.getenv('DB_HOST')
dbname = os.getenv('DB_NAME')
username = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')


def handler(event, context):
    logging.info('Iniciando a execução da função lambda.')

    id_funcionario = event['id_funcionario']

    conn = connection()

    try:
        ponto = buscar_ponto(id_funcionario, conn)
        situacao_pontos = busca_situacao_pontos(conn)

        if not ponto:
            salva_ponto_com_primeiro_periodo(id_funcionario, situacao_pontos, conn)
        else:
            salva_ou_atualiza_periodo_pedido(ponto.id_ponto, conn)

        conn.cursor().close()
        conn.close()
    except Exception as e:
        logging.error(f'Erro ao salvar ponto: {e}')
        return {"result": "Erro ao salvar ponto."}

    return {"result": "Ponto salvo com sucesso."}


def connection():
    config = {
        'dbname': dbname,
        'user': username,
        'password': password,
        'host': host
    }
    return psycopg2.connect(**config)
