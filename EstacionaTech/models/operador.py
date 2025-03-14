from EstacionaTech.EstacionaTech.database.database import conectar
import sqlite3
import datetime


class Operador:
    @staticmethod
    def create(id_usuario, cpf_usuario, nome, email, senha_hash):
        """
        Cria um novo operador no banco de dados.

        Args:
            id_usuario (str): ID único do operador.
            cpf_usuario (str): CPF do operador.
            nome (str): Nome completo do operador.
            email (str): Email do operador.
            senha_hash (str): Hash da senha gerada com werkzeug.

        Returns:
            tuple: (success: bool, message: str)
        """
        conn = conectar()
        cursor = conn.cursor()
        try:
            # Verificar se ID ou email já existem
            cursor.execute(
                "SELECT * FROM Usuario WHERE id_usuario = ? OR email = ?",
                (id_usuario, email)
            )
            if cursor.fetchone():
                return False, "ID de usuário ou email já cadastrado."

            # Inserir novo operador
            cursor.execute(
                """
                INSERT INTO Usuario 
                    (id_usuario, cpf_usuario, nome, email, senha, tipo, data_ingresso)
                VALUES (?, ?, ?, ?, ?, 'operador', ?)
                """,
                (id_usuario, cpf_usuario, nome, email, senha_hash, datetime.datetime.now())
            )
            conn.commit()
            return True, "Operador cadastrado com sucesso."
        except sqlite3.Error as e:
            conn.rollback()
            return False, f"Erro ao cadastrar operador: {e}"
        finally:
            conn.close()

    @staticmethod
    def delete(id_operador):
        """
        Remove um operador do banco de dados.

        Args:
            id_operador (str): ID do operador a ser removido.

        Returns:
            tuple: (success: bool, message: str)
        """
        conn = conectar()
        cursor = conn.cursor()
        try:
            # Verificar existência do operador
            cursor.execute(
                "SELECT * FROM Usuario WHERE id_usuario = ? AND tipo = 'operador'",
                (id_operador,)
            )
            if not cursor.fetchone():
                return False, "Operador não encontrado."

            cursor.execute(
                "DELETE FROM Usuario WHERE id_usuario = ?",
                (id_operador,)
            )
            conn.commit()
            return True, "Operador removido com sucesso."
        except sqlite3.Error as e:
            conn.rollback()
            return False, f"Erro ao remover operador: {e}"
        finally:
            conn.close()

    @staticmethod
    def update(id_usuario, nome, email, cpf_usuario, senha_hash=None):
        """
        Atualiza os dados de um operador.

        Args:
            id_usuario (str): ID do operador.
            nome (str): Novo nome.
            email (str): Novo email.
            cpf_usuario (str): Novo CPF.
            senha_hash (str, optional): Novo hash da senha (opcional).

        Returns:
            tuple: (success: bool, message: str)
        """
        conn = conectar()
        cursor = conn.cursor()
        try:
            # Verificar existência do operador
            cursor.execute(
                "SELECT * FROM Usuario WHERE id_usuario = ? AND tipo = 'operador'",
                (id_usuario,)
            )
            if not cursor.fetchone():
                return False, "Operador não encontrado."

            # Montar query de atualização
            if senha_hash:
                query = """
                    UPDATE Usuario 
                    SET nome = ?, email = ?, cpf_usuario = ?, senha = ?
                    WHERE id_usuario = ?
                """
                params = (nome, email, cpf_usuario, senha_hash, id_usuario)
            else:
                query = """
                    UPDATE Usuario 
                    SET nome = ?, email = ?, cpf_usuario = ?
                    WHERE id_usuario = ?
                """
                params = (nome, email, cpf_usuario, id_usuario)

            cursor.execute(query, params)
            conn.commit()
            return True, "Operador atualizado com sucesso."
        except sqlite3.Error as e:
            conn.rollback()
            return False, f"Erro ao atualizar operador: {e}"
        finally:
            conn.close()

    @staticmethod
    def get_all():
        """
        Retorna todos os operadores cadastrados.

        Returns:
            list: Lista de tuplas com dados dos operadores.
        """
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM Usuario WHERE tipo = 'operador'")
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Erro ao buscar operadores: {e}")
            return []
        finally:
            conn.close()