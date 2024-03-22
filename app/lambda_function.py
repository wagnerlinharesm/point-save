import logging
import os
from datetime import datetime

import pytz

from app.src.core.usecase.punch_clock_use_case import PunchClockUseCase
from app.src.util.jwt_util import JwtUtil

logger = logging.getLogger()
logger.setLevel(logging.INFO)

host = os.getenv('DB_HOST')
dbname = os.getenv('DB_NAME')
username = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')

now = datetime.now(pytz.timezone('America/Sao_Paulo'))


def handler(event, context):
    logging.info('Iniciando a execução da função lambda')

    employee_id = get_username(event)

    punch_clock_use_case = PunchClockUseCase()

    try:
        punch_clock_use_case.execute(employee_id, now)
    except Exception as e:
        logging.error(f'Erro ao salvar ponto: {e}')
        return {"result": "Erro ao salvar ponto"}

    return {"result": "Ponto salvo com sucesso"}


def get_username(event):
    jwt_token = get_jwt_token(event)
    jwt_util = JwtUtil(jwt_token)

    return jwt_util.get_required_attribute("cognito:username")


def get_jwt_token(event):
    authorization = event['headers'].get('Authorization')
    split_authorization = authorization.split()

    if len(split_authorization) == 1:
        return split_authorization[0]
    elif len(split_authorization) == 2:
        return split_authorization[1]

    raise Exception("invalid authorization.")