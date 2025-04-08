from EstacionaTech.EstacionaTech.models.vaga import Vaga

class VagaController:
    @staticmethod
    def criar_vaga(id_vaga, setor, tipo, status):
        vaga = Vaga(id_vaga, setor, tipo, status)
        vaga.salvar()
        return vaga

    @staticmethod
    def obter_vaga(id_vaga):
        """Busca um vaga pelo ID"""
        vaga = Vaga.buscar(id_vaga)
        return vaga

    @staticmethod
    def editar_vaga(id_vaga, setor, tipo, status):
        """Atualiza os dados de uma vaga"""
        vaga = Vaga(id_vaga, setor, tipo, status)
        return vaga.atualizar(tipo, status)


    @staticmethod
    def excluir_vaga(id_vaga):
        """Remove um setor pelo ID"""
        vaga = Vaga.deletar(id_vaga)
        return vaga

    @staticmethod
    def listar_vagas():
        """Lista todos os setores cadastrados"""
        vagas= Vaga.listar_todas()
        return vagas

