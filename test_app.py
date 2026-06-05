"""
test_app.py - Testes de medicamentos, clientes e fornecedores.

Execucao: pytest test_app.py test_vendas.py -v
"""

import pytest
from test_conftest import client


class TestMedicamentos:

    def test_criar(self):
        r = client.post("/api/medicamentos", json={
            "nome": "Dipirona 500mg", "principio_ativo": "Dipirona Monoidratada",
            "preco": 5.50, "estoque": 100, "lote": "LOT123",
            "data_validade": "2025-12-31",
        })
        assert r.status_code == 201
        assert r.json()["nome"] == "Dipirona 500mg"

    def test_listar(self):
        r = client.get("/api/medicamentos")
        assert r.status_code == 200
        assert isinstance(r.json(), list)

    def test_obter(self):
        med_id = client.post("/api/medicamentos", json={
            "nome": "Aspirina 100mg", "principio_ativo": "Acido Acetilsalicilico",
            "preco": 3.50, "estoque": 50, "lote": "LOT456",
            "data_validade": "2025-12-31",
        }).json()["id"]
        r = client.get(f"/api/medicamentos/{med_id}")
        assert r.status_code == 200
        assert r.json()["nome"] == "Aspirina 100mg"

    def test_atualizar(self):
        med_id = client.post("/api/medicamentos", json={
            "nome": "Vitamina C 1000mg", "principio_ativo": "Acido Ascorbico",
            "preco": 10.00, "estoque": 200, "lote": "LOT789",
            "data_validade": "2025-12-31",
        }).json()["id"]
        r = client.put(f"/api/medicamentos/{med_id}",
                       json={"preco": 9.99, "estoque": 150})
        assert r.status_code == 200
        assert r.json()["preco"] == 9.99

    def test_deletar(self):
        med_id = client.post("/api/medicamentos", json={
            "nome": "Ibuprofeno 400mg", "principio_ativo": "Ibuprofeno",
            "preco": 4.50, "estoque": 75, "lote": "LOT999",
            "data_validade": "2025-12-31",
        }).json()["id"]
        assert client.delete(f"/api/medicamentos/{med_id}").status_code == 204
        assert client.get(f"/api/medicamentos/{med_id}").status_code == 404

    def test_nome_duplicado(self):
        client.post("/api/medicamentos", json={
            "nome": "Medicamento Unico", "principio_ativo": "Principio X",
            "preco": 5.00, "estoque": 100, "lote": "LOT111",
            "data_validade": "2025-12-31",
        })
        r = client.post("/api/medicamentos", json={
            "nome": "Medicamento Unico", "principio_ativo": "Principio Y",
            "preco": 6.00, "estoque": 50, "lote": "LOT222",
            "data_validade": "2025-12-31",
        })
        assert r.status_code == 400


class TestClientes:

    def test_criar(self):
        r = client.post("/api/clientes", json={
            "cpf": "12345678901", "nome": "Joao Silva",
            "email": "joao@example.com",
        })
        assert r.status_code == 201
        assert r.json()["cpf"] == "12345678901"

    def test_cpf_duplicado(self):
        client.post("/api/clientes", json={"cpf": "11111111111", "nome": "Cliente Um"})
        r = client.post("/api/clientes", json={"cpf": "11111111111", "nome": "Cliente Dois"})
        assert r.status_code == 400

    def test_listar(self):
        r = client.get("/api/clientes")
        assert r.status_code == 200
        assert isinstance(r.json(), list)


class TestFornecedores:

    def test_criar(self):
        r = client.post("/api/fornecedores", json={
            "nome": "Industria Farmaceutica XYZ",
            "cnpj": "12345678000100",
        })
        assert r.status_code == 201
        assert r.json()["cnpj"] == "12345678000100"

    def test_cnpj_duplicado(self):
        client.post("/api/fornecedores", json={"nome": "Forn A", "cnpj": "99999999000100"})
        r = client.post("/api/fornecedores", json={"nome": "Forn B", "cnpj": "99999999000100"})
        assert r.status_code == 400


class TestHealth:

    def test_health_check(self):
        r = client.get("/health")
        assert r.status_code == 200
        assert r.json()["status"] == "OK"


if __name__ == "__main__":
    import pytest as _pytest
    _pytest.main([__file__, "-v"])
