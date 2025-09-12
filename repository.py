from db import query_all, query_one, execute

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

def buscar_por_id(id_: int):
    """
    Busca um imóvel pelo id.
    Retorna um dict se existir, ou None se não existir.
    """
    sql = "SELECT * FROM imoveis WHERE id = ?"
    return query_one(sql, (id_,))

def criar(data: dict) -> int:
    """
    Insere um imóvel na tabela 'imoveis' e retorna o id gerado.
    'data' deve estar validado (sem 'id', tipos corretos).
    """
    # 1) Filtra apenas colunas conhecidas da tabela
    fields = [k for k in data.keys() if k in ALLOWED]
    if not fields:
        # não há nada para inserir
        raise ValueError("Nenhum campo válido para inserir.")

    # 2) Monta SQL dinâmico: INSERT INTO imoveis (colunas) VALUES (?, ?, ...)
    placeholders = ", ".join(["?"] * len(fields))
    columns = ", ".join(fields)
    values = [data[k] for k in fields]

    sql = f"INSERT INTO imoveis ({columns}) VALUES ({placeholders})"

    # 3) Executa e retorna o id gerado
    new_id, _ = execute(sql, values)
    return new_id

def atualizar_total(id_: int, data: dict):
    """
    PUT: substitui a representação inteira do imóvel.
    Campos não enviados em 'data' viram NULL (semântica de PUT).
    Retorna o registro final, ou None se o id não existir.
    """
    if not buscar_por_id(id_):
        return None

    # usa as colunas válidas do seu schema
    cols = list(ALLOWED)  # {"logradouro","tipo_logradouro","bairro","cidade","cep","tipo","valor","data_aquisicao"}
    cols.sort()  # só para manter ordem determinística (opcional)

    set_parts = [f"{col} = ?" for col in cols]
    params = [data.get(col) for col in cols]  # se não veio no body → None
    params.append(id_)

    sql = f"UPDATE imoveis SET {', '.join(set_parts)} WHERE id = ?"
    _, rowcount = execute(sql, params)
    if rowcount == 0:
        return None

    return buscar_por_id(id_)

def remover(id_: int) -> bool:
    _, rowcount = execute("DELETE FROM imoveis WHERE id = ?", (id_,))
    return rowcount > 0
