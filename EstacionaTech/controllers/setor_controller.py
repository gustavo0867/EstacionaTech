import sqlite3
from EstacionaTech.database.database import conectar
from EstacionaTech.models.setor import Setor

# criar_setor(nome, n_vagas) → Cria um setor chamando salvar() do Model.
# editar_setor(id_setor, nome, n_vagas) → Atualiza um setor chamando atualizar().
# excluir_setor(id_setor)
# obter_setor(id_setor) → Retorna um setor específico, chamando buscar_por_id().
# listar_setores()


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

