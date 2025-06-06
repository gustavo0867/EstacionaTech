from EstacionaTech.models.relatorio import Relatorio
from datetime import datetime
from EstacionaTech.services.gerador_pdf import relatorio_locacoes, relatorio_operacional_geral, relatorio_operacional_clientes, relatorio_financeiro
class RelatorioController:
    def __init__(self):
        self.relatorio_model = Relatorio()

    def obter_relatorio_locacoes(self, data_inicio_str: str, data_fim_str: str):
        data_inicio, data_fim = self.validar_datas(data_inicio_str, data_fim_str)
        if not data_inicio:
            return {"erro": "Datas inválidas"}

        locacoes = self.relatorio_model.listar_locacoes_no_periodo(data_inicio, data_fim)
        return relatorio_locacoes(locacoes, data_inicio_str, data_fim_str)

    def obter_relatorio_operacional(self, data_inicio_str: str, data_fim_str: str):
        data_inicio, data_fim = self.validar_datas(data_inicio_str, data_fim_str)
        if not data_inicio:
            return {"erro": "Datas inválidas"}

        vagas = self.relatorio_model.listar_vagas_mais_utlizadas(data_inicio, data_fim)
        tempo_medio = self.relatorio_model.calcular_tempo_medio_permanencia(data_inicio, data_fim)
        maior_movimento, menor_movimento = self.relatorio_model.calcular_procura_por_horario(data_inicio, data_fim)
        return relatorio_operacional_geral(vagas, tempo_medio, maior_movimento, menor_movimento, data_inicio_str, data_fim_str)

    def obter_relatorio_operacional_clientes(self):
        mensalistas = self.relatorio_model.listar_mensalistas()
        clientes_mais_veiculos = self.relatorio_model.listar_clientes_com_mais_veiculos()
        clientes_frequentes = self.relatorio_model.listar_clientes_frequentes()

        return relatorio_operacional_clientes(mensalistas, clientes_mais_veiculos, clientes_frequentes)

    def obter_relatorio_financeiro(self, data_inicio_str: str, data_fim_str: str):
        data_inicio, data_fim = self.validar_datas(data_inicio_str, data_fim_str)
        if not data_inicio:
            return {"erro": "Datas inválidas"}

        faturamento_total = self.relatorio_model.faturamento_total(data_inicio, data_fim)
        faturamento_por_dia = self.relatorio_model.faturamento_por_dia(data_inicio, data_fim)
        media_diaria = self.relatorio_model.media_diaria_faturamento(data_inicio, data_fim)
        #round(faturamento_total / ((data_fim - data_inicio).days or 1), 2)
        return relatorio_financeiro(faturamento_total, faturamento_por_dia, media_diaria, data_inicio_str, data_fim_str)

    def validar_datas(self, data_inicio_str, data_fim_str):
        try:
            data_inicio = datetime.strptime(data_inicio_str, "%Y-%m-%d")
            data_inicio = data_inicio.replace(hour=0, minute=0, second=0, microsecond=0)

            data_fim = datetime.strptime(data_fim_str, "%Y-%m-%d")
            data_fim = data_fim.replace(hour=23, minute=59, second=59, microsecond=999999)

            return data_inicio, data_fim
        except ValueError:
            return None, None

