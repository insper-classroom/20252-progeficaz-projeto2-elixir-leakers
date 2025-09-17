Projeto RestAPI desenvolvido por Gabriel Rosa e Lucas Bressanin

Grupo: Elixir Leakers

# API de Imóveis 🏠

API RESTful em Flask para gerenciar imóveis. O projeto segue TDD (pytest), utiliza MySQL (Aiven) em produção e oferece CRUD completo.

## ✨ Funcionalidades

- `GET /imoveis`: lista imóveis (com filtros por query params)
- `GET /imoveis/<id>`: busca um imóvel pelo id
- `POST /imoveis`: cria um novo imóvel
- `PUT /imoveis/<id>`: atualiza **toda** a representação do imóvel
- `DELETE /imoveis/<id>`: remove um imóvel

## 🌐 API em Produção

A API está rodando publicamente em:

🔗 http://54.196.232.66/

## 🧰 Stack

- Python 3.10+, Flask
- PyMySQL (MySQL – Aiven)
- pytest (TDD)
- Postman (testes manuais)

## 📦 Requisitos

- Python 3.10+
- `pip` e `venv` (ou Pipenv)
- Acesso a um banco MySQL (Aiven)

## 🚀 Como rodar localmente

```bash
git clone <URL_DO_REPO>
cd <PASTA_DO_REPO>

python -m venv venv
# Linux/Mac
source venv/bin/activate
# Windows
venv\Scripts\activate

pip install -r requirements.txt



