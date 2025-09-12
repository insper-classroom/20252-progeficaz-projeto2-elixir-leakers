from flask import Flask, request, jsonify, url_for, make_response 
import repository, validators

app = Flask(__name__)

# 1) GET /imoveis  (com filtros por query params)
@app.route('/imoveis', methods=['GET'])
def listar_imoveis():
    parametros = {
        "id": request.args.get("id"),
        "logradouro": request.args.get("logradouro"),
        "tipo_logradouro": request.args.get("tipo_logradouro"),
        "bairro": request.args.get("bairro"),   
        "cidade": request.args.get("cidade"),
        "cep": request.args.get("cep"),
        "tipo": request.args.get("tipo"),
        "valor": request.args.get("valor"),
        "data_aquisicao": request.args.get("data_aquisicao"),
    }
        
    lista = repository.listar(parametros)
    
    return jsonify(lista), 200


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
    # 1) Content-Type precisa ser JSON
    if not request.is_json:
        return jsonify({"error": "Content-Type deve ser application/json"}), 415

    # 2) Ler JSON com segurança
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify({"error": "JSON inválido"}), 400

    # 3) Validar e normalizar (obrigatórios, tipos, formatos)
    ok, data_or_err = validators.validar_imovel(payload, parcial=False)
    if not ok:
        return jsonify({"error": data_or_err}), 400
    data = data_or_err  # já vem com 'valor' como float, sem 'id', etc.

    # 4) Inserir via repositório
    try:
        novo_id = repository.criar(data)
    except Exception as e:
        # ajuste esse tratamento conforme seu schema (400/409/etc.)
        return jsonify({"error": "Falha ao criar", "details": str(e)}), 400

    # 5) Buscar o registro criado e devolver 201 + Location
    criado = repository.buscar_por_id(novo_id)
    resp = make_response(jsonify(criado), 201)
    resp.headers['Location'] = url_for('obter_imovel', id=novo_id, _external=True)
    return resp


# 4) PUT ou PATCH /imoveis/<id> (escolha sua semântica)
@app.route('/imoveis/<int:id>', methods=['PUT', 'PATCH'])
def atualizar_imovel(id):
    # 1. checar Content-Type e JSON
    # 2. buscar item por id → 404 se não existir
    # 3. validar dados (PUT: todos os campos; PATCH: só os enviados)
    # 4. ATENÇÃO: atualize o objeto/linha real (mutação), não reatribua variável local
    # 5. return jsonify(atualizado), 200
    ...


# 5) DELETE /imoveis/<id>
@app.route('/imoveis/<int:id>', methods=['DELETE'])
def remover_imovel(id):
    # 1. buscar item → 404 se não existir
    # 2. remover
    # 3. return '', 204  (ou jsonify({"message": "removido"}), 200)
    ...
 
if __name__ == '__main__':
    app.run(debug=True)