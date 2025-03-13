import sqlite3
from datetime import datetime
from setor import Setor
from vaga import Vaga

class Usuario:
    def __init__(self, id_usuario, cpf, nome, email, senha, tipo, db_path="estacionatech.db"):
        self.id_usuario = id_usuario
        self.cpf = cpf
        self.nome = nome
        self.email = email
        self.senha = senha
        self.tipo = tipo  # 'administrador' ou 'operador'
        self.data_ingresso = datetime.now()
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        #self.criar_tabela()

    def inserir_usuario(self):
        """Insere um novo usuário no banco"""
        try:
            self.cursor.execute('''
                INSERT INTO usuario (id_usuario, cpf_usuario, nome, email, senha, tipo, data_ingresso, data_saida)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (self.id_usuario, self.cpf, self.nome, self.email, self.senha, self.tipo, self.data_ingresso, self.data_saida))
            self.conn.commit()
            print(f"Usuário {self.nome}({self.tipo}) cadastrado com sucesso.")
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

# ================================
# Subclasse Administrador (Herança)
# ================================
class Administrador(Usuario):
    def __init__(self, id_usuario, cpf, nome, email, senha, db_path="estacionatech.db"):
        super().__init__(id_usuario, cpf, nome, email, senha, "administrador", db_path)

    def criar_operador(self, id_operador, cpf, nome, email, senha):
        """Cria um novo operador"""
        operador = Usuario(id_operador, cpf, nome, email, senha, "operador", self.db_path)
        operador.inserir_usuario()

    def criar_setor(self, id_setor, n_vagas):
        """Cria um novo setor"""
        setor = Setor(id_setor, n_vagas)
        setor.inserir_setor()
        # self.cursor.execute("INSERT INTO setor (id_setor, n_vagas) VALUES (?, ?)", (id_setor, n_vagas))
        # self.conn.commit()
        # print(f"Setor {id_setor} criado com {n_vagas} vagas.")

    def listar_setores(self):
        """Lista todos os setores"""
        Setor.listar_setores()

        # self.cursor.execute("SELECT * FROM setor")
        # return self.cursor.fetchall()

    def remover_setor(self, id_setor):
        """Remove um setor"""
        Setor.remover_setor(id_setor)

        # self.cursor.execute("DELETE FROM setor WHERE id_setor = ?", (id_setor,))
        # self.conn.commit()
        # print(f"Setor {id_setor} removido com sucesso.")

    def criar_vaga(self, id_vaga, setor, tipo, status):
        """Cria uma nova vaga"""

        vaga = Vaga(id_vaga, setor, tipo, status)
        vaga.inserir_vaga()

        # self.cursor.execute("INSERT INTO vaga (id_vaga, setor, tipo, status) VALUES (?, ?, ?, 'livre')",
        #                     (id_vaga, setor, tipo))
        # self.conn.commit()
        # print(f"Vaga {id_vaga} do tipo {tipo} criada no setor {setor}.")

    def alterar_status_vaga(self, id_vaga, status):
        """Altera o status de uma vaga para 'manutenção' ou 'livre'"""
        if status not in ("manutenção", "livre"):
            raise ValueError("O administrador só pode alterar para 'manutenção' ou 'livre'.")

        self.cursor.execute("UPDATE vaga SET status = ? WHERE id_vaga = ?", (status, id_vaga))
        self.conn.commit()
        print(f"Vaga {id_vaga} atualizada para o status {status}.")


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
