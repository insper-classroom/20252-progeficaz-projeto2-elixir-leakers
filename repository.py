from db import query_all, query_one, execute

def listar(tipo=None, cidade=None):
    sql = "SELECT * FROM imoveis"
    params = []
    clauses = []

    if tipo:
        clauses.append("LOWER(tipo) = LOWER(%s)")
        params.append(tipo)

    if cidade:
        clauses.append("LOWER(cidade) = LOWER(%s)")
        params.append(cidade)

    if clauses:
        sql += " WHERE " + " AND ".join(clauses)

    sql += " ORDER BY id"
    return query_all(sql, params)

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
            continue

        if chave in {"logradouro", "tipo_logradouro", "bairro", "cidade", "cep", "tipo"}:
            clauses.append(f"LOWER({chave}) = LOWER(%s)")
            params.append(valor)

        elif chave == "valor":
            clauses.append("valor = %s")
            params.append(valor)

        elif chave == "data_aquisicao":
            clauses.append("data_aquisicao = %s")
            params.append(valor)

    if clauses:
        sql += " WHERE " + " AND ".join(clauses)

    sql += " ORDER BY id"
    return query_all(sql, params)

def buscar_por_id(id_: int):
    sql = "SELECT * FROM imoveis WHERE id = %s"
    return query_one(sql, (id_,))

def criar(data: dict) -> int:

    fields = [k for k in data.keys() if k in ALLOWED]
    if not fields:
        raise ValueError("Nenhum campo válido para inserir.")

    placeholders = ", ".join(["%s"] * len(fields))
    columns = ", ".join(fields)
    values = [data[k] for k in fields]

    sql = f"INSERT INTO imoveis ({columns}) VALUES ({placeholders})"
    new_id, _ = execute(sql, values)
    return new_id

def atualizar_total(id_: int, data: dict):
    if not buscar_por_id(id_):
        return None

    cols = sorted(list(ALLOWED))  
    set_parts = [f"{col} = %s" for col in cols]
    params = [data.get(col) for col in cols] + [id_]

    sql = f"UPDATE imoveis SET {', '.join(set_parts)} WHERE id = %s"
    _, rowcount = execute(sql, params)
    if rowcount == 0:
        return None

    return buscar_por_id(id_)

def remover(id_: int) -> bool:
    _, rowcount = execute("DELETE FROM imoveis WHERE id = %s", (id_,))
    return rowcount > 0
