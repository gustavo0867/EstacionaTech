import sqlite3

class Setor:
    def __init__(self, id_setor, n_vagas, db_path="estacionatech.db"):
        self.id_setor = id_setor
        self.n_vagas = n_vagas
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def inserir_setor(self):
        """Insere um novo setor no banco"""
        try:
            self.cursor.execute('''
                INSERT INTO setor (id_setor, n_vagas)
                VALUES (?, ?)
            ''', (self.id_setor, self.n_vagas))
            self.conn.commit()
            print(f"Setor {self.id_setor} cadastrado com sucesso.")
        except sqlite3.Error as e:
            print(f"Erro ao inserir setor: {e}")

    def buscar_setor(self, id_setor):
        """Busca um setor pelo ID"""
        self.cursor.execute("SELECT * FROM setor WHERE id_setor = ?", (id_setor,))
        return self.cursor.fetchone()

    def atualizar_setor(self, id_setor, n_vagas=None):
        """Atualiza os dados de um setor"""
        if n_vagas is not None:
            self.cursor.execute("""
                UPDATE setor SET n_vagas = ? WHERE id_setor = ?
            """, (n_vagas, id_setor))
            self.conn.commit()

    def remover_setor(self, id_setor):
        """Remove um setor pelo ID"""
        self.cursor.execute("DELETE FROM setor WHERE id_setor = ?", (id_setor,))
        self.conn.commit()
        print("Setor removido com sucesso.")

    def listar_setores(self):
        """Lista todos os setores cadastrados"""
        self.cursor.execute("SELECT * FROM setor")
        return self.cursor.fetchall()

    def fechar_conexao(self):
        """Fecha a conexão com o banco"""
        self.conn.close()
