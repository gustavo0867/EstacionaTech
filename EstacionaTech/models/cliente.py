from EstacionaTech.database.database import conectar
import sqlite3


class Cliente:
    def __init__(self, nome, cpf, telefone=None, email=None, mensalista=0, modalidade="casual", id_cliente=None):
        self.id_cliente = id_cliente
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone
        self.email = email
        self.mensalista = mensalista  # 0 = não mensalista, 1 = mensalista
        self.modalidade = modalidade  # casual, mensalista, pcd, idoso

    def salvar(self):
        """Insere um novo cliente no banco de dados."""
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO Cliente (nome, cpf, telefone, email, mensalista, modalidade)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (self.nome, self.cpf, self.telefone, self.email, self.mensalista, self.modalidade))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Erro ao inserir cliente: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def buscar_por_cpf(cpf):
        """Busca um cliente pelo CPF."""
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM Cliente WHERE cpf = ?", (cpf,))
            cliente = cursor.fetchone()
            return cliente
        except sqlite3.Error as e:
            print(f"Erro ao buscar cliente: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def buscar_por_id(id_cliente):
        """Busca um cliente pelo ID."""
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM Cliente WHERE id_cliente = ?", (id_cliente,))
            cliente = cursor.fetchone()
            return cliente
        except sqlite3.Error as e:
            print(f"Erro ao buscar cliente: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def listar_todos():
        """Lista todos os clientes cadastrados."""
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT c.*, COUNT(v.placa) as qtd_veiculos 
                FROM Cliente c
                LEFT JOIN Veiculo v ON c.id_cliente = v.id_cliente
                GROUP BY c.id_cliente
                ORDER BY c.nome
            ''')
            clientes = cursor.fetchall()

            # Para cada cliente, buscar seus veículos
            clientes_com_veiculos = []
            for cliente in clientes:
                cursor.execute("SELECT * FROM Veiculo WHERE id_cliente = ?", (cliente[0],))
                veiculos = cursor.fetchall()
                cliente_dict = {
                    'id_cliente': cliente[0],
                    'nome': cliente[1],
                    'cpf': cliente[2],
                    'telefone': cliente[3],
                    'email': cliente[4],
                    'mensalista': cliente[5],
                    'modalidade': cliente[6],
                    'qtd_veiculos': cliente[7],
                    'veiculos': veiculos
                }
                clientes_com_veiculos.append(cliente_dict)

            return clientes_com_veiculos
        except sqlite3.Error as e:
            print(f"Erro ao listar clientes: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def atualizar(id_cliente, nome=None, cpf=None, telefone=None, email=None, mensalista=None, modalidade=None):
        """Atualiza os dados de um cliente."""
        conn = conectar()
        cursor = conn.cursor()

        updates = []
        values = []

        if nome:
            updates.append("nome = ?")
            values.append(nome)
        if cpf:
            updates.append("cpf = ?")
            values.append(cpf)
        if telefone is not None:
            updates.append("telefone = ?")
            values.append(telefone)
        if email is not None:
            updates.append("email = ?")
            values.append(email)
        if mensalista is not None:
            updates.append("mensalista = ?")
            values.append(mensalista)
        if modalidade is not None:
            updates.append("modalidade = ?")
            values.append(modalidade)

        if not updates:
            return False

        values.append(id_cliente)

        try:
            query = f"UPDATE Cliente SET {', '.join(updates)} WHERE id_cliente = ?"
            cursor.execute(query, values)
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Erro ao atualizar cliente: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def deletar(id_cliente):
        """Remove um cliente pelo ID."""
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Cliente WHERE id_cliente = ?", (id_cliente,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Erro ao remover cliente: {e}")
            return False
        finally:
            conn.close()
