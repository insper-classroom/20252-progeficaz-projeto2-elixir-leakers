from unittest.mock import patch, ANY
from api import app

def test_obter_imoveis():
    fake_data = [
        {
            "id": 1,
            "logradouro": "Nicole Common",
            "tipo_logradouro": "Travessa",
            "bairro": "Lake Danielle",
            "cidade": "Judymouth",
            "cep": "85184",
            "tipo": "casa em condominio",
            "valor": 488423.52,
            "data_aquisicao": "2017-07-29"
        },
        {
            "id": 2,
            "logradouro": "Price Prairie",
            "tipo_logradouro": "Travessa",
            "bairro": "Colonton",
            "cidade": "North Garyville",
            "cep": "93354",
            "tipo": "casa em condominio",
            "valor": 260069.89,
            "data_aquisicao": "2021-11-30"
        },
    ]

    with patch("api.repository.listar_com_filtros", return_value=fake_data) as mock_listar:
        client = app.test_client()
        resp = client.get("/imoveis")

        assert resp.status_code == 200
        body = resp.get_json()

        esperado = [dict(item, _links=ANY) for item in fake_data]
        assert body == esperado

        mock_listar.assert_called_once_with({})
