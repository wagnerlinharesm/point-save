import json
import logging

from datetime import datetime, date
from app.src.entity.periodo_ponto import PeriodoPonto


def salvar(periodo_ponto, conn):
    logging.info('f=salvar_periodo_ponto, m=iniciando processo para salvar periodo ponto')

    sql = """
    INSERT INTO periodo_ponto (id_ponto, hora_entrada, hora_saida, horas_periodo)
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


def atualizar(periodo_ponto, now, conn):
    logging.info('f=atualizar_periodo_ponto, m=iniciando processo para atualizar periodo ponto')

    datetime_entrada = datetime.combine(now, periodo_ponto.horario_entrada)
    datetime_saida = datetime.combine(now, periodo_ponto.horario_saida)

    diferenca = datetime_saida - datetime_entrada

    horas_periodo = (diferenca.seconds // 3600, (diferenca.seconds // 60) % 60, diferenca.seconds % 60)

    sql = """
    UPDATE periodo_ponto
    SET hora_saida = %s, horas_periodo = %s
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


def calcular_horas_trabalhadas(id_ponto, now, conn):
    sql = """SELECT hora_entrada, hora_saida FROM periodo_ponto WHERE id_ponto = %s AND hora_saida 
    IS NOT NULL"""

    cursor = conn.cursor()

    cursor.execute(sql, (id_ponto,))
    horas_trabalhadas_data = cursor.fetchall()

    total_horas_trabalhadas = None

    for horas_trabalhada_data in horas_trabalhadas_data:
        datetime_entrada = datetime.combine(now, horas_trabalhada_data[0])
        datetime_saida = datetime.combine(now, horas_trabalhada_data[1])

        diferenca = datetime_saida - datetime_entrada

        horas_periodo = (diferenca.seconds // 3600, (diferenca.seconds // 60) % 60, diferenca.seconds % 60)

        if total_horas_trabalhadas is None:
            total_horas_trabalhadas = horas_periodo
        else:
            total_horas_trabalhadas = (
                total_horas_trabalhadas[0] + horas_periodo[0],
                total_horas_trabalhadas[1] + horas_periodo[1],
                total_horas_trabalhadas[2] + horas_periodo[2]
            )

    return total_horas_trabalhadas
