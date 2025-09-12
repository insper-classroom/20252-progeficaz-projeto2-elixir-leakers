import api

def test_delete_imovel_ok(client, monkeypatch):
    monkeypatch.setattr(api.repository, "buscar_por_id", lambda _id: {"id":_id})
    monkeypatch.setattr(api.repository, "remover", lambda _id: True)

    resp = client.delete("/imoveis/3")
    assert resp.status_code == 204
    assert resp.data == b""

def test_delete_imovel_inexistente(client, monkeypatch):
    monkeypatch.setattr(api.repository, "buscar_por_id", lambda _id: None)
    resp = client.delete("/imoveis/9999")
    assert resp.status_code == 404
