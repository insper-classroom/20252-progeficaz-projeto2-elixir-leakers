from flask import Flask, request, jsonify, url_for, make_response
import repository, validators

app = Flask(__name__)

def with_links(item):
    iid = item["id"]
    item = dict(item) 
    item["_links"] = {
        "self":   {"href": url_for("obter_imovel", id=iid, _external=True)},
        "update": {"href": url_for("atualizar_imovel", id=iid, _external=True), "method": "PUT"},
        "delete": {"href": url_for("remover_imovel", id=iid, _external=True), "method": "DELETE"},
    }
    return item


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
    lista_com_links = [with_links(x) for x in lista] 
    return jsonify(lista_com_links), 200


@app.route('/imoveis/<int:id>', methods=['GET'])
def obter_imovel(id):
    item = repository.buscar_por_id(id)
    if not item:
        return jsonify({"error": "Não encontrado"}), 404
    return jsonify(with_links(item)), 200  


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
    resp = make_response(jsonify(with_links(criado)), 201) 
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

    data = data_or_err

    atualizado = repository.atualizar_total(id, data)
    if not atualizado:
        return jsonify({"error": "Não encontrado"}), 404

    return jsonify(with_links(atualizado)), 200  


@app.route('/imoveis/<int:id>', methods=['DELETE'])
def remover_imovel(id):
    if not repository.buscar_por_id(id):
        return jsonify({"error": "Não encontrado"}), 404

    ok = repository.remover(id)
    if not ok:
        return jsonify({"error": "Não encontrado"}), 404

    return "", 204


@app.errorhandler(404)
def _404(_):
    return jsonify({"error": "Não encontrado"}), 404

@app.errorhandler(400)
def _400(err):
    return jsonify({"error": "Requisição inválida", "details": str(err)}), 400
 
if __name__ == '__main__':
    app.run(debug=True)
