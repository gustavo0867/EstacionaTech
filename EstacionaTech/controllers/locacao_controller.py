from EstacionaTech.EstacionaTech.models.veiculo import Veiculo
from EstacionaTech.EstacionaTech.models.vaga import Vaga
from EstacionaTech.EstacionaTech.models.locacao import Locacao

class LocacaoController:
    @staticmethod
    def registrar_entrada(id_vaga, placa, id_operador):
        """
        Registra a entrada de um veículo no estacionamento.

        Args:
            id_vaga: Identificador da vaga
            placa: Placa do veículo
            id_operador: ID do operador que registrou a entrada

        Returns:
            Tuple (success, message)
        """
        # Verificar se o veículo existe
        veiculo_existe = Veiculo.buscar_por_placa(placa)
        if not veiculo_existe:
            # Implementação futura: solicitar cadastro de veículo
            return False, "Veículo não cadastrado no sistema."

        # Registrar entrada
        success, message = Locacao.criar(id_vaga, placa, id_operador)
        return success, message

    @staticmethod
    def registrar_saida(id_locacao, id_operador):
        """
        Registra a saída de um veículo e calcula o valor a pagar.

        Args:
            id_locacao: ID da locação a ser finalizada
            id_operador: ID do operador que registrou a saída

        Returns:
            Tuple (success, message, dados_pagamento)
        """
        success, message = Locacao.finalizar(id_locacao, id_operador)

        if not success:
            return False, message, None

        # Calcular valor a pagar
        dados_pagamento = Locacao.calcular_valor(id_locacao)

        return True, message, dados_pagamento

    @staticmethod
    def buscar_locacao(id_locacao):
        """
        Busca uma locação pelo ID.

        Args:
            id_locacao: ID da locação

        Returns:
            Dados da locação ou None
        """
        return Locacao.buscar_por_id(id_locacao)

    @staticmethod
    def listar_ativas():
        """Lista todas as locações ativas (veículos estacionados)"""
        return Locacao.listar_ativas()

    @staticmethod
    def listar_recentes(limit=10):
        """Lista as locações mais recentes"""
        return Locacao.listar_recentes(limit)

    @staticmethod
    def buscar_por_placa(placa):
        """Busca locações ativas pela placa do veículo"""
        return Locacao.buscar_por_placa(placa)

    @staticmethod
    def calcular_valor(id_locacao):
        """Calcula o valor a ser pago por uma locação"""
        return Locacao.calcular_valor(id_locacao)

    @staticmethod
    def listar_vagas_disponiveis():
        """Lista todas as vagas disponíveis para estacionamento"""
        vagas = Vaga.listar_todas()
        return [vaga for vaga in vagas if vaga[3] == 'livre']