from EstacionaTech.models.tarifa import obter_tarifa, atualizar_tarifa

def buscar_tarifa():
    """Retorna a tarifa atual para a aplicação"""
    return obter_tarifa()

def modificar_tarifa(novo_valor, nova_tolerancia):
    """Modifica a tarifa no banco"""
    atualizar_tarifa(novo_valor, nova_tolerancia)
    return {"mensagem": "Tarifa atualizada com sucesso!"}
