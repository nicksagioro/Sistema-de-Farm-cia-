"""
populate_db.py - Popula o banco com dados de exemplo.

Uso: python populate_db.py
Requer a API rodando em http://localhost:8000.
"""

from datetime import datetime, timedelta
from api_client import APIClient

api = APIClient()
VALIDADE = (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")


def _post_lista(nome_secao: str, criar_fn, itens: list):
    print(f"\n{nome_secao}")
    for item in itens:
        try:
            criar_fn(item)
            print(f"  OK  {item.get('nome', item)}")
        except Exception as e:
            print(f"  ERRO  {item.get('nome', item)}: {e}")


def criar_fornecedores():
    _post_lista("Fornecedores", api.criar_fornecedor, [
        {"nome": "Industria Farmaceutica Brasil S.A.", "cnpj": "12345678000100",
         "telefone": "1133334444", "email": "contato@farmbrasil.com.br"},
        {"nome": "Medicamentos Genericos LTDA", "cnpj": "98765432000100",
         "telefone": "1144445555", "email": "vendas@medgenericos.com.br"},
        {"nome": "Pharma Distribuicao Nacional", "cnpj": "55443322000100",
         "telefone": "1155556666", "email": "distribuicao@pharma.com.br"},
        {"nome": "Vitaminas e Suplementos LTDA", "cnpj": "11223344000100",
         "telefone": "1166667777", "email": "vitaminas@suplement.com.br"},
        {"nome": "Antibioticos Especializados", "cnpj": "77788899000100",
         "telefone": "1177778888", "email": "antibioticos@especial.com.br"},
    ])


def criar_medicamentos():
    _post_lista("Medicamentos", api.criar_medicamento, [
        {"nome": "Dipirona 500mg",    "principio_ativo": "Dipirona Monoidratada",
         "preco": 5.50,  "estoque": 100, "lote": "LOT001", "data_validade": VALIDADE},
        {"nome": "Ibuprofeno 400mg",  "principio_ativo": "Ibuprofeno",
         "preco": 8.75,  "estoque": 75,  "lote": "LOT002", "data_validade": VALIDADE},
        {"nome": "Amoxicilina 500mg", "principio_ativo": "Amoxicilina Tri-hidratada",
         "preco": 12.50, "estoque": 50,  "lote": "LOT003", "data_validade": VALIDADE},
        {"nome": "Omeprazol 20mg",    "principio_ativo": "Omeprazol",
         "preco": 15.00, "estoque": 80,  "lote": "LOT004", "data_validade": VALIDADE},
        {"nome": "Vitamina C 1000mg", "principio_ativo": "Acido Ascorbico",
         "preco": 18.90, "estoque": 120, "lote": "LOT005", "data_validade": VALIDADE},
        {"nome": "Captopril 25mg",    "principio_ativo": "Captopril",
         "preco": 22.50, "estoque": 60,  "lote": "LOT006", "data_validade": VALIDADE},
        {"nome": "Metformina 500mg",  "principio_ativo": "Metformina",
         "preco": 10.00, "estoque": 150, "lote": "LOT007", "data_validade": VALIDADE},
        {"nome": "Loratadina 10mg",   "principio_ativo": "Loratadina",
         "preco": 14.50, "estoque": 90,  "lote": "LOT008", "data_validade": VALIDADE},
        {"nome": "Azitromicina 500mg","principio_ativo": "Azitromicina",
         "preco": 25.00, "estoque": 40,  "lote": "LOT009", "data_validade": VALIDADE},
        {"nome": "Cetirizina 10mg",   "principio_ativo": "Cetirizina HCl",
         "preco": 16.75, "estoque": 110, "lote": "LOT010", "data_validade": VALIDADE},
    ])


def criar_clientes():
    _post_lista("Clientes", api.criar_cliente, [
        {"cpf": "11144477788", "nome": "Joao Silva Santos",
         "email": "joao.silva@email.com",   "telefone": "11987654321"},
        {"cpf": "22255588899", "nome": "Maria Oliveira Costa",
         "email": "maria.oliveira@email.com","telefone": "11912345678"},
        {"cpf": "33366699900", "nome": "Carlos Mendes Pereira",
         "email": "carlos.mendes@email.com", "telefone": "11998765432"},
        {"cpf": "44477700011", "nome": "Ana Paula Ferreira",
         "email": "ana.paula@email.com",     "telefone": "11987123456"},
        {"cpf": "55588811122", "nome": "Pedro Goncalves Marques",
         "email": "pedro.goncalves@email.com","telefone": "11965432109"},
    ])


def criar_vendas():
    print("\nVendas")
    try:
        clientes = api.listar_clientes()
        meds     = api.listar_medicamentos()
        if not clientes or not meds:
            print("  AVISO  Sem clientes ou medicamentos suficientes.")
            return
        vendas = [
            {"id_cliente": clientes[0]["id"], "desconto": 0,
             "itens": [{"id_medicamento": meds[0]["id"], "quantidade": 2,
                        "preco_unitario": meds[0]["preco"]},
                       {"id_medicamento": meds[1]["id"], "quantidade": 1,
                        "preco_unitario": meds[1]["preco"]}]},
            {"id_cliente": clientes[1]["id"], "desconto": 5,
             "itens": [{"id_medicamento": meds[2]["id"], "quantidade": 1,
                        "preco_unitario": meds[2]["preco"]}]},
            {"id_cliente": clientes[2]["id"], "desconto": 0,
             "itens": [{"id_medicamento": meds[3]["id"], "quantidade": 3,
                        "preco_unitario": meds[3]["preco"]},
                       {"id_medicamento": meds[4]["id"], "quantidade": 2,
                        "preco_unitario": meds[4]["preco"]}]},
        ]
        for i, v in enumerate(vendas, 1):
            try:
                res = api.criar_venda(v)
                print(f"  OK  Venda #{i} - R$ {float(res['total']):.2f}")
            except Exception as e:
                print(f"  ERRO  Venda #{i}: {e}")
    except Exception as e:
        print(f"  ERRO  {e}")


def main():
    import requests as _r
    print("=" * 50)
    print("POPULACAO DO BANCO - FARMACIA")
    print("=" * 50)
    try:
        if _r.get("http://localhost:8000/health", timeout=5).status_code != 200:
            print("Erro ao conectar com a API.")
            return
        print("API conectada.\n")
    except Exception as e:
        print(f"API indisponivel: {e}")
        return

    criar_fornecedores()
    criar_medicamentos()
    criar_clientes()
    criar_vendas()
    print("\n" + "=" * 50)
    print("CONCLUIDO!")
    print("  Interface : python main.py")
    print("  Docs API  : http://localhost:8000/docs")


if __name__ == "__main__":
    main()
