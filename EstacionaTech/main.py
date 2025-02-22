from database.database import adicionar_usuario, criar_tabelas, verificar_login

def menu_operador():
    print("\nMenu do Operador:")
    print("1. Visualizar Estacionamento")
    print("2. Registrar Entrada de Veículo")
    print("3. Registrar Saída de Veículo")
    print("4. Sair")

def menu_administrativo():
    print("\nMenu do Administrador:")
    print("1. Visualizar Estacionamento")
    print("2. Registrar Entrada de Veículo")
    print("3. Registrar Saída de Veículo")
    print("4. Adicionar Usuário")  # Nova opção para adicionar um usuário
    print("5. Sair")

    opcao = input("\nEscolha uma opção: ")

    if opcao == '1':
        pass
    elif opcao == '2':
        pass
    elif opcao == '3':
        pass
    elif opcao == '4':
        nome = input("Digite o nome do usuário: ")
        email = input("Digite o email do usuário: ")
        senha = input("Digite a senha do usuário: ")
        tipo = input("Digite o tipo do usuário (administrador/operador): ")
        adicionar_usuario(nome, email, senha, tipo)
        print("\nUsuário adicionado com sucesso!")
    elif opcao == '5':
        print("Saindo do menu...")
    else:
        print("Opção inválida. Tente novamente.")

def cadastrar_operador():
    nome = input("Nome do operador: ")
    email = input("Email do operador: ")
    senha = input("Senha do operador: ")
    adicionar_usuario(nome, email, senha, 'operador')
    print("Operador cadastrado com sucesso!")

# Função para iniciar o sistema após o login
def iniciar_sistema(usuario):
    if usuario[4] == 'operador':
        menu_operador()
    elif usuario[4] == 'administrador':
        menu_administrativo()

def main():
    criar_tabelas()  # Cria as tabelas se não existirem

    # Realizando o login
    print("Bem-vindo ao EstacionaTech!")
    email = input("Email: ")
    senha = input("Senha: ")

    usuario = verificar_login(email, senha)
    if usuario:
        print(f"\nLogin bem-sucedido! Bem-vindo, {usuario[1]} ({usuario[2]})")
        iniciar_sistema(usuario)
    else:
        print("Credenciais inválidas. Tente novamente.")

if __name__ == "__main__":
    main()