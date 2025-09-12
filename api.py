from flask import Flask, request, jsonify, url_for, make_response 
import repository, validators

app = Flask(__name__)



# 2) GET /imoveis/<id>
@app.route('/imoveis/<int:id>', methods=['GET'])
def obter_imovel(id):
    item = repository.buscar_por_id(id)
    if not item:
        return jsonify({"error": "Não encontrado"}), 404
    return jsonify(item), 200


# 3) POST /imoveis
@app.route('/imoveis', methods=['POST'])
def criar_imovel():
    if not request.is_json:
        return jsonify({"error": "Content-Type deve ser application/json"}), 415

    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify({"error": "JSON inválido"}), 400

    ok, data_or_err = validators.validar_imovel(payload, parcial=False)
    if not ok:
        return jsonify({"error": data_or_err}), 400
    data = data_or_err

    try:
        novo_id = repository.criar(data)
    except Exception as e:
        return jsonify({"error": "Falha ao criar", "details": str(e)}), 400

    criado = repository.buscar_por_id(novo_id)
    resp = make_response(jsonify(criado), 201)
    resp.headers['Location'] = url_for('obter_imovel', id=novo_id, _external=True)
    return resp


@app.route('/imoveis/<int:id>', methods=['PUT'])
def atualizar_imovel(id):
    if not request.is_json:
        return jsonify({"error": "Content-Type deve ser application/json"}), 415

    if not repository.buscar_por_id(id):
        return jsonify({"error": "Não encontrado"}), 404

    payload = request.get_json(silent=True) or {}
    ok, data_or_err = validators.validar_imovel(payload, parcial=False)
    if not ok:
        return jsonify({"error": data_or_err}), 400

    data = data_or_err  # <<< GARANTA ESSA LINHA (não passe a tupla para o repo)

    atualizado = repository.atualizar_total(id, data)
    if not atualizado:
        return jsonify({"error": "Não encontrado"}), 404

    return jsonify(atualizado), 200


@app.route('/imoveis/<int:id>', methods=['DELETE'])
def remover_imovel(id):
    # checa existência explícita
    if not repository.buscar_por_id(id):
        return jsonify({"error": "Não encontrado"}), 404

    ok = repository.remover(id)
    if not ok:
        # se rowcount = 0 (corrida), também 404
        return jsonify({"error": "Não encontrado"}), 404

    return "", 204
 
if __name__ == '__main__':
    app.run(debug=True)