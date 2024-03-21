import json
import logging

from datetime import datetime
from app.src.entity.periodo_ponto import PeriodoPonto


def salvar(periodo_ponto, conn):
    logging.info('f=salvar_periodo_ponto, m=iniciando processo para salvar periodo ponto')

    sql = """
    INSERT INTO periodo_ponto (id_ponto, horario_entrada, horario_saida, horas_periodo)
    VALUES (%s, %s, %s, %s)
    """

    cursor = conn.cursor()

    cursor.execute(sql, (periodo_ponto.id_periodo_ponto,
                         periodo_ponto.id_ponto,
                         periodo_ponto.horario_entrada,
                         periodo_ponto.horario_saida,
                         periodo_ponto.horas_periodo,))

    conn.commit()

    logging.info(f'f=salvar_periodo_ponto, m=periodo ponto salvo com sucesso {json.dumps(periodo_ponto.__dict__)}')
    return periodo_ponto


def atualizar(periodo_ponto, conn):
    logging.info('f=atualizar_periodo_ponto, m=iniciando processo para atualizar periodo ponto')

    horas_periodo = (periodo_ponto.horario_saida - periodo_ponto.horario_entrada).total_seconds() / 3600

    sql = """
    UPDATE periodo_ponto
    SET horario_saida = %s, horas_periodo = %s
    WHERE id_periodo_ponto = %s
    """

    cursor = conn.cursor()

    cursor.execute(sql, (periodo_ponto.horario_saida, horas_periodo, periodo_ponto.id_periodo_ponto,))

    conn.commit()

    logging.info(f'f=atualizar_periodo_ponto, m=periodo ponto atualizado com sucesso {json.dumps(periodo_ponto.__dict__)}')


def buscar(id_ponto, conn):
    logging.info('f=buscar_periodo_ponto_aberto, m=inciando a verificação para ver se existe periodo ponto aberto')

    sql = """SELECT * FROM periodo_ponto WHERE id_ponto = %s AND hora_saida is null"""

    cursor = conn.cursor()

    cursor.execute(sql, (id_ponto,))
    periodos_ponto_data = cursor.fetchall()

    if periodos_ponto_data:
        periodo_ponto_data = periodos_ponto_data[0]
        periodo_ponto = PeriodoPonto(
            periodo_ponto_data[0],
            periodo_ponto_data[1],
            periodo_ponto_data[2],
            periodo_ponto_data[3],
            periodo_ponto_data[4]
        )

        logging.info(f'f=buscar_periodo_ponto_aberto, m=periodo ponto encontrado {json.dumps(periodo_ponto.__dict__)}')
        return periodo_ponto

    logging.info(f'f=buscar_periodo_ponto_aberto, m=periodo ponto não encontrado')
    return None


def calcular_horas_trabalhadas(id_ponto, conn):
    sql = """SELECT horario_entrada, horario_saida FROM periodo_ponto WHERE id_ponto = %s AND horario_saida 
    IS NOT NULL"""

    cursor = conn.cursor()

    cursor.execute(sql, (id_ponto,))
    horas_trabalhadas_data = cursor.fetchall()

    total_horas_trabalhadas = 0

    for horas_trabalhada_data in horas_trabalhadas_data:
        horario_entrada = datetime.strptime(horas_trabalhada_data[0], '%H:%M:%S')
        horario_saida = datetime.strptime(horas_trabalhada_data[1], '%H:%M:%S')
        horas_trabalhadas = (horario_saida - horario_entrada).seconds / 3600
        total_horas_trabalhadas += horas_trabalhadas

    return total_horas_trabalhadas
