from EstacionaTech.database.database import conectar
import sqlite3
from datetime import datetime, timedelta
from collections import defaultdict

class Relatorio:

    # //// RELATÓRIOS OPERACIONAIS ////
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

    def listar_vagas_mais_utlizadas(self, data_inicio: datetime, data_fim: datetime):
        conn = conectar()
        cursor = conn.cursor()

        #Lista as vagas mais utilizadas do estacionamento
        query = """
            SELECT id_vaga, COUNT(id_vaga) AS qtd_uso
            FROM locacao
            WHERE data_hora_entrada >= ? AND data_hora_entrada <= ?
            GROUP BY id_vaga
            ORDER BY qtd_uso DESC
            """
        try:
            cursor.execute(query, (data_inicio, data_fim))
            vagas = cursor.fetchall()
            conn.commit()

            return vagas
        except sqlite3.Error as e:
            print(f"Erro ao realizar consulta ao banco de dados: {e}")
            return False
        finally:
            conn.close()

    def calcular_tempo_medio_permanencia(self, data_inicio: datetime, data_fim: datetime):
        """
        Calcula o tempo médio de permanência, ignorando durações irrealistas (outliers).
        """
        conn = conectar()
        cursor = conn.cursor()

        LIMITE_MAX_HORAS = 24
        
        limite_em_segundos = LIMITE_MAX_HORAS * 3600

        query = f"""
            SELECT AVG(strftime('%s', data_hora_saida) - strftime('%s', data_hora_entrada)) AS tempo_medio_segundos
            FROM locacao
            WHERE 
                data_hora_saida IS NOT NULL 
                AND data_hora_saida BETWEEN ? AND ?
                AND (strftime('%s', data_hora_saida) - strftime('%s', data_hora_entrada)) < ?
        """
        try:
            data_fim_ajustada = data_fim.replace(hour=23, minute=59, second=59)

            # O novo parâmetro (limite_em_segundos) é adicionado à execução
            cursor.execute(query, (data_inicio, data_fim_ajustada, limite_em_segundos))
            resultado = cursor.fetchone()
            conn.commit()

            segundos_medios = resultado[0] if resultado and resultado[0] is not None else 0

            if segundos_medios > 0:
                segundos_medios = round(segundos_medios)
                td = timedelta(seconds=segundos_medios)
                
                horas, remanescente = divmod(td.seconds, 3600)
                minutos, segundos = divmod(remanescente, 60)
                
                partes = []
                if td.days > 0:
                    partes.append(f"{td.days} dia{'s' if td.days > 1 else ''}")
                if horas > 0:
                    partes.append(f"{horas} hora{'s' if horas > 1 else ''}")
                if minutos > 0:
                    partes.append(f"{minutos} minuto{'s' if minutos > 1 else ''}")
                # Apenas mostra segundos se for a única unidade de tempo relevante
                if segundos > 0 and not partes:
                     partes.append(f"{segundos} segundo{'s' if segundos > 1 else ''}")

                return ", ".join(partes) if partes else "Menos de um minuto"
            else:
                return "Nenhuma permanência válida encontrada no período."

        except sqlite3.Error as e:
            print(f"Erro ao realizar consulta ao banco de dados: {e}")
            return "Erro ao calcular dados"
        finally:
            conn.close()



    def calcular_procura_por_horario(self, data_inicio: datetime, data_fim: datetime):
        conn = conectar()
        cursor = conn.cursor()

        query = """
            SELECT data_hora_entrada, data_hora_saida
            FROM locacao
            WHERE data_hora_entrada >= ? AND data_hora_entrada <= ?
            """
        try:
            cursor.execute(query, (data_inicio, data_fim))
            locacoes = cursor.fetchall()
            conn.commit()

            # Inicialização de contador para as faixas
            faixas = {
                'Madrugada (00h-06h)': 0,
                'Manhã (06h-12h)': 0,
                'Tarde (12h-18h)': 0,
                'Noite (18h-00h)': 0
            }

            # Para cada locação
            # for loc in locacoes:
            #     print(f"Tuple recebida: {loc} com {len(loc)} elementos", flush = True)

            for entrada, saida in locacoes:
                if isinstance(entrada, str):
                    entrada = datetime.fromisoformat(entrada)
                if saida is not None:
                    if isinstance(saida, str):
                        saida = datetime.fromisoformat(saida)
                else:
                    saida = data_fim.replace(hour=23, minute=59)#saída em aberto, estabelece um limite igual à data fim para gerar o relatório do status naquele momento

                print(f"Entrada: {entrada} ({type(entrada)}), Saída: {saida} ({type(saida)})", flush=True)

                hora_atual = entrada
                while hora_atual < saida:
                    print(f"****hora_atual: {hora_atual} - ({type(hora_atual)}) || saida: {saida} - ({type(saida)})", flush = True)
                    hora = hora_atual.hour
                    if 0 <= hora < 6:
                        faixas['Madrugada (00h-06h)'] += 1
                    elif 6 <= hora < 12:
                        faixas['Manhã (06h-12h)'] += 1
                    elif 12 <= hora < 18:
                        faixas['Tarde (12h-18h)'] += 1
                    else:
                        faixas['Noite (18h-00h)'] += 1
                    hora_atual += timedelta(hours=1)

            maior_movimento = max(faixas, key=faixas.get)
            menor_movimento = min(faixas, key=faixas.get)

            return maior_movimento, menor_movimento
        except sqlite3.Error as e:
            print(f"Erro ao realizar consulta ao banco de dados: {e}")
            return False
        finally:
            conn.close()

    def listar_mensalistas(self):#, data_inicio: datetime, data_fim: datetime
        conn = conectar()
        cursor = conn.cursor()

        query = """
            SELECT id_cliente, cpf, nome, telefone, email, modalidade
            FROM cliente
            WHERE mensalista = TRUE
        """

        try:
            cursor.execute(query)
            resultado = cursor.fetchall()
            conn.commit()

            return resultado
        except sqlite3.Error as e:
            print(f"Erro ao realizar consulta ao banco de dados: {e}")
        finally:
            conn.close()

    def listar_clientes_com_mais_veiculos(self):
        conn = conectar()
        cursor = conn.cursor()

        query = """
            SELECT c.id_cliente, c.cpf, c.nome, c.telefone, c.email, c.mensalista, c.modalidade, COUNT(v.id_cliente) as qtde_veiculos
            FROM cliente c
            INNER JOIN veiculo v 
            ON c.id_cliente = v.id_cliente
            GROUP BY c.id_cliente
            ORDER BY qtde_veiculos DESC
            LIMIT 10
            """
        try:
            cursor.execute(query)
            resultado = cursor.fetchall()
            conn.commit()

            return resultado
        except sqlite3.Error as e:
            print(f"Erro ao realizar consulta ao banco de dados: {e}")
        finally:
            conn.close()

    def listar_clientes_frequentes(self):
        conn = conectar()
        cursor = conn.cursor()

        query = """
            SELECT c.id_cliente, c.cpf, c.nome, c.telefone, c.email, c.mensalista, c.modalidade,
            COUNT(l.id_locacao) AS total_locacoes
            FROM cliente c
            JOIN veiculo v ON c.id_cliente = v.id_cliente
            JOIN locacao l ON v.placa = l.id_veiculo
            GROUP BY c.id_cliente
            ORDER BY total_locacoes DESC
            LIMIT 10;
        """

        try:
            cursor.execute(query)
            resultado = cursor.fetchall()
            conn.commit()

            return resultado
        except sqlite3.Error as e:
            print(f"Erro ao realizar consulta ao banco de dados: {e}")
        finally:
            conn.close()


    def faturamento_total(self, data_inicio: datetime, data_fim: datetime):
        conn = conectar()
        cursor = conn.cursor()

        # ==============================================================================
        # CONFIGURAÇÃO DO FILTRO: Defina aqui o intervalo de valores "realistas"
        # para um único pagamento. Valores fora deste intervalo serão ignorados.
        LIMITE_MIN_PAGAMENTO = 0.01  # Ignora pagamentos zerados ou negativos
        LIMITE_MAX_PAGAMENTO = 1000.00 # Ignora pagamentos muito altos (provavelmente testes)
        # ==============================================================================

        query = """
            SELECT SUM(pagamento.valor) AS faturamento
            FROM pagamento
            WHERE 
                pagamento.data_pagamento BETWEEN ? AND ?
                AND pagamento.valor > ? AND pagamento.valor < ?
        """

        try:
            data_fim_ajustada = data_fim.replace(hour=23, minute=59, second=59)
            
            cursor.execute(query, (data_inicio, data_fim_ajustada, LIMITE_MIN_PAGAMENTO, LIMITE_MAX_PAGAMENTO))
            resultado = cursor.fetchone()
            conn.commit()

            return resultado[0] if resultado and resultado[0] is not None else 0
        except sqlite3.Error as e:
            print(f"Erro ao realizar consulta ao banco de dados: {e}")
            return 0
        finally:
            conn.close()

    def faturamento_por_dia(self, data_inicio: datetime, data_fim: datetime):
        # Faturamento por dia, também com filtro de bom senso
        conn = conectar()
        cursor = conn.cursor()

        # Usamos os mesmos limites para consistência
        LIMITE_MIN_PAGAMENTO = 0.01
        LIMITE_MAX_PAGAMENTO = 1000.00

        query = """
            SELECT DATE(locacao.data_hora_saida) AS dia, SUM(pagamento.valor) AS total
            FROM locacao
            JOIN pagamento 
            ON locacao.id_locacao = pagamento.id_locacao
            WHERE 
                locacao.data_hora_saida BETWEEN ? AND ?
                AND pagamento.valor > ? AND pagamento.valor < ?
            GROUP BY dia
            ORDER BY dia
        """

        try:
            data_fim_ajustada = data_fim.replace(hour=23, minute=59, second=59)

            cursor.execute(query, (data_inicio, data_fim_ajustada, LIMITE_MIN_PAGAMENTO, LIMITE_MAX_PAGAMENTO))
            resultados = cursor.fetchall()
            conn.commit()

            return resultados
        except sqlite3.Error as e:
            print(f"Erro ao realizar consulta ao banco de dados: {e}")
            return [] # Retorna lista vazia em caso de erro
        finally:
            conn.close()


    def media_diaria_faturamento(self, data_inicio: datetime, data_fim: datetime):
        # Esta função não precisa de alteração, pois já usa a faturamento_total() corrigida.
        faturamento_total_filtrado = self.faturamento_total(data_inicio, data_fim)
        dias = (data_fim - data_inicio).days or 1  # Evita divisão por zero
        
        if faturamento_total_filtrado > 0:
            return round(faturamento_total_filtrado / dias, 2) 
        else:
            return 0
