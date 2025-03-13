import sqlite3

class Vaga:
    def __init__(self, id_vaga, setor, tipo, status, db_path="estacionatech.db"):
        self.id_vaga = id_vaga
        self.setor = setor
        self.tipo = tipo
        self.status = status
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def inserir_vaga(self):
        """Insere uma nova vaga no banco."""
        try:
            self.cursor.execute('''
                INSERT INTO vaga (id_vaga, setor, tipo, status)
                VALUES (?, ?, ?, ?)
            ''', (self.id_vaga, self.setor, self.tipo, self.status))
            self.conn.commit()
            print("Vaga cadastrada com sucesso.")
        except sqlite3.Error as e:
            print(f"Erro ao inserir vaga: {e}")

    def buscar_vaga(self, id_vaga):
        """Busca uma vaga pelo ID."""
        self.cursor.execute("SELECT * FROM vaga WHERE id_vaga = ?", (id_vaga,))
        return self.cursor.fetchone()

    def atualizar_vaga(self, id_vaga, setor=None, tipo=None, status=None):
        """Atualiza os dados de uma vaga."""
        updates = []
        values = []

        if setor:
            updates.append("setor = ?")
            values.append(setor)
        if tipo:
            updates.append("tipo = ?")
            values.append(tipo)
        if status:
            updates.append("status = ?")
            values.append(status)

        values.append(id_vaga)
        query = f"UPDATE vaga SET {', '.join(updates)} WHERE id_vaga = ?"
        self.cursor.execute(query, values)
        self.conn.commit()

    def remover_vaga(self, id_vaga):
        """Remove uma vaga pelo ID."""
        self.cursor.execute("DELETE FROM vaga WHERE id_vaga = ?", (id_vaga,))
        self.conn.commit()
        print("Vaga removida com sucesso.")

    def listar_vagas(self):
        """Lista todas as vagas cadastradas."""
        self.cursor.execute("SELECT * FROM vaga")
        return self.cursor.fetchall()

    def fechar_conexao(self):
        """Fecha a conexão com o banco."""
        self.conn.close()
