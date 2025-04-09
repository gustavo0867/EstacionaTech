import sqlite3
import datetime
from EstacionaTech.database.database import conectar


class PagamentoController:
    @staticmethod
    def registrar_pagamento(id_locacao, id_operador, valor, forma_pagamento='dinheiro'):
        """
        Registra um pagamento para uma locação.

        Args:
            id_locacao: ID da locação
            id_operador: ID do operador que registrou o pagamento
            valor: Valor do pagamento
            forma_pagamento: Forma de pagamento (dinheiro, cartão, etc.)

        Returns:
            Tuple (success, message)
        """
        conn = conectar()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO Pagamento 
                (id_locacao, id_operador, valor, data_pagamento, forma_pagamento)
                VALUES (?, ?, ?, ?, ?)
            """, (
                id_locacao,
                id_operador,
                valor,
                datetime.datetime.now(),
                forma_pagamento
            ))

            conn.commit()
            return True, "Pagamento registrado com sucesso."
        except sqlite3.Error as e:
            conn.rollback()
            return False, f"Erro ao registrar pagamento: {e}"
        finally:
            conn.close()

    @staticmethod
    def buscar_pagamento(id_locacao):
        """
        Busca o pagamento de uma locação pelo ID da locação.

        Args:
            id_locacao: ID da locação

        Returns:
            Dados do pagamento ou None
        """
        conn = conectar()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT * FROM Pagamento
                WHERE id_locacao = ?
            """, (id_locacao,))

            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Erro ao buscar pagamento: {e}")
            return None
        finally:
            conn.close()