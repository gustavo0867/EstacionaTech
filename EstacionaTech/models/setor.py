import sqlite3
from EstacionaTech.database.database import conectar

class Setor:
    def __init__(self, id_setor, n_vagas):
        self.id_setor = id_setor
        self.n_vagas = n_vagas

def inserir_setor(self):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO usuario (id_usuario, cpf_usuario, nome, email, senha, tipo, data_ingresso, data_saida)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (self.id_setor, self.n_vagas))
        conn.commit()
        print(f"Setor {self.id_setor} (cadastrado com sucesso.")
    except sqlite3.Error as e:
        print(f"Erro ao inserir usuário: {e}")


def listar_setores():
    """Busca a setores no banco de dados"""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id_setor FROM Setor")
    setores = cursor.fetchall()
    setores_formatados = [{"id_setor": s[0]} for s in setores]


    conn.close()

    return setores_formatados