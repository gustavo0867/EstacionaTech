from EstacionaTech.models.relatorio import Relatorio
from datetime import datetime

class RelatorioController:
    def __init__(self):
        self.relatorio_model = Relatorio()

    def obter_relatorio_locacoes(self, data_inicio_str: str, data_fim_str: str):
        data_inicio, data_fim = self.validar_datas(data_inicio_str, data_fim_str)
        if not data_inicio:
            return {"erro": "Datas inválidas"}

        locacoes = self.relatorio_model.listar_locacoes_no_periodo(data_inicio, data_fim)
        return {"dados": locacoes}

    def obter_relatorio_operacional(self, data_inicio_str: str, data_fim_str: str):
        data_inicio, data_fim = self.validar_datas(data_inicio_str, data_fim_str)
        if not data_inicio:
            return {"erro": "Datas inválidas"}

        vagas, tempo_medio = self.relatorio_model.listar_infos_operacionais_relevantes(data_inicio, data_fim)
        return {
            "vagas_mais_utilizadas": vagas,
            "tempo_medio_permanencia": tempo_medio
        }

    def obter_relatorio_financeiro(self, data_inicio_str: str, data_fim_str: str):
        data_inicio, data_fim = self.validar_datas(data_inicio_str, data_fim_str)
        if not data_inicio:
            return {"erro": "Datas inválidas"}

        faturamento_total = self.relatorio_model.faturamento_total(data_inicio, data_fim)
        faturamento_diario = self.relatorio_model.faturamento_por_dia(data_inicio, data_fim)
        media_diaria = self.relatorio_model.media_diaria_faturamento(data_inicio, data_fim)
        #round(faturamento_total / ((data_fim - data_inicio).days or 1), 2)
        return {
            "faturamento_total": faturamento_total,
            "faturamento_diario": faturamento_diario,
            "media_diaria": media_diaria
        }

    def validar_datas(self, data_inicio_str, data_fim_str):
        try:
            data_inicio = datetime.strptime(data_inicio_str, "%Y-%m-%d")
            data_inicio = data_inicio.replace(hour=0, minute=0, second=0, microsecond=0)

            data_fim = datetime.strptime(data_fim_str, "%Y-%m-%d")
            data_fim = data_fim.replace(hour=23, minute=59, second=59, microsecond=999999)

            return data_inicio, data_fim
        except ValueError:
            return None, None

