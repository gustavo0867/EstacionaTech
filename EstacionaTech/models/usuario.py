import sqlite3
from datetime import datetime

class Usuario:
    def __init__(self, db_path="estacionatech.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.criar_tabela()

    def inserir_usuario(self, id_usuario, cpf, nome, email, senha, tipo, data_ingresso, data_saida=None):
        """Insere um novo usuário no banco"""
        try:
            self.cursor.execute('''
                INSERT INTO usuario (id_usuario, cpf_usuario, nome, email, senha, tipo, data_ingresso, data_saida)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (id_usuario, cpf, nome, email, senha, tipo, data_ingresso, data_saida))
            self.conn.commit()
            print("Usuário cadastrado com sucesso.")
        except sqlite3.Error as e:
            print(f"Erro ao inserir usuário: {e}")

    def buscar_usuario(self, id_usuario):
        """Busca um usuário pelo ID"""
        self.cursor.execute("SELECT * FROM usuario WHERE id_usuario = ?", (id_usuario,))
        return self.cursor.fetchone()

    def buscar_tipo_usuario(self, id_usuario):
        """Retorna o tipo do usuário baseado no ID - Será utilizada para controle de acesso"""
        self.cursor.execute("SELECT tipo FROM usuario WHERE id_usuario = ?", (id_usuario,))
        return self.cursor.fetchone()

        # usuario = self.usuarios.get(id_usuario)
        # return usuario["tipo"] if usuario else None

    def atualizar_usuario(self, id_usuario, nome=None, email=None, senha=None, tipo=None, data_saida=None):
        """Atualiza os dados de um usuário"""
        updates = []
        values = []

        if nome:
            updates.append("nome = ?")
            values.append(nome)
        if email:
            updates.append("email = ?")
            values.append(email)
        if senha:
            updates.append("senha = ?")
            values.append(senha)
        if tipo:
            updates.append("tipo = ?")
            values.append(tipo)
        if data_saida:
            updates.append("data_saida = ?")
            values.append(data_saida)

        values.append(id_usuario)
        query = f"UPDATE usuario SET {', '.join(updates)} WHERE id_usuario = ?"
        self.cursor.execute(query, values)
        self.conn.commit()

    def remover_usuario(self, id_usuario):
        """Remove um usuário pelo ID"""
        self.cursor.execute("DELETE FROM usuario WHERE id_usuario = ?", (id_usuario,))
        self.conn.commit()
        print("Usuário removido com sucesso.")

    def listar_usuarios(self):
        """Lista todos os usuários cadastrados"""
        self.cursor.execute("SELECT * FROM usuario")
        return self.cursor.fetchall()

    def fechar_conexao(self):
        """Fecha a conexão com o banco"""
        self.conn.close()




# Exemplo de uso
# if __name__ == "__main__":
#     usuario_model = Usuario()
#
#     # Inserir um usuário de teste
#     usuario_model.inserir_usuario(
#         id_usuario="U001",
#         cpf="12345678900",
#         nome="Administrador Teste",
#         email="admin@teste.com",
#         senha="senha123",
#         tipo="administrador",
#         data_ingresso=str(datetime.now())
#     )
#
#     # Buscar e exibir usuário
#     user = usuario_model.buscar_usuario("U001")
#     print(user)
#
#     # Fechar conexão
#     usuario_model.fechar_conexao()
