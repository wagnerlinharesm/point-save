import logging

from datetime import datetime
from app.src.entity.ponto import Ponto


def salvar(ponto, conn):
    logging.info('f=salvar_ponto, m=iniciando processo para salvar ponto.')

    data_formatada = ponto.data.strftime('%Y-%m-%d')

    sql_insert = """
    INSERT INTO ponto (id_funcionario, id_situacao_ponto, data, horas_trabalhadas)
    VALUES (%s, %s, %s, %s)
    """

    sql_select = """
    SELECT * FROM ponto WHERE id_funcionario = %s AND data = %s
    """

    cursor = conn.cursor()

    cursor.execute(sql_insert, (ponto.id_funcionario, ponto.id_situacao_ponto, data_formatada, ponto.horas_trabalhadas))

    conn.commit()

    cursor.execute(sql_select, (ponto.id_funcionario, data_formatada,))
    ponto_data = cursor.fetchone()
    ponto.id_ponto = ponto_data[0]

    logging.info(f'f=salvar_ponto, m=ponto salvo com sucesso {ponto}.')
    return ponto


def atualizar(id_ponto, horas_trabalhadas, conn):
    logging.info('f=atualizar_ponto, m=iniciando processo para atualizar ponto.')

    sql = """
    UPDATE ponto
    SET horas_trabalhadas = %s
    WHERE id_ponto = %S
    """

    cursor = conn.cursor()

    cursor.execute(sql, (horas_trabalhadas,id_ponto,))

    conn.commit()

    logging.info(f'f=atualizar_ponto, m=ponto atualizado com sucesso.')


def buscar(id_funcionario, conn):
    logging.info('f=buscar_ponto, m=inciando a verificação para ver se existe ponto já criado.')

    data_formatada = datetime.now().strftime('%Y-%m-%d')

    sql = """SELECT * FROM ponto WHERE id_funcionario = %s AND data = %s"""

    cursor = conn.cursor()

    cursor.execute(sql, (id_funcionario, data_formatada,))
    ponto_data = cursor.fetchone()

    if ponto_data:
        ponto = Ponto(ponto_data[0], ponto_data[1], ponto_data[2], ponto_data[3], ponto_data[4])

        logging.info(f'f=buscar_ponto, m=ponto encontrado {ponto}.')

        return ponto

    logging.info(f'f=buscar_ponto, m=ponto não encontrado.')
    return None
