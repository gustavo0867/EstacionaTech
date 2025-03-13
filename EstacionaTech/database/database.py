import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import datetime


def conectar():
    return sqlite3.connect("estacionatech.db")

def verificar_login(email, senha):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Usuario WHERE email = ?", (email,))
    usuario = cursor.fetchone()
    conn.close()

    if usuario and check_password_hash(usuario[4], senha):
        return usuario
    return None

def criar_tabelas():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS Estacionamento (
        id_estacionamento INTEGER PRIMARY KEY AUTOINCREMENT,
	    nome TEXT NOT NULL,
        endereço TEXT NOT NULL,
        capacidade_total INTEGER NOT NULL,
        cnpj TEXT NOT NULL,
        status TEXT NOT NULL CHECK (status IN ('ativo', 'inativo', 'manutenção'))
    );
    
    CREATE TABLE IF NOT EXISTS Setor (
        id_setor TEXT PRIMARY KEY,
        n_vagas INTEGER NOT NULL
    );
    
    CREATE TABLE IF NOT EXISTS Vaga (
        id_vaga TEXT PRIMARY KEY,
        setor TEXT NOT NULL,
        tipo TEXT NOT NULL CHECK (tipo IN ('carro', 'moto', 'deficiente', 'etc.')),
        status TEXT NOT NULL CHECK (status IN ('livre', 'ocupada', 'reservada', 'manutenção')),
        FOREIGN KEY (setor) REFERENCES Setor(id_setor)
);

    CREATE TABLE IF NOT EXISTS Veiculo (
        placa TEXT PRIMARY KEY,
        modelo TEXT NOT NULL,
        marca TEXT NOT NULL,
        cor TEXT NOT NULL,
        ano_fabricacao INTEGER NOT NULL,
        id_cliente TEXT NOT NULL,
        FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente)
    );

    CREATE TABLE IF NOT EXISTS Locacao (
        id_locacao INTEGER PRIMARY KEY AUTOINCREMENT,
        id_vaga INTEGER NOT NULL,
        id_veiculo TEXT NOT NULL,
        id_operador TEXT NOT NULL,
        data_hora_entrada DATETIME NOT NULL,
        data_hora_saida DATETIME,
        FOREIGN KEY (id_vaga) REFERENCES Vaga(id_vaga),
        FOREIGN KEY (id_veiculo) REFERENCES Veiculo(placa),
        FOREIGN KEY (id_operador) REFERENCES Usuario(id_usuario)
    );

    CREATE TABLE IF NOT EXISTS Usuario (
        id_usuario TEXT PRIMARY KEY,
        cpf_usuario TEXT NOT NULL,
        nome TEXT NOT NULL,
        email TEXT NOT NULL,
        senha TEXT NOT NULL,
        tipo TEXT NOT NULL CHECK (tipo IN ('administrador', 'operador')),
        data_ingresso DATETIME NOT NULL,
        data_saida DATETIME
    );

    CREATE TABLE IF NOT EXISTS Cliente (
        id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
        cpf TEXT,
        nome TEXT NOT NULL,
        telefone TEXT NOT NULL,
        email TEXT NOT NULL,
        mensalista BOOLEAN NOT NULL,
        modalidade TEXT NOT NULL CHECK (modalidade IN ('casual', 'mensalista', 'pcd', 'idoso'))
);

    CREATE TABLE IF NOT EXISTS Pagamento (
        id_pagamento INTEGER PRIMARY KEY AUTOINCREMENT,
        id_locacao INTEGER NOT NULL,
        id_operador TEXT NOT NULL,
        valor REAL NOT NULL,
        data_pagamento DATETIME NOT NULL,
        forma_pagamento TEXT NOT NULL CHECK (forma_pagamento IN ('dinheiro', 'cartão', 'etc.')),
        FOREIGN KEY (id_locacao) REFERENCES Locacao(id_locacao),
        FOREIGN KEY (id_operador) REFERENCES Usuario(id_usuario)
    );
    """)

    cursor.execute("SELECT * FROM Usuario WHERE email = 'master@admin.com'")
    if not cursor.fetchone():
        hashed_password = generate_password_hash('admin123')
        cursor.execute("""
        INSERT INTO Usuario (id_usuario, cpf_usuario, nome, email, senha, tipo, data_ingresso)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            'master_001',
            '00000000000',
            'Administrador Master',
            'master@admin.com',
            hashed_password,
            'administrador',
            datetime.datetime.now()

        ))

    conexao.commit()
    conexao.close()


# Executa a criação das tabelas ao iniciar o sistema
criar_tabelas()


# ** alterar para a função inserir_usuario de model/usuario **
def adicionar_usuario(nome, email, senha, tipo):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO Usuario (nome, email, senha, tipo)
    VALUES (?, ?, ?, ?)
    """, (nome, email, senha, tipo))
    conn.commit()
    conn.close()

