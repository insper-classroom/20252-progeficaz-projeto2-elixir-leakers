import api
import pytest

def test_put_imovel_ok(client, monkeypatch):
    monkeypatch.setattr(api.repository, "buscar_por_id", lambda _id: {"id": _id})
    payload_norm = {"logradouro":"Rua X","cidade":"SP","tipo":"casa","valor":123.0}
    monkeypatch.setattr(api.validators, "validar_imovel", lambda p, parcial: (True, payload_norm))
    monkeypatch.setattr(api.repository, "atualizar_total",
                        lambda _id, data: dict(id=_id, **data))

    resp = client.put("/imoveis/5", json={"logradouro":"Rua X","cidade":"SP","tipo":"casa","valor":123})
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["id"] == 5
    assert body["valor"] == 123.0

def test_put_imovel_inexistente(client, monkeypatch):
    monkeypatch.setattr(api.repository, "buscar_por_id", lambda _id: None)
    resp = client.put("/imoveis/999", json={"logradouro":"A","cidade":"B","tipo":"casa","valor":1})
    assert resp.status_code == 404

def test_put_imovel_content_type_errado(client):
    resp = client.put("/imoveis/1", data="texto", headers={"Content-Type":"text/plain"})
    assert resp.status_code == 415

@pytest.mark.parametrize("payload", [
    {"cidade":"SP","tipo":"casa","valor":1},           
    {"logradouro":"A","tipo":"casa","valor":1},        
    {"logradouro":"A","cidade":"SP","valor":1},        
    {"logradouro":"A","cidade":"SP","tipo":"casa"}     
])
def test_put_imovel_invalido(client, monkeypatch, payload):
    monkeypatch.setattr(api.repository, "buscar_por_id", lambda _id: {"id": _id})
    monkeypatch.setattr(api.validators, "validar_imovel", lambda p, parcial: (False, "Campos obrigatórios ausentes"))
    resp = client.put("/imoveis/1", json=payload)
    assert resp.status_code == 400
