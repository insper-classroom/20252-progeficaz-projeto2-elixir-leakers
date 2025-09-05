from db import query_all

def listar(tipo=None, cidade=None):
    sql = "SELECT * FROM imoveis"
    params = []
    clauses = []

    if tipo:
        clauses.append("LOWER(tipo) = LOWER(?)")
        params.append(tipo)

    if cidade:
        clauses.append("LOWER(cidade) = LOWER(?)")
        params.append(cidade)

    if clauses:
        sql += " WHERE " + " AND ".join(clauses)

    sql += " ORDER BY id"

    return query_all(sql, params)

from db import query_all

# Lista de colunas que podem ser filtradas
ALLOWED = {
    "logradouro", "tipo_logradouro", "bairro", "cidade",
    "cep", "tipo", "valor", "data_aquisicao"
}

def listar_com_filtros(filtros: dict):
    sql = "SELECT * FROM imoveis"
    clauses = []
    params = []

    for chave, valor in filtros.items():
        if chave not in ALLOWED:
            continue  # ignora chaves inválidas

        # se for texto -> comparar sem diferenciar maiúscula/minúscula
        if chave in {"logradouro","tipo_logradouro","bairro","cidade","cep","tipo"}:
            clauses.append(f"LOWER({chave}) = LOWER(?)")
            params.append(valor)

        # se for valor -> comparação numérica
        elif chave == "valor":
            clauses.append("valor = ?")
            params.append(valor)

        # se for data -> igualdade direta (já validada como YYYY-MM-DD)
        elif chave == "data_aquisicao":
            clauses.append("data_aquisicao = ?")
            params.append(valor)

    if clauses:
        sql += " WHERE " + " AND ".join(clauses)

    sql += " ORDER BY id"
    return query_all(sql, params)

