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
    senha = getpass.getpass("Senha: ")
    usuarios[email] = {"nome": nome, "senha": senha}
    print("Usuário cadastrado com sucesso!")

def login():
    global usuario_logado
    print("\n--- Login ---")
    email = input("E-mail: ")
    senha = getpass.getpass("Senha: ")
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
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, abort, make_response, request
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

# =========================
# DADOS EM MEMÓRIA
# =========================

eventos = [
    {
        'id': 1,
        'nome': 'Show de Rock',
        'local': 'São Paulo',
        'ingressos_disponiveis': 100,
        'preco': 150.0
    },
    {
        'id': 2,
        'nome': 'Teatro Clássico',
        'local': 'Rio de Janeiro',
        'ingressos_disponiveis': 50,
        'preco': 80.0
    }
]

compras = []

# =========================
# LISTAR EVENTOS
# =========================
# curl -i http://localhost:5000/eventos
@app.route('/eventos', methods=['GET'])
def listar_eventos():
    return jsonify({'eventos': eventos})


# =========================
# DETALHAR EVENTO
# =========================
# curl -i http://localhost:5000/eventos/1
@app.route('/eventos/<int:idEvento>', methods=['GET'])
def detalhe_evento(idEvento):
    evento = [e for e in eventos if e['id'] == idEvento]
    if len(evento) == 0:
        abort(404)
    return jsonify({'evento': evento[0]})


# =========================
# CRIAR EVENTO
# =========================
# curl -i -H "Content-Type: application/json" -X POST -d '{"nome":"Festival","local":"SP"}' http://localhost:5000/eventos
@app.route('/eventos', methods=['POST'])
def criar_evento():
    if not request.json or not 'nome' in request.json:
        abort(400)

    evento = {
        'id': eventos[-1]['id'] + 1 if eventos else 1,
        'nome': request.json['nome'],
        'local': request.json.get('local', ""),
        'ingressos_disponiveis': request.json.get('ingressos_disponiveis', 0),
        'preco': request.json.get('preco', 0.0)
    }

    eventos.append(evento)
    return jsonify({'evento': evento}), 201


# =========================
# ATUALIZAR EVENTO
# =========================
# curl -i -X PUT -H "Content-Type: application/json" -d '{"preco":200}' http://localhost:5000/eventos/1
@app.route('/eventos/<int:idEvento>', methods=['PUT'])
def atualizar_evento(idEvento):
    evento = [e for e in eventos if e['id'] == idEvento]
    if len(evento) == 0:
        abort(404)

    if not request.json:
        abort(400)

    evento[0]['nome'] = request.json.get('nome', evento[0]['nome'])
    evento[0]['local'] = request.json.get('local', evento[0]['local'])
    evento[0]['preco'] = request.json.get('preco', evento[0]['preco'])
    evento[0]['ingressos_disponiveis'] = request.json.get(
        'ingressos_disponiveis',
        evento[0]['ingressos_disponiveis']
    )

    return jsonify({'evento': evento[0]})


# =========================
# EXCLUIR EVENTO
# =========================
# curl -i -X DELETE http://localhost:5000/eventos/1
@app.route('/eventos/<int:idEvento>', methods=['DELETE'])
def excluir_evento(idEvento):
    evento = [e for e in eventos if e['id'] == idEvento]
    if len(evento) == 0:
        abort(404)

    eventos.remove(evento[0])
    return jsonify({'resultado': True})


# =========================
# COMPRAR INGRESSO
# =========================
# curl -i -X POST -H "Content-Type: application/json" -d '{"evento_id":1, "quantidade":2}' http://localhost:5000/comprar
@app.route('/comprar', methods=['POST'])
def comprar_ingresso():
    if not request.json or not 'evento_id' in request.json:
        abort(400)

    evento = [e for e in eventos if e['id'] == request.json['evento_id']]
    if len(evento) == 0:
        abort(404)

    quantidade = request.json.get('quantidade', 1)

    if evento[0]['ingressos_disponiveis'] < quantidade:
        return jsonify({'erro': 'Ingressos insuficientes'}), 400

    evento[0]['ingressos_disponiveis'] -= quantidade

    compra = {
        'id': len(compras) + 1,
        'evento_id': evento[0]['id'],
        'quantidade': quantidade
    }

    compras.append(compra)

    return jsonify({'compra': compra}), 201


# =========================
# CANCELAR COMPRA
# =========================
# curl -i -X DELETE http://localhost:5000/comprar/1
@app.route('/comprar/<int:idCompra>', methods=['DELETE'])
def cancelar_compra(idCompra):
    compra = [c for c in compras if c['id'] == idCompra]
    if len(compra) == 0:
        abort(404)

    evento = [e for e in eventos if e['id'] == compra[0]['evento_id']]
    evento[0]['ingressos_disponiveis'] += compra[0]['quantidade']

    compras.remove(compra[0])

    return jsonify({'resultado': True})


# =========================
# LISTAR COMPRAS (PROTEGIDO)
# =========================
# curl -u usuario:123 -i http://localhost:5000/compras
@app.route('/compras', methods=['GET'])
@auth.login_required
def listar_compras():
    return jsonify({'compras': compras})


# =========================
# AUTENTICAÇÃO
# =========================
@auth.get_password
def get_password(username):
    if username == 'usuario':
        return '123'
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'erro': 'Acesso Negado'}), 403)


# =========================
# ERRO 404
# =========================
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'erro': 'Recurso não encontrado'}), 404)


# =========================
# EXECUÇÃO
# =========================
if __name__ == '__main__':
    print("Servidor de Ingressos Online rodando...")
    app.run(host='0.0.0.0', debug=True)