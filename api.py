from flask import Flask, request, jsonify, url_for, make_response 
import repository

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
    
    filtros = {k: v for k, v in parametros.items() if v not in (None, "", " ")}
    
    lista = repository.listar_com_filtros(filtros)
    
    return jsonify(lista), 200


# 2) GET /imoveis/<id>
@app.route('/imoveis/<int:id>', methods=['GET'])
def obter_imovel(id):
    # 1. buscar item por id
    # 2a. se achar: return jsonify(item), 200
    # 2b. se não:  return jsonify({"error": "Não encontrado"}), 404
    ...

# 3) POST /imoveis
@app.route('/imoveis', methods=['POST'])
def criar_imovel():
    # 1. checar Content-Type (request.is_json) → 415 se errado
    # 2. ler JSON (request.get_json) → validar campos obrigatórios/tipos → 400 se inválido
    # 3. inserir registro (definir id) 
    # 4. montar resposta 201 com Location apontando para /imoveis/<id_novo>
    #    resp = make_response(jsonify(criado), 201)
    #    resp.headers['Location'] = url_for('obter_imovel', id=novo_id, _external=True)
    #    return resp
    ...

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