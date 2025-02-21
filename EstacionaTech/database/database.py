import sqlite3


def conectar():
    return sqlite3.connect("estacionatech.db")


def criar_tabelas():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS Vaga (
        id_vaga INTEGER PRIMARY KEY AUTOINCREMENT,
        id_mapa INTEGER NOT NULL,
        tipo TEXT NOT NULL CHECK (tipo IN ('carro', 'moto', 'deficiente', 'etc.')),
        status TEXT NOT NULL CHECK (status IN ('livre', 'ocupada', 'reservada', 'manutenção')),
        FOREIGN KEY (id_mapa) REFERENCES Layout(id_layout)
    );

    CREATE TABLE IF NOT EXISTS Veiculo (
        placa TEXT PRIMARY KEY,
        modelo TEXT NOT NULL,
        marca TEXT NOT NULL,
        cor TEXT NOT NULL,
        ano_fabricacao INTEGER NOT NULL,
        id_cliente TEXT NOT NULL,
        FOREIGN KEY (id_cliente) REFERENCES Cliente(cpf)
    );

    CREATE TABLE IF NOT EXISTS Locacao (
        id_locacao INTEGER PRIMARY KEY AUTOINCREMENT,
        id_vaga INTEGER NOT NULL,
        id_veiculo TEXT NOT NULL,
        data_hora_entrada DATETIME NOT NULL,
        data_hora_saida DATETIME,
        id_operador INTEGER NOT NULL,
        FOREIGN KEY (id_vaga) REFERENCES Vaga(id_vaga),
        FOREIGN KEY (id_veiculo) REFERENCES Veiculo(placa),
        FOREIGN KEY (id_operador) REFERENCES Operador(id_operador)
    );

    CREATE TABLE IF NOT EXISTS Layout (
        id_layout INTEGER PRIMARY KEY AUTOINCREMENT,
        n_vagas INTEGER NOT NULL,
        visao BLOB NOT NULL
    );

    CREATE TABLE IF NOT EXISTS Usuario (
        id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL,
        tipo TEXT NOT NULL CHECK (tipo IN ('administrador', 'operador')),
        UNIQUE(email)
    );

    CREATE TABLE IF NOT EXISTS Cliente (
        cpf TEXT PRIMARY KEY,
        nome TEXT NOT NULL,
        telefone TEXT NOT NULL,
        mensalista BOOLEAN NOT NULL
    );

    CREATE TABLE IF NOT EXISTS Pagamento (
        id_pagamento INTEGER PRIMARY KEY AUTOINCREMENT,
        id_locacao INTEGER NOT NULL,
        valor REAL NOT NULL,
        data_pagamento DATETIME NOT NULL,
        forma_pagamento TEXT NOT NULL CHECK (forma_pagamento IN ('dinheiro', 'cartão', 'etc.')),
        FOREIGN KEY (id_locacao) REFERENCES Locacao(id_locacao)
    );
    """)

    # Verificando se o usuário master já existe, caso contrário, criando-o
    cursor.execute("SELECT * FROM Usuario WHERE email = 'master@admin.com'")
    if not cursor.fetchone():
        cursor.execute("""
        INSERT INTO Usuario (nome, email, senha, tipo)
        VALUES (?, ?, ?, ?)
        """, ('Administrador Master', 'master@admin.com', 'admin123', 'administrador'))

    conexao.commit()
    conexao.close()


# Executa a criação das tabelas ao iniciar o sistema
criar_tabelas()


def adicionar_usuario(nome, email, senha, tipo):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO Usuario (nome, email, senha, tipo)
    VALUES (?, ?, ?, ?)
    """, (nome, email, senha, tipo))
    conn.commit()
    conn.close()


def verificar_login(email, senha):
    conn = conectar()
    cursor = conn.cursor()

    # Verificar se o usuário existe com o email fornecido e se a senha confere
    cursor.execute("""
    SELECT * FROM Usuario WHERE email = ? AND senha = ?
    """, (email, senha))

    # Se houver um resultado, retorna o usuário, senão, retorna None
    usuario = cursor.fetchone()
    conn.close()

    if usuario:
        return usuario  # Retorna os dados do usuário (tupla)
    else:
        return None  # Se não encontrar, retorna None