import sqlite3
from EstacionaTech.database.database import conectar

def obter_tarifa():
    """Busca a tarifa no banco de dados"""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT valor_por_hora, tempo_tolerancia FROM Tarifa LIMIT 1")
    tarifa = cursor.fetchone()
    conn.close()

    if not tarifa:
        return (5.00, 15)  # Padrão caso não haja tarifa cadastrada

    return tarifa

def atualizar_tarifa(valor_por_hora, tempo_tolerancia):
    """Atualiza a tarifa no banco de dados"""
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE Tarifa SET valor_por_hora = ?, tempo_tolerancia = ?", (valor_por_hora, tempo_tolerancia))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()
