import sqlite3
from EstacionaTech.database.database import conectar


# salvar() → Insere um novo setor no banco.
# atualizar() → Atualiza um setor existente.
# deletar() → Remove um setor pelo id_setor.
# buscar_por_id(id_setor) → Retorna um setor específico.
# listar_todos()

class Setor:
    def __init__(self, id_setor, n_vagas):
        self.id_setor = id_setor
        self.n_vagas = n_vagas

    def salvar(self):
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Setor (id_setor, n_vagas) VALUES (?, ?)", (self.id_setor, self.n_vagas))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Erro ao inserir setor: {e}")
            return False
        finally:
            conn.close()

    def buscar(self):
        """Busca um setor pelo ID"""
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Setor WHERE id_setor = ?", (self.id_setor,))
        setor = cursor.fetchone()
        conn.close()
        return setor

    def atualizar(self):
        """Atualiza os dados de um setor"""
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE Setor SET n_vagas = ? WHERE id_setor = ?", (self.n_vagas, self.id_setor))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Erro ao atualizar setor: {e}")
            return False
        finally:
            conn.close()

    def deletar(id):
        """Remove um setor pelo ID"""
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Setor WHERE id_setor = ?", (id))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Erro ao remover setor: {e}")
            return False
        finally:
            conn.close()

    def listar_todos():
        """Busca a setores no banco de dados"""
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Setor")
        setores = cursor.fetchall()
        #setores_formatados = [{"id_setor": s[0], "n_vagas": s[1]} for s in setores]

        conn.close()

        return setores