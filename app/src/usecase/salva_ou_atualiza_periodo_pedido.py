from datetime import datetime

from app.src.entity.periodo_ponto import PeriodoPonto
from app.src.repository.periodo_ponto_repository import (
    buscar as buscar_periodo_ponto_aberto,
    salvar as salvar_periodo_ponto,
    atualizar as atualizar_periodo_ponto,
    calcular_horas_trabalhadas
)
from app.src.repository.ponto_repository import atualizar as atualizar_ponto


def execute(id_ponto, situacao_pontos, conn) -> None:
    periodo_ponto = buscar_periodo_ponto_aberto(id_ponto, conn)

    if periodo_ponto:
        situacao = next(filter(lambda situacao_ponto: situacao_ponto.descricao == 'FECHADO', situacao_pontos))
        periodo_ponto.horario_saida = datetime.now()
        atualizar_periodo_ponto(periodo_ponto, conn)
    else:
        situacao = next(filter(lambda situacao_ponto: situacao_ponto.descricao == 'ABERTO', situacao_pontos))
        salvar_periodo_ponto(
            PeriodoPonto(
                None,
                id_ponto,
                datetime.now(),
                None,
                0
            ),
            conn
        )

    horas_trabalhadas = calcular_horas_trabalhadas(id_ponto, conn)
    atualizar_ponto(id_ponto, horas_trabalhadas, situacao.id_situacao_ponto, conn)
