from EstacionaTech.EstacionaTech.database.database import conectar
import sqlite3


class Veiculo:
    def __init__(self, placa, modelo, marca, cor, ano_fabricacao, id_cliente):
        self.placa = placa
        self.modelo = modelo
        self.marca = marca
        self.cor = cor
        self.ano_fabricacao = ano_fabricacao
        self.id_cliente = id_cliente

    def salvar(self):
        """Insere um novo veículo no banco de dados."""
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO Veiculo (placa, modelo, marca, cor, ano_fabricacao, id_cliente)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (self.placa, self.modelo, self.marca, self.cor, self.ano_fabricacao, self.id_cliente))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Erro ao inserir veículo: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def buscar_por_placa(placa):
        """Busca um veículo pela placa."""
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM Veiculo WHERE placa = ?", (placa,))
            veiculo = cursor.fetchone()
            return veiculo
        except sqlite3.Error as e:
            print(f"Erro ao buscar veículo: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def listar_todos():
        """Lista todos os veículos cadastrados."""
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT v.*, c.nome as cliente_nome 
                FROM Veiculo v
                LEFT JOIN Cliente c ON v.id_cliente = c.id_cliente
                ORDER BY v.placa
            """)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Erro ao listar veículos: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def listar_por_cliente(id_cliente):
        """Lista todos os veículos de um cliente específico."""
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM Veiculo WHERE id_cliente = ?", (id_cliente,))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Erro ao listar veículos do cliente: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def atualizar(placa, modelo=None, marca=None, cor=None, ano_fabricacao=None, id_cliente=None):
        """Atualiza os dados de um veículo."""
        conn = conectar()
        cursor = conn.cursor()

        updates = []
        values = []

        if modelo:
            updates.append("modelo = ?")
            values.append(modelo)
        if marca:
            updates.append("marca = ?")
            values.append(marca)
        if cor:
            updates.append("cor = ?")
            values.append(cor)
        if ano_fabricacao:
            updates.append("ano_fabricacao = ?")
            values.append(ano_fabricacao)
        if id_cliente:
            updates.append("id_cliente = ?")
            values.append(id_cliente)

        if not updates:
            return False

        values.append(placa)

        try:
            query = f"UPDATE Veiculo SET {', '.join(updates)} WHERE placa = ?"
            cursor.execute(query, values)
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Erro ao atualizar veículo: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def deletar(placa):
        """Remove um veículo pela placa."""
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Veiculo WHERE placa = ?", (placa,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Erro ao remover veículo: {e}")
            return False
        finally:
            conn.close()