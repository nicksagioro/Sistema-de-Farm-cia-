"""
Script para popular o banco de dados com dados de exemplo
Uso: python populate_db.py
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/api"

def criar_medicamentos():
    """Cria medicamentos de exemplo"""
    medicamentos = [
        {
            "nome": "Dipirona 500mg",
            "principio_ativo": "Dipirona Monoidratada",
            "preco": 5.50,
            "estoque": 100,
            "lote": "LOT2024001",
            "data_validade": (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d"),
            "fabricante": "Genérico Brasil",
            "descricao": "Analgésico e antitérmico"
        },
        {
            "nome": "Ibuprofeno 400mg",
            "principio_ativo": "Ibuprofeno",
            "preco": 8.75,
            "estoque": 75,
            "lote": "LOT2024002",
            "data_validade": (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d"),
            "fabricante": "Genérico Brasil",
            "descricao": "Anti-inflamatório e analgésico"
        },
        {
            "nome": "Amoxicilina 500mg",
            "principio_ativo": "Amoxicilina Tri-hidratada",
            "preco": 12.50,
            "estoque": 50,
            "lote": "LOT2024003",
            "data_validade": (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d"),
            "fabricante": "Antibiótico Plus",
            "descricao": "Antibiótico de amplo espectro"
        },
        {
            "nome": "Omeprazol 20mg",
            "principio_ativo": "Omeprazol",
            "preco": 15.00,
            "estoque": 80,
            "lote": "LOT2024004",
            "data_validade": (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d"),
            "fabricante": "Gastro Care",
            "descricao": "Bloqueador de ácido gástrico"
        },
        {
            "nome": "Vitamina C 1000mg",
            "principio_ativo": "Ácido Ascórbico",
            "preco": 18.90,
            "estoque": 120,
            "lote": "LOT2024005",
            "data_validade": (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d"),
            "fabricante": "Vitaminol",
            "descricao": "Suplemento vitamínico"
        },
        {
            "nome": "Captopril 25mg",
            "principio_ativo": "Captopril",
            "preco": 22.50,
            "estoque": 60,
            "lote": "LOT2024006",
            "data_validade": (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d"),
            "fabricante": "Cardio Control",
            "descricao": "Inibidor de ACE para pressão arterial"
        },
        {
            "nome": "Metformina 500mg",
            "principio_ativo": "Metformina",
            "preco": 10.00,
            "estoque": 150,
            "lote": "LOT2024007",
            "data_validade": (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d"),
            "fabricante": "Diabetes Control",
            "descricao": "Antidiabético oral"
        },
        {
            "nome": "Loratadina 10mg",
            "principio_ativo": "Loratadina",
            "preco": 14.50,
            "estoque": 90,
            "lote": "LOT2024008",
            "data_validade": (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d"),
            "fabricante": "Alergia Free",
            "descricao": "Anti-histamínico não sedativo"
        },
        {
            "nome": "Azitromicina 500mg",
            "principio_ativo": "Azitromicina",
            "preco": 25.00,
            "estoque": 40,
            "lote": "LOT2024009",
            "data_validade": (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d"),
            "fabricante": "Macro Antibiotic",
            "descricao": "Antibiótico macrolídeo"
        },
        {
            "nome": "Cetirizina 10mg",
            "principio_ativo": "Cetirizina HCl",
            "preco": 16.75,
            "estoque": 110,
            "lote": "LOT2024010",
            "data_validade": (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d"),
            "fabricante": "Alergia Solution",
            "descricao": "Anti-histamínico de segunda geração"
        }
    ]
    
    print("📊 Criando medicamentos...")
    for med in medicamentos:
        try:
            response = requests.post(f"{BASE_URL}/medicamentos", json=med)
            if response.status_code == 201:
                print(f"✅ {med['nome']} criado com sucesso")
            else:
                print(f"⚠️  {med['nome']} - Erro: {response.status_code}")
        except Exception as e:
            print(f"❌ Erro ao criar {med['nome']}: {e}")

def criar_clientes():
    """Cria clientes de exemplo"""
    clientes = [
        {
            "cpf": "11144477788",
            "nome": "João Silva Santos",
            "email": "joao.silva@email.com",
            "telefone": "11987654321",
            "endereco": "Rua das Flores, 123, São Paulo, SP"
        },
        {
            "cpf": "22255588899",
            "nome": "Maria Oliveira Costa",
            "email": "maria.oliveira@email.com",
            "telefone": "11912345678",
            "endereco": "Avenida Paulista, 456, São Paulo, SP"
        },
        {
            "cpf": "33366699900",
            "nome": "Carlos Mendes Pereira",
            "email": "carlos.mendes@email.com",
            "telefone": "11998765432",
            "endereco": "Rua Augusta, 789, São Paulo, SP"
        },
        {
            "cpf": "44477700011",
            "nome": "Ana Paula Ferreira",
            "email": "ana.paula@email.com",
            "telefone": "11987123456",
            "endereco": "Avenida Brasil, 321, Rio de Janeiro, RJ"
        },
        {
            "cpf": "55588811122",
            "nome": "Pedro Gonçalves Marques",
            "email": "pedro.goncalves@email.com",
            "telefone": "11965432109",
            "endereco": "Rua Quinze de Novembro, 654, Belo Horizonte, MG"
        }
    ]
    
    print("\n👥 Criando clientes...")
    for cliente in clientes:
        try:
            response = requests.post(f"{BASE_URL}/clientes", json=cliente)
            if response.status_code == 201:
                print(f"✅ {cliente['nome']} criado com sucesso")
            else:
                print(f"⚠️  {cliente['nome']} - Erro: {response.status_code}")
        except Exception as e:
            print(f"❌ Erro ao criar {cliente['nome']}: {e}")

def criar_fornecedores():
    """Cria fornecedores de exemplo"""
    fornecedores = [
        {
            "nome": "Indústria Farmacêutica Brasil S.A.",
            "cnpj": "12345678000100",
            "telefone": "1133334444",
            "email": "contato@farmbrasil.com.br",
            "endereco": "Rua Industrial, 100, São Paulo, SP"
        },
        {
            "nome": "Medicamentos Genéricos LTDA",
            "cnpj": "98765432000100",
            "telefone": "1144445555",
            "email": "vendas@medgenericos.com.br",
            "endereco": "Avenida Comercial, 200, São Paulo, SP"
        },
        {
            "nome": "Pharma Distribuição Nacional",
            "cnpj": "55443322000100",
            "telefone": "1155556666",
            "email": "distribuicao@pharma.com.br",
            "endereco": "Rua da Distribuição, 300, Campinas, SP"
        },
        {
            "nome": "Vitaminas e Suplementos LTDA",
            "cnpj": "11223344000100",
            "telefone": "1166667777",
            "email": "vitaminas@suplement.com.br",
            "endereco": "Avenida das Vitaminas, 400, Rio de Janeiro, RJ"
        },
        {
            "nome": "Antibióticos Especializados",
            "cnpj": "77788899000100",
            "telefone": "1177778888",
            "email": "antibioticos@especial.com.br",
            "endereco": "Rua da Especialidade, 500, Belo Horizonte, MG"
        }
    ]
    
    print("\n🏭 Criando fornecedores...")
    for fornecedor in fornecedores:
        try:
            response = requests.post(f"{BASE_URL}/fornecedores", json=fornecedor)
            if response.status_code == 201:
                print(f"✅ {fornecedor['nome']} criado com sucesso")
            else:
                print(f"⚠️  {fornecedor['nome']} - Erro: {response.status_code}")
        except Exception as e:
            print(f"❌ Erro ao criar {fornecedor['nome']}: {e}")

def criar_vendas():
    """Cria vendas de exemplo"""
    print("\n🛍️  Criando vendas...")
    
    # Primeiro, obter IDs dos clientes e medicamentos
    try:
        clientes = requests.get(f"{BASE_URL}/clientes").json()
        medicamentos = requests.get(f"{BASE_URL}/medicamentos").json()
        
        if not clientes or not medicamentos:
            print("❌ Erro: Não há clientes ou medicamentos cadastrados")
            return
        
        vendas = [
            {
                "id_cliente": clientes[0]["id"],
                "desconto": 0,
                "observacoes": "Compra normal",
                "itens": [
                    {
                        "id_medicamento": medicamentos[0]["id"],
                        "quantidade": 2,
                        "preco_unitario": medicamentos[0]["preco"]
                    },
                    {
                        "id_medicamento": medicamentos[1]["id"],
                        "quantidade": 1,
                        "preco_unitario": medicamentos[1]["preco"]
                    }
                ]
            },
            {
                "id_cliente": clientes[1]["id"],
                "desconto": 5.00,
                "observacoes": "Cliente VIP - 10% desconto",
                "itens": [
                    {
                        "id_medicamento": medicamentos[2]["id"],
                        "quantidade": 1,
                        "preco_unitario": medicamentos[2]["preco"]
                    }
                ]
            },
            {
                "id_cliente": clientes[2]["id"],
                "desconto": 0,
                "observacoes": "Entrega em casa",
                "itens": [
                    {
                        "id_medicamento": medicamentos[3]["id"],
                        "quantidade": 3,
                        "preco_unitario": medicamentos[3]["preco"]
                    },
                    {
                        "id_medicamento": medicamentos[4]["id"],
                        "quantidade": 2,
                        "preco_unitario": medicamentos[4]["preco"]
                    }
                ]
            }
        ]
        
        for i, venda in enumerate(vendas):
            try:
                response = requests.post(f"{BASE_URL}/vendas", json=venda)
                if response.status_code == 201:
                    print(f"✅ Venda #{i+1} criada com sucesso - Total: R$ {response.json()['total']:.2f}")
                else:
                    print(f"⚠️  Venda #{i+1} - Erro: {response.status_code}")
            except Exception as e:
                print(f"❌ Erro ao criar venda #{i+1}: {e}")
    
    except Exception as e:
        print(f"❌ Erro ao obter dados para criar vendas: {e}")

def main():
    """Executa o script de população"""
    print("="*60)
    print("🏥 POPULAÇÃO DO BANCO DE DADOS - FARMÁCIA")
    print("="*60)
    print(f"Conectando em: {BASE_URL}\n")
    
    try:
        # Testar conexão
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("API conectada com sucesso!\n")
        else:
            print("Erro ao conectar com a API")
            return
    except Exception as e:
        print(f"Erro ao conectar com a API: {e}")
        print("   Certifique-se de que a API está rodando em http://localhost:8000")
        return
    
    # Executar população
    criar_medicamentos()
    criar_clientes()
    criar_fornecedores()
    criar_vendas()
    
    print("\n" + "="*60)
    print("POPULAÇÃO DO BANCO CONCLUÍDA!")
    print("="*60)
    print("\nAgora você pode:")
    print("1. Iniciar a interface Qt5: python frontend/main.py")
    print("2. Acessar a documentação: http://localhost:8000/docs")
    print("3. Usar os dados de exemplo para testar as funcionalidades")

if __name__ == "__main__":
    main()
