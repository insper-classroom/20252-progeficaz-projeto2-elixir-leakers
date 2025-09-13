import pytest
import validators

def test_validar_imovel_valido_transforma_valor_em_float():
    payload = {"logradouro":"Rua X","cidade":"SP","tipo":"casa","valor":"123.45"}
    ok, data = validators.validar_imovel(payload, parcial=False)
    assert ok is True
    assert isinstance(data["valor"], float)
    assert data["valor"] == 123.45

@pytest.mark.parametrize("faltando", [
    ({"cidade":"SP","tipo":"casa","valor":100}),
    ({"logradouro":"Rua X","tipo":"casa","valor":100}),
    ({"logradouro":"Rua X","cidade":"SP","valor":100}),
    ({"logradouro":"Rua X","cidade":"SP","tipo":"casa"}) 
])
def test_validar_imovel_falta_obrigatorio(faltando):
    ok, msg = validators.validar_imovel(faltando, parcial=False)
    assert ok is False
    assert "Campos obrigatórios" in msg

@pytest.mark.parametrize("valor_invalido", ["abc", "", None])
def test_validar_imovel_valor_invalido(valor_invalido):
    payload = {"logradouro":"Rua X","cidade":"SP","tipo":"casa","valor":valor_invalido}
    ok, msg = validators.validar_imovel(payload, parcial=False)
    assert ok is False
    assert "valor" in msg

@pytest.mark.parametrize("data", ["2024-13-01", "24-01-01", "2024/01/01"])
def test_validar_imovel_data_invalida(data):
    payload = {"logradouro":"Rua X","cidade":"SP","tipo":"casa","valor":100,"data_aquisicao":data}
    ok, msg = validators.validar_imovel(payload, parcial=False)
    assert ok is False
    assert "data_aquisicao" in msg

def test_validar_imovel_parcial_nao_exige_obrigatorios():
    ok, data = validators.validar_imovel({"valor":"77"}, parcial=True)
    assert ok is True
    assert data["valor"] == 77.0
