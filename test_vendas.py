"""
test_vendas.py - Testes de vendas.

Execucao: pytest test_vendas.py -v
"""

from test_conftest import client

_cpf_counter = [10000000000]


def _fixture(label: str):
    """Cria um cliente e um medicamento e retorna seus IDs."""
    _cpf_counter[0] += 1
    cpf = str(_cpf_counter[0])

    cli = client.post("/api/clientes", json={"cpf": cpf, "nome": f"Cliente {label}"})
    assert cli.status_code == 201, cli.json()

    med = client.post("/api/medicamentos", json={
        "nome": f"Remedio {label}", "principio_ativo": "Principio",
        "preco": 10.00, "estoque": 100, "lote": f"LT{label}",
        "data_validade": "2026-12-31",
    })
    assert med.status_code == 201, med.json()
    return cli.json()["id"], med.json()["id"]


def _venda(cliente_id, med_id, qtd=2):
    return client.post("/api/vendas", json={
        "id_cliente": cliente_id,
        "desconto": 0,
        "itens": [{"id_medicamento": med_id,
                   "quantidade": qtd,
                   "preco_unitario": 10.00}],
    })


class TestVendas:

    def test_criar_venda(self):
        cli_id, med_id = _fixture("V01")
        r = _venda(cli_id, med_id)
        assert r.status_code == 201
        assert r.json()["total"] == 20.0

    def test_estoque_insuficiente(self):
        cli_id, med_id = _fixture("V02")
        r = _venda(cli_id, med_id, qtd=9999)
        assert r.status_code == 400

    def test_deletar_restaura_estoque(self):
        cli_id, med_id = _fixture("V03")
        estoque_antes = client.get(f"/api/medicamentos/{med_id}").json()["estoque"]
        vid = _venda(cli_id, med_id, qtd=5).json()["id"]
        client.delete(f"/api/vendas/{vid}")
        estoque_depois = client.get(f"/api/medicamentos/{med_id}").json()["estoque"]
        assert estoque_depois == estoque_antes

    def test_listar_vendas(self):
        r = client.get("/api/vendas")
        assert r.status_code == 200
        assert isinstance(r.json(), list)


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
