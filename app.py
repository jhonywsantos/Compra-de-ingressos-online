# --- Módulos principais do sistema de compra de ingressos ---
import getpass

# Dados simulados em memória
usuarios = {}
eventos = []
compras = []
usuario_logado = None

# --- Cadastro e autenticação de usuário ---
def cadastrar_usuario():
    print("\n--- Cadastro de Usuário ---")
    email = input("E-mail: ")
    if email in usuarios:
        print("Usuário já cadastrado!")
        return
    nome = input("Nome: ")
    senha = input("Senha: ")
    usuarios[email] = {"nome": nome, "senha": senha}
    print("Usuário cadastrado com sucesso!")

def login():
    global usuario_logado
    print("\n--- Login ---")
    email = input("E-mail: ")
    senha = input("Senha: ")
    user = usuarios.get(email)
    if user and user["senha"] == senha:
        usuario_logado = email
        print(f"Bem-vindo, {user['nome']}!")
    else:
        print("E-mail ou senha incorretos!")

def logout():
    global usuario_logado
    usuario_logado = None
    print("Logout realizado com sucesso.")

# --- Gestão de eventos ---
def cadastrar_evento():
    print("\n--- Cadastro de Evento ---")
    nome = input("Nome do evento: ")
    data = input("Data (dd/mm/aaaa): ")
    local = input("Local: ")
    preco = float(input("Preço do ingresso: R$ "))
    qtd = int(input("Quantidade de ingressos disponíveis: "))
    evento = {"nome": nome, "data": data, "local": local, "preco": preco, "qtd": qtd}
    eventos.append(evento)
    print("Evento cadastrado com sucesso!")

def listar_eventos():
    print("\n--- Eventos Disponíveis ---")
    if not eventos:
        print("Nenhum evento cadastrado.")
        return
    for idx, ev in enumerate(eventos, 1):
        print(f"{idx}. {ev['nome']} | {ev['data']} | {ev['local']} | R$ {ev['preco']:.2f} | Ingressos: {ev['qtd']}")

# --- Compra de ingressos ---
def comprar_ingresso():
    if usuario_logado is None:
        print("Você precisa estar logado para comprar ingressos.")
        return
    listar_eventos()
    if not eventos:
        return
    try:
        escolha = int(input("Escolha o número do evento: "))
        evento = eventos[escolha-1]
    except (ValueError, IndexError):
        print("Evento inválido.")
        return
    print(f"Evento selecionado: {evento['nome']}")
    print(f"Ingressos disponíveis: {evento['qtd']}")
    qtd = int(input("Quantidade de ingressos: "))
    if qtd <= 0 or qtd > evento['qtd']:
        print("Quantidade inválida.")
        return
    total = qtd * evento['preco']
    print(f"Valor total: R$ {total:.2f}")
    confirm = input("Confirmar compra? (s/n): ").lower()
    if confirm == 's':
        evento['qtd'] -= qtd
        compras.append({"usuario": usuario_logado, "evento": evento['nome'], "qtd": qtd, "total": total})
        print("Compra realizada com sucesso!")
    else:
        print("Compra cancelada.")

# --- Menu principal ---
def menu():
    while True:
        print("\n==== Sistema de Compra de Ingressos ====")
        print("1. Cadastrar usuário")
        print("2. Login")
        print("3. Logout")
        print("4. Cadastrar evento")
        print("5. Listar eventos")
        print("6. Comprar ingresso")
        print("0. Sair")
        opcao = input("Escolha uma opção: ")
        if opcao == '1':
            cadastrar_usuario()
        elif opcao == '2':
            login()
        elif opcao == '3':
            logout()
        elif opcao == '4':
            cadastrar_evento()
        elif opcao == '5':
            listar_eventos()
        elif opcao == '6':
            comprar_ingresso()
        elif opcao == '0':
            print("Saindo...")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu()