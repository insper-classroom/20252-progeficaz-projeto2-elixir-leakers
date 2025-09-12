import re

def validar_imovel(payload: dict, parcial: bool = False) -> tuple[bool, dict | str]:
    """
    Valida os dados de um imóvel.
    - payload: dicionário vindo do cliente (JSON já convertido)
    - parcial: False = todos obrigatórios (POST), True = pode faltar campos (PATCH/PUT)
    Retorna:
      (True, dados_normalizados) se ok
      (False, "mensagem de erro") se inválido
    """

    data = dict(payload)  # copia para não mexer no original

    # 1) Nunca permitir 'id' no payload
    if "id" in data:
        data.pop("id")

    # 2) Campos obrigatórios (apenas no POST = parcial=False)
    obrigatorios = {"logradouro", "cidade", "tipo", "valor"}
    if not parcial:
        faltando = [campo for campo in obrigatorios if campo not in data or str(data[campo]).strip() == ""]
        if faltando:
            return False, f"Campos obrigatórios ausentes: {', '.join(faltando)}"

    # 3) Converter e validar 'valor'
    if "valor" in data:
        try:
            data["valor"] = float(data["valor"])
        except (TypeError, ValueError):
            return False, "O campo 'valor' deve ser numérico"
        if data["valor"] < 0:
            return False, "O campo 'valor' deve ser positivo"

    # 4) Validar data (se existir)
    if "data_aquisicao" in data and data["data_aquisicao"] is not None:
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", str(data["data_aquisicao"])):
            return False, "O campo 'data_aquisicao' deve estar no formato YYYY-MM-DD"

    # 5) Limpar strings (tirar espaços extras)
    for chave, valor in list(data.items()):
        if isinstance(valor, str):
            data[chave] = valor.strip()

    return True, data
