import sqlite3
from EstacionaTech.database.database import conectar
from EstacionaTech.models.setor import Setor

class SetorController:
    
    @staticmethod
    def inserir_setor(id_setor, n_vagas):
        """Insere um novo setor no banco"""
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Setor (id_setor, n_vagas) VALUES (?, ?)", (id_setor, n_vagas))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Erro ao inserir setor: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def buscar_setor(id_setor):
        """Busca um setor pelo ID"""


        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Setor WHERE id_setor = ?", (id_setor,))
        setor = cursor.fetchone()
        conn.close()
        return setor

    @staticmethod
    def atualizar_setor(id_setor, n_vagas):
        """Atualiza os dados de um setor"""
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE Setor SET n_vagas = ? WHERE id_setor = ?", (n_vagas, id_setor))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Erro ao atualizar setor: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def remover_setor(id_setor):
        """Remove um setor pelo ID"""
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Setor WHERE id_setor = ?", (id_setor,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Erro ao remover setor: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def listar_setores():
        """Lista todos os setores cadastrados"""
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Setor")
        setores = cursor.fetchall()
        conn.close()
        return setores
