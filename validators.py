import re
from datetime import datetime

def validar_imovel(payload: dict, parcial: bool = False) -> tuple[bool, dict | str]:
    """
    Valida os dados de um imóvel.
    - payload: dicionário vindo do cliente (JSON já convertido)
    - parcial: False = todos obrigatórios (POST/PUT), True = pode faltar campos (PATCH)
    Retorna:
      (True, dados_normalizados) se ok
      (False, "mensagem de erro") se inválido
    """

    data = dict(payload)  # cópia para não mexer no original

    # 1) Nunca permitir 'id' no payload
    if "id" in data:
        data.pop("id")

    # 2) Campos obrigatórios (apenas no POST/PUT = parcial=False)
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
        s = str(data["data_aquisicao"]).strip()

        # valida formato básico
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", s):
            return False, "O campo 'data_aquisicao' deve estar no formato YYYY-MM-DD"

        # valida se a data é real (sem mês 13, dia 32 etc.)
        try:
            datetime.strptime(s, "%Y-%m-%d")
        except ValueError:
            return False, "O campo 'data_aquisicao' não representa uma data válida (YYYY-MM-DD)"

        # normaliza
        data["data_aquisicao"] = s

    # 5) Limpar strings (tirar espaços extras)
    for chave, valor in list(data.items()):
        if isinstance(valor, str):
            data[chave] = valor.strip()

    return True, data
