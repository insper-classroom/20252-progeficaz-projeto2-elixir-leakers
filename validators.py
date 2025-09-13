import re
from datetime import datetime

def validar_imovel(payload: dict, parcial: bool = False) -> tuple[bool, dict | str]:
    data = dict(payload)  
    
    if "id" in data:
        data.pop("id")

   
    obrigatorios = {"logradouro", "cidade", "tipo", "valor"}
    if not parcial:
        faltando = [campo for campo in obrigatorios if campo not in data or str(data[campo]).strip() == ""]
        if faltando:
            return False, f"Campos obrigatórios ausentes: {', '.join(faltando)}"


    if "valor" in data:
        try:
            data["valor"] = float(data["valor"])
        except (TypeError, ValueError):
            return False, "O campo 'valor' deve ser numérico"
        if data["valor"] < 0:
            return False, "O campo 'valor' deve ser positivo"

    if "data_aquisicao" in data and data["data_aquisicao"] is not None:
        s = str(data["data_aquisicao"]).strip()

        if not re.match(r"^\d{4}-\d{2}-\d{2}$", s):
            return False, "O campo 'data_aquisicao' deve estar no formato YYYY-MM-DD"

        try:
            datetime.strptime(s, "%Y-%m-%d")
        except ValueError:
            return False, "O campo 'data_aquisicao' não representa uma data válida (YYYY-MM-DD)"

        data["data_aquisicao"] = s

    for chave, valor in list(data.items()):
        if isinstance(valor, str):
            data[chave] = valor.strip()

    return True, data
