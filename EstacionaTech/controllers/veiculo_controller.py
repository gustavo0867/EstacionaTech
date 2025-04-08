from EstacionaTech.models.veiculo import Veiculo


class VeiculoController:
    @staticmethod
    def criar_veiculo(placa, modelo, marca, cor, ano_fabricacao, id_cliente):
        """Cria um novo veículo"""
        veiculo = Veiculo(placa, modelo, marca, cor, ano_fabricacao, id_cliente)
        return veiculo.salvar()

    @staticmethod
    def obter_veiculo(placa):
        """Busca um veículo pela placa"""
        return Veiculo.buscar_por_placa(placa)

    @staticmethod
    def editar_veiculo(placa, modelo=None, marca=None, cor=None, ano_fabricacao=None, id_cliente=None):
        """Atualiza os dados de um veículo"""
        return Veiculo.atualizar(placa, modelo, marca, cor, ano_fabricacao, id_cliente)

    @staticmethod
    def excluir_veiculo(placa):
        """Remove um veículo pela placa"""
        return Veiculo.deletar(placa)

    @staticmethod
    def listar_veiculos():
        """Lista todos os veículos cadastrados"""
        return Veiculo.listar_todos()

    @staticmethod
    def listar_por_cliente(id_cliente):
        """Lista todos os veículos de um cliente específico"""
        return Veiculo.listar_por_cliente(id_cliente)
