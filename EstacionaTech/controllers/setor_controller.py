from EstacionaTech.models.setor import Setor

class SetorController:
    @staticmethod
    def criar_setor(id_setor, n_vagas):
        setor = Setor(id_setor, n_vagas)
        setor.salvar()
        return setor

    @staticmethod
    def obter_setor(id_setor):
        """Busca um setor pelo ID"""
        setor = Setor.buscar(id_setor)
        return setor

    @staticmethod
    def editar_setor(id_setor, n_vagas):
        """Atualiza os dados de um setor"""
        setor = Setor(id_setor, n_vagas)
        setor.atualizar()

    @staticmethod
    def excluir_setor(id_setor):
        """Remove um setor pelo ID"""
        setor = Setor.deletar(id_setor)
        return setor

    @staticmethod
    def listar_setores():
        """Lista todos os setores cadastrados"""
        setores = Setor.listar_todos()
        return setores

