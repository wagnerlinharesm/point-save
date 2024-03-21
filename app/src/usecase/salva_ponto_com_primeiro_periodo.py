import logging

from datetime import datetime
from app.src.entity.ponto import Ponto
from app.src.entity.periodo_ponto import PeriodoPonto
from app.src.repository.ponto_repository import salvar as salvar_ponto
from app.src.repository.periodo_ponto_repository import salvar as salvar_periodo_ponto

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def execute(id_funcionario, situacao_pontos, conn) -> None:
    situacao = next(filter(lambda situacao_ponto: situacao_ponto.descricao == 'ABERTO', situacao_pontos))

    time_only = datetime.now().time()

    ponto = salvar_ponto(
        Ponto(
            None,
            id_funcionario,
            situacao.id_situacao_ponto,
            datetime.now(),
            time_only
        ),
        conn
    )

    salvar_periodo_ponto(
        PeriodoPonto(
            None,
            ponto.id_ponto,
            time_only,
            None,
            None
        ),
        conn
    )
