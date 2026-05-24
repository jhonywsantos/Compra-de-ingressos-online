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