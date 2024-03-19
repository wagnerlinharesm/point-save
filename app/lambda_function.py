import os
import boto3

from datetime import date
from datetime import datetime

RDS_ARN = os.environ.get('RDS_ARN')
SECRET_RDS = os.environ.get('SECRET_RDS')
DATABASE_NAME = os.environ.get('DATABASE_NAME')


def handler(event, context):
    id_funcionario = event['id_funcionario']

    # Buscar o Ponto no RDS
    ponto = buscar_ponto(id_funcionario, date.today())
    situacao_pontos = busca_situacao_pontos()

    if not ponto:
        situacao_ponto_aberto = next(
            filter(lambda situacao_ponto: situacao_ponto.descricao == 'ABERTO', situacao_pontos)
        )
        ponto = Ponto(None, id_funcionario, situacao_ponto_aberto.id_situacao_ponto, datetime.now(), None)
        salvar_ponto(ponto)
    else:
        periodo_ponto = buscar_periodo_ponto_aberto(ponto.id_ponto)

        if periodo_ponto:
            periodo_ponto.horario_saida = datetime.now()
            atualizar_periodo_ponto(periodo_ponto)
        else:
            periodo_ponto = PeriodoPonto(None, ponto.id_ponto, datetime.now(), None, 0)
            salvar_periodo_ponto(periodo_ponto)

        ponto.horas_trabalhadas += calcular_horas_trabalhadas(periodo_ponto)
        atualizar_ponto(ponto)

    return event


def buscar_ponto(id_funcionario, data):
    rds = boto3.client('rds-data')

    data_formatada = data.strftime('%Y-%m-%d')

    sql = f"SELECT * FROM ponto WHERE id_funcionario = {id_funcionario} AND data = '{data_formatada}'"

    response = rds.execute_statement(
        resourceArn=RDS_ARN,
        secretArn=SECRET_RDS,
        database=DATABASE_NAME,
        sql=sql
    )

    if response['records']:
        ponto_data = response['records'][0]
        ponto = Ponto(ponto_data[0], ponto_data[1], ponto_data[2], ponto_data[3], ponto_data[4])
        return ponto

    return None


def busca_situacao_pontos():
    rds = boto3.client('rds-data')

    sql = f"SELECT * FROM situacao_ponto"

    response = rds.execute_statement(
        resourceArn=RDS_ARN,
        secretArn=SECRET_RDS,
        database=DATABASE_NAME,
        sql=sql
    )

    if response['records']:
        situacao_pontos = []

        for situacao_ponto_data in response['records']:
            situacao_ponto = SituacaoPonto(situacao_ponto_data[0], situacao_ponto_data[1])
            situacao_pontos.append(situacao_ponto)

        return situacao_pontos

    return None


def buscar_periodo_ponto_aberto(id_ponto):
    rds = boto3.client('rds-data')

    sql = f"SELECT * FROM periodo_ponto WHERE id_ponto = {id_ponto} AND hora_saida is null"

    response = rds.execute_statement(
        resourceArn=RDS_ARN,
        secretArn=SECRET_RDS,
        database=DATABASE_NAME,
        sql=sql
    )

    if response['records']:
        periodo_ponto_data = response['records'][0]
        periodo_ponto = PeriodoPonto(
            periodo_ponto_data[0],
            periodo_ponto_data[1],
            periodo_ponto_data[2],
            periodo_ponto_data[3],
            periodo_ponto_data[4]
        )
        return periodo_ponto

    return None


def salvar_ponto(ponto):
    rds = boto3.client('rds-data')

    data_formatada = ponto.data.strftime('%Y-%m-%d')

    sql = f"""
    INSERT INTO ponto (id_funcionario, id_situacao_ponto, data, horas_trabalhadas)
    VALUES ({ponto.id_funcionario}, {ponto.id_situacao_ponto}, '{data_formatada}', {ponto.horas_trabalhadas})
    """

    response = rds.execute_statement(
        resourceArn=RDS_ARN,
        secretArn=SECRET_RDS,
        database=DATABASE_NAME,
        sql=sql
    )

    ponto.id_ponto = response['generatedFields'][0]['longValue']

    return ponto


def salvar_periodo_ponto(periodo_ponto):
    rds = boto3.client('rds-data')

    sql = f"""
    INSERT INTO periodo_ponto (id_periodo_ponto, id_ponto, horario_entrada, horario_saida, horas_periodo)
    VALUES ({periodo_ponto.id_periodo_ponto}, {periodo_ponto.id_ponto}, '{periodo_ponto.horario_entrada}', {periodo_ponto.horario_saida}, {periodo_ponto.horas_periodo})
    """

    response = rds.execute_statement(
        resourceArn=RDS_ARN,
        secretArn=SECRET_RDS,
        database=DATABASE_NAME,
        sql=sql
    )

    periodo_ponto.id_periodo_ponto = response['generatedFields'][0]['longValue']

    return periodo_ponto


def atualizar_periodo_ponto(periodo_ponto):
    rds = boto3.client('rds-data')

    horas_periodo = (periodo_ponto.horario_saida - periodo_ponto.horario_entrada).total_seconds() / 3600

    sql = f"""
    UPDATE periodo_ponto
    SET horario_saida = {periodo_ponto.horario_saida}, horas_periodo = {horas_periodo}
    WHERE id_periodo_ponto = {periodo_ponto.id_periodo_ponto}
    """

    rds.execute_statement(
        resourceArn=RDS_ARN,
        secretArn=SECRET_RDS,
        database=DATABASE_NAME,
        sql=sql
    )


def calcular_horas_trabalhadas(id_ponto):
    rds = boto3.client('rds-data')

    sql = f"SELECT horario_entrada, horario_saida FROM periodo_ponto WHERE id_ponto = {id_ponto} AND horario_saida IS NOT NULL"

    response = rds.execute_statement(
        resourceArn=RDS_ARN,
        secretArn=SECRET_RDS,
        database=DATABASE_NAME,
        sql=sql
    )

    total_horas_trabalhadas = 0

    for record in response['records']:
        horario_entrada = datetime.strptime(record[0], '%H:%M:%S')
        horario_saida = datetime.strptime(record[1], '%H:%M:%S')
        horas_trabalhadas = (horario_saida - horario_entrada).seconds / 3600
        total_horas_trabalhadas += horas_trabalhadas

    return total_horas_trabalhadas


def atualizar_ponto(ponto):
    rds = boto3.client('rds-data')

    sql = f"""
    UPDATE ponto
    SET horas_trabalhadas = {ponto.horas_trabalhadas}
    WHERE id_ponto = {ponto.id_ponto}
    """

    rds.execute_statement(
        resourceArn=RDS_ARN,
        secretArn=SECRET_RDS,
        database=DATABASE_NAME,
        sql=sql
    )


class Ponto:
    def __init__(self, id_ponto, id_funcionario, id_situacao_ponto, data, horas_trabalhadas):
        self.id_ponto = id_ponto
        self.id_funcionario = id_funcionario
        self.id_situacao_ponto = id_situacao_ponto
        self.data = data
        self.horas_trabalhadas = horas_trabalhadas


class SituacaoPonto:
    def __init__(self, id_situacao_ponto, descricao):
        self.id_situacao_ponto = id_situacao_ponto
        self.descricao = descricao


class PeriodoPonto:
    def __init__(self, id_periodo_ponto, id_ponto, horario_entrada, horario_saida, horas_periodo):
        self.id_periodo_ponto = id_periodo_ponto
        self.id_ponto = id_ponto
        self.horario_entrada = horario_entrada
        self.horario_saida = horario_saida
        self.horas_periodo = horas_periodo
