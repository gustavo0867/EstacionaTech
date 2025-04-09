from EstacionaTech.models.cliente import Cliente


class ClienteController:
    @staticmethod
    def criar_cliente(nome, cpf, telefone=None, email=None, mensalista=0, modalidade="casual"):
        """Cria um novo cliente"""
        cliente = Cliente(nome, cpf, telefone, email, mensalista, modalidade)
        return cliente.salvar()

    @staticmethod
    def buscar_por_cpf(cpf):
        """Busca um cliente pelo CPF"""
        return Cliente.buscar_por_cpf(cpf)

    @staticmethod
    def buscar_por_id(id_cliente):
        """Busca um cliente pelo ID"""
        return Cliente.buscar_por_id(id_cliente)

    @staticmethod
    def editar_cliente(id_cliente, nome=None, cpf=None, telefone=None, email=None, mensalista=None, modalidade=None):
        """Atualiza os dados de um cliente"""
        return Cliente.atualizar(id_cliente, nome, cpf, telefone, email, mensalista, modalidade)

    @staticmethod
    def excluir_cliente(id_cliente):
        """Remove um cliente pelo ID"""
        return Cliente.deletar(id_cliente)

    @staticmethod
    def listar_clientes():
        """Lista todos os clientes cadastrados"""
        return Cliente.listar_todos()
