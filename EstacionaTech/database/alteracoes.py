import os
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from database import conectar

def criar_nova():
    conexao = conectar()
    cursor = conexao.cursor()

    # Criação das tabelas principais
    cursor.executescript("""
    CREATE TABLE Vaga_nova (
        id_vaga TEXT PRIMARY KEY,
        setor TEXT NOT NULL,
        tipo TEXT NOT NULL CHECK (tipo IN ('carro', 'moto', 'utilitário', 'preferencial')),
        status TEXT NOT NULL CHECK (status IN ('livre', 'ocupada', 'reservada', 'manutenção')),
        FOREIGN KEY (setor) REFERENCES Setor(id_setor)
    );

""")
def copiar():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.executescript("""
    INSERT INTO Vaga_nova (id_vaga, setor, tipo, status)
    SELECT id_vaga, setor, tipo, status FROM Vaga;
    
    
    """)

    conexao.commit()
    conexao.close()

def excluir():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.executescript("""
        DROP TABLE Vaga;
        ALTER TABLE Vaga_nova RENAME TO Vaga;
        
    """)
    conexao.commit()
    conexao.close()

excluir()