import pytest
import api

def test_post_imovel_ok(client, monkeypatch):
    payload = {"logradouro":"Rua X","cidade":"SP","tipo":"casa","valor":100.0}

    monkeypatch.setattr(api.validators, "validar_imovel", lambda p, parcial: (True, payload))

    monkeypatch.setattr(api.repository, "criar", lambda data: 123)
    monkeypatch.setattr(api.repository, "buscar_por_id", lambda _id: dict(id=_id, **payload))

    resp = client.post("/imoveis", json=payload)   
    assert resp.status_code == 201
    assert "Location" in resp.headers
    body = resp.get_json()
    assert body["id"] == 123
    assert body["cidade"] == "SP"

def test_post_imovel_content_type_errado(client):
    resp = client.post("/imoveis", data="nao-json", headers={"Content-Type":"text/plain"})
    assert resp.status_code == 415

@pytest.mark.parametrize("payload", [
    {"cidade":"SP","tipo":"casa","valor":100},  
    {"logradouro":"Rua X","tipo":"casa","valor":100},  
])
def test_post_imovel_invalido_pelo_validador(client, monkeypatch, payload):
    monkeypatch.setattr(api.validators, "validar_imovel", lambda p, parcial: (False, "Campos obrigatórios ausentes"))
    resp = client.post("/imoveis", json=payload)
    assert resp.status_code == 400
