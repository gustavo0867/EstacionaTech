import sqlite3
from EstacionaTech.database.database import conectar

class Vaga:
    def __init__(self, id_vaga, setor, tipo, status):
        self.id_vaga = id_vaga
        self.setor = setor
        self.tipo = tipo
        self.status = status
        # self.conn = sqlite3.connect(db_path)
        # self.cursor = self.conn.cursor()

    def salvar(self):
        """Insere uma nova vaga no banco."""
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO vaga (id_vaga, setor, tipo, status)
                VALUES (?, ?, ?, ?)
            ''', (self.id_vaga, self.setor, self.tipo, self.status))
            conn.commit()
            print("Vaga cadastrada com sucesso.")
            return True
        except sqlite3.Error as e:
            print(f"Erro ao inserir vaga: {e}")
            return False
        finally:
            conn.close()

    def buscar(self):
        """Busca uma vaga pelo ID."""
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vaga WHERE id_vaga = ?", (self.id_vaga,))
        vaga = cursor.fetchone()
        return vaga

    def atualizar(self, tipo=None, status=None):
        # """Atualiza os dados de uma vaga."""
        # conn = conectar()
        # cursor = conn.cursor()
        #
        # updates = []
        # values = []
        #
        # # if setor:
        # #     updates.append("setor = ?")
        # #     values.append(setor)
        # if tipo:
        #     updates.append("tipo = ?")
        #     values.append(tipo)
        # if status:
        #     updates.append("status = ?")
        #     values.append(status)
        #
        # values.append(self.id_vaga)
        # try:
        #     query = f"UPDATE vaga SET {', '.join(updates)} WHERE id_vaga = ?"
        #     cursor.execute(query, values)
        #     conn.commit()
        #     return True
        # except sqlite3.Error as e:
        #     print(f"Erro ao atualizar vaga: {e}")
        #     return False
        # finally:
        #     conn.close()


        #####

        """Atualiza os dados de uma vaga."""
        conn = conectar()
        cursor = conn.cursor()

        updates = []
        values = []

        if tipo is not None:
            updates.append("tipo = ?")
            values.append(tipo)
        if status is not None:
            updates.append("status = ?")
            values.append(status)

        # Se não houver nada para atualizar, evita erro SQL
        if not updates:
            conn.close()
            return False

        # Adiciona o ID da vaga no final dos valores
        values.append(self.id_vaga)

        try:
            query = f"UPDATE vaga SET {', '.join(updates)} WHERE id_vaga = ?"
            cursor.execute(query, values)
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Erro ao atualizar vaga: {e}")
            return False
        finally:
            conn.close()

    def deletar(id):
        """Remove uma vaga pelo ID."""
        conn = conectar()
        cursor = conn.cursor()

        try:
            query = "DELETE FROM vaga WHERE id_vaga = ?"
            cursor.execute(query, (id,))
            conn.commit()
            print("Vaga removida com sucesso.")
            return True
        except sqlite3.Error as e:
            print(f"Erro ao remover vaga: {e}")
            return False
        finally:
            conn.close()

    def listar_todas():
        """Lista todas as vagas cadastradas."""
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM vaga")
        vagas = cursor.fetchall()

        conn.close()

        return vagas
