from EstacionaTech.database.database import conectar
import sqlite3
from datetime import datetime

class Relatorio:

    def listar_locacoes_no_periodo(self, data_inicio: datetime, data_fim: datetime):
        conn = conectar()
        cursor = conn.cursor()

        query = """
            SELECT * 
            FROM locacao
            WHERE data_hora_entrada >= ? AND data_hora_entrada <= ?
        """
        try:
            cursor.execute(query, (data_inicio, data_fim))
            veiculos = cursor.fetchall()
            conn.commit()

            return veiculos
        except sqlite3.Error as e:
            print(f"Erro ao realizar consulta ao banco de dados: {e}")
            return False
        finally:
            conn.close()

    def listar_infos_operacionais_relevantes(self, data_inicio: datetime, data_fim: datetime):
        conn = conectar()
        cursor = conn.cursor()

        #Lista as vagas mais utilizadas do estacionamento
        query_vagas = """
            SELECT id_vaga, COUNT(id_vaga) AS qtd_uso
            FROM locacao
            WHERE data_hora_entrada >= ? AND data_hora_entrada <= ?
            GROUP BY id_vaga
            ORDER BY qtd_uso DESC
            """

        #Calcula o tempo médio de permanência no estacionamento
        query_tempo_medio = """
            SELECT AVG(strftime('%s', locacao.data_hora_saida) - strftime('%s', locacao.data_hora_entrada)) AS tempo_medio
            FROM locacao
            WHERE locacao.data_hora_saida >= ? AND locacao.data_hora_saida <= ?
            """
            #JOIN saida ON entrada.id = saida.entrada_id
        try:
            cursor.execute(query_vagas, (data_inicio, data_fim))
            cursor.execute(query_tempo_medio, (data_inicio, data_fim))
            vagas = cursor.fetchall()
            tempo_medio = cursor.fetchone()
            conn.commit()

            return vagas, tempo_medio[0] if tempo_medio else None
        except sqlite3.Error as e:
            print(f"Erro ao realizar consulta ao banco de dados: {e}")
            return False
        finally:
            conn.close()


    # def tempo_medio_permanencia(self, data_inicio: datetime, data_fim: datetime):
    #     query = """
    #         SELECT AVG(strftime('%s', saida.data_saida) - strftime('%s', entrada.data_entrada)) AS tempo_medio
    #         FROM entrada
    #         JOIN saida ON entrada.id = saida.entrada_id
    #         WHERE saida.data_saida >= ? AND saida.data_saida <= ?
    #     """
    #     conn = self._conectar()
    #     cursor = conn.cursor()
    #     cursor.execute(query, (data_inicio, data_fim))
    #     resultado = cursor.fetchone()
    #     conn.close()
    #     return resultado[0] if resultado else None
    def faturamento_total(self, data_inicio: datetime, data_fim: datetime):
        conn = conectar()
        cursor = conn.cursor()

        query = """
            SELECT SUM(pagamento.valor) AS faturamento
            FROM pagamento
            WHERE pagamento.data_pagamento >= ? AND pagamento.data_pagamento <= ?
        """

        try:
            cursor.execute(query, (data_inicio, data_fim))
            resultado = cursor.fetchone()
            conn.commit()

            return resultado[0] if resultado else 0
        except sqlite3.Error as e:
            print(f"Erro ao realizar consulta ao banco de dados: {e}")
        finally:
            conn.close()

    def faturamento_por_dia(self, data_inicio: datetime, data_fim: datetime):
        #Faturamento por dia
        conn = conectar()
        cursor = conn.cursor()

        query = """
            SELECT DATE(locacao.data_hora_saida) AS dia, SUM(pagamento.valor) AS total
            FROM locacao
            JOIN pagamento 
            ON locacao.id_locacao = pagamento.id_locacao
            WHERE locacao.data_hora_saida >= ? AND locacao.data_hora_saida <= ?
            GROUP BY dia
            ORDER BY dia
            """

        try:
            cursor.execute(query, (data_inicio, data_fim))
            resultados = cursor.fetchall()
            conn.commit()

            return resultados
        except sqlite3.Error as e:
            print(f"Erro ao realizar consulta ao banco de dados: {e}")
        finally:
            conn.close()

        # #Média Diária de Faturamento
        # faturamento_total = self.calc_faturamento_total(data_inicio, data_fim)
        # dias = (data_fim - data_inicio).days or 1  # Evita divisão por zero
        #
        # return resultados, round(faturamento_total / dias, 2) if faturamento_total else 0


    def media_diaria_faturamento(self, data_inicio: datetime, data_fim: datetime):
        faturamento_total = self.faturamento_total(data_inicio, data_fim)
        dias = (data_fim - data_inicio).days or 1  # Evita divisão por zero
        return round(faturamento_total / dias, 2) if faturamento_total else 0

    # def faturamento_por_dia(self, data_inicio: datetime, data_fim: datetime):
    #     query = """
    #         SELECT DATE(saida.data_saida) AS dia, SUM(saida.valor_pago) AS total
    #         FROM saida
    #         WHERE saida.data_saida >= ? AND saida.data_saida <= ?
    #         GROUP BY dia
    #         ORDER BY dia
    #     """
    #     conn = self._conectar()
    #     cursor = conn.cursor()
    #     cursor.execute(query, (data_inicio, data_fim))
    #     resultados = cursor.fetchall()
    #     conn.close()
    #     return resultados