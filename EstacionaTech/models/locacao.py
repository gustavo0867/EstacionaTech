from EstacionaTech.database.database import conectar
import sqlite3
import datetime


class Locacao:
    def __init__(self, id_locacao=None, id_vaga=None, id_veiculo=None, id_operador=None, data_hora_entrada=None,
                 data_hora_saida=None):
        self.id_locacao = id_locacao
        self.id_vaga = id_vaga
        self.id_veiculo = id_veiculo
        self.id_operador = id_operador
        self.data_hora_entrada = data_hora_entrada
        self.data_hora_saida = data_hora_saida

    @staticmethod
    def criar(id_vaga, id_veiculo, id_operador):
        """Registra entrada de um veículo no estacionamento"""
        conn = conectar()
        cursor = conn.cursor()

        try:
            # Verificar se a vaga está livre
            cursor.execute("SELECT status FROM Vaga WHERE id_vaga = ?", (id_vaga,))
            vaga = cursor.fetchone()

            if not vaga:
                return False, "Vaga não encontrada."

            if vaga[0] != 'livre':
                return False, "Vaga não está livre."

            # Verificar se o veículo existe
            cursor.execute("SELECT * FROM Veiculo WHERE placa = ?", (id_veiculo,))
            if not cursor.fetchone():
                return False, "Veículo não cadastrado."

            # Atualizar status da vaga para ocupada
            cursor.execute("UPDATE Vaga SET status = 'ocupada' WHERE id_vaga = ?", (id_vaga,))

            # Inserir registro de locação
            cursor.execute("""
                INSERT INTO Locacao (id_vaga, id_veiculo, id_operador, data_hora_entrada)
                VALUES (?, ?, ?, ?)
            """, (id_vaga, id_veiculo, id_operador, datetime.datetime.now()))

            conn.commit()
            return True, "Entrada de veículo registrada com sucesso."
        except sqlite3.Error as e:
            conn.rollback()
            return False, f"Erro ao registrar entrada: {e}"
        finally:
            conn.close()

    @staticmethod
    def finalizar(id_locacao, id_operador):
        """Registra a saída de um veículo e libera a vaga"""
        conn = conectar()
        cursor = conn.cursor()

        try:
            # Verificar se a locação existe e não está finalizada
            cursor.execute("""
                SELECT id_vaga, data_hora_saida FROM Locacao 
                WHERE id_locacao = ?
            """, (id_locacao,))

            locacao = cursor.fetchone()
            if not locacao:
                return False, "Locação não encontrada."

            if locacao[1] is not None:
                return False, "Esta locação já foi finalizada."

            # Atualizar locação com data/hora de saída
            data_hora_saida = datetime.datetime.now()
            cursor.execute("""
                UPDATE Locacao SET data_hora_saida = ?, id_operador = ?
                WHERE id_locacao = ?
            """, (data_hora_saida, id_operador, id_locacao))

            # Liberar a vaga
            cursor.execute("UPDATE Vaga SET status = 'livre' WHERE id_vaga = ?", (locacao[0],))

            conn.commit()
            return True, "Saída de veículo registrada com sucesso."
        except sqlite3.Error as e:
            conn.rollback()
            return False, f"Erro ao registrar saída: {e}"
        finally:
            conn.close()

    @staticmethod
    def buscar_por_id(id_locacao):
        """Busca uma locação pelo ID"""
        conn = conectar()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT 
                    l.id_locacao,       -- [0]
                    l.id_vaga,          -- [1]
                    l.id_veiculo,       -- [2]
                    l.data_hora_entrada,-- [3]
                    l.data_hora_saida,  -- [4]
                    v.modelo,           -- [5]
                    v.placa,            -- [6]
                    v.cor,              -- [7]
                    u.nome              -- [8]
                FROM Locacao l
                JOIN Veiculo v ON l.id_veiculo = v.placa
                JOIN Usuario u ON l.id_operador = u.id_usuario
                WHERE l.id_locacao = ?
            """, (id_locacao,))

            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Erro ao buscar locação: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def listar_ativas():
        """Lista todas as locações ativas (sem data de saída)"""
        conn = conectar()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT l.id_locacao, l.id_vaga, l.id_veiculo, l.data_hora_entrada,
                       v.modelo, v.cor
                FROM Locacao l
                JOIN Veiculo v ON l.id_veiculo = v.placa
                WHERE l.data_hora_saida IS NULL
                ORDER BY l.data_hora_entrada DESC
            """)

            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Erro ao listar locações ativas: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def listar_recentes(limit=10):
        """Lista as locações mais recentes, incluindo finalizadas"""
        conn = conectar()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT l.id_locacao, l.id_vaga, l.id_veiculo, 
                       l.data_hora_entrada, l.data_hora_saida,
                       v.modelo, v.cor
                FROM Locacao l
                JOIN Veiculo v ON l.id_veiculo = v.placa
                ORDER BY 
                    CASE WHEN l.data_hora_saida IS NULL THEN 0 ELSE 1 END,
                    l.data_hora_entrada DESC
                LIMIT ?
            """, (limit,))

            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Erro ao listar locações recentes: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def buscar_por_placa(placa):
        """Busca locações ativas por placa do veículo"""
        conn = conectar()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT l.id_locacao, l.id_vaga, l.id_veiculo, l.data_hora_entrada,
                       v.modelo, v.cor
                FROM Locacao l
                JOIN Veiculo v ON l.id_veiculo = v.placa
                WHERE l.id_veiculo LIKE ? AND l.data_hora_saida IS NULL
                ORDER BY l.data_hora_entrada DESC
            """, (f"%{placa}%",))

            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Erro ao buscar locações por placa: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def calcular_valor(id_locacao):
        """Calcula o valor a ser pago com base na tarifa cadastrada"""
        conn = conectar()
        cursor = conn.cursor()

        try:
            # Buscar dados da locação
            cursor.execute("""
                SELECT data_hora_entrada, data_hora_saida 
                FROM Locacao
                WHERE id_locacao = ?
            """, (id_locacao,))

            locacao = cursor.fetchone()
            if not locacao or locacao[1] is None:
                return None

            # Converter strings para objetos datetime
            if isinstance(locacao[0], str):
                entrada = datetime.datetime.fromisoformat(locacao[0].replace(' ', 'T'))
            else:
                entrada = locacao[0]

            if isinstance(locacao[1], str):
                saida = datetime.datetime.fromisoformat(locacao[1].replace(' ', 'T'))
            else:
                saida = locacao[1]

            # Calcular duração em minutos
            duracao_minutos = (saida - entrada).total_seconds() / 60

            # Buscar tarifa atual
            cursor.execute("SELECT valor_por_hora, tempo_tolerancia FROM Tarifa")
            tarifa = cursor.fetchone()

            if not tarifa:
                return None

            valor_por_hora, tempo_tolerancia = tarifa

            # Calcular valor a pagar
            if duracao_minutos <= tempo_tolerancia:
                return 0  # Dentro da tolerância, não cobra

            # Converte para horas e calcula, sempre arredondando para cima
            horas = duracao_minutos / 60
            horas_cobradas = max(1, int(horas) + (1 if horas % 1 > 0 else 0))

            return {
                'valor': horas_cobradas * valor_por_hora,
                'horas_cobradas': horas_cobradas,
                'duracao_minutos': int(duracao_minutos),
                'valor_por_hora': valor_por_hora
            }

        except (sqlite3.Error, ValueError) as e:
            print(f"Erro ao calcular valor: {e}")
            return None
        finally:
            conn.close()