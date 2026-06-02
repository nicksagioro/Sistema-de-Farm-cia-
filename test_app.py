import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from app import app
from models import Medicamento, Cliente, Fornecedor, Venda, ItemVenda

# Banco de dados de teste (SQLite em memória)
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# ==================== TESTES MEDICAMENTOS ====================

class TestMedicamentos:
    
    def test_criar_medicamento(self):
        """Testa criação de um medicamento"""
        response = client.post(
            "/api/medicamentos",
            json={
                "nome": "Dipirona 500mg",
                "principio_ativo": "Dipirona Monoidratada",
                "preco": 5.50,
                "estoque": 100,
                "lote": "LOT123",
                "data_validade": "2025-12-31"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["nome"] == "Dipirona 500mg"
        assert data["preco"] == 5.50
    
    def test_listar_medicamentos(self):
        """Testa listagem de medicamentos"""
        response = client.get("/api/medicamentos")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_obter_medicamento(self):
        """Testa obtenção de um medicamento específico"""
        # Criar primeiro
        create_response = client.post(
            "/api/medicamentos",
            json={
                "nome": "Aspirin",
                "principio_ativo": "Ácido Acetilsalicílico",
                "preco": 3.50,
                "estoque": 50,
                "lote": "LOT456",
                "data_validade": "2025-12-31"
            }
        )
        med_id = create_response.json()["id"]
        
        # Obter
        response = client.get(f"/api/medicamentos/{med_id}")
        assert response.status_code == 200
        assert response.json()["nome"] == "Aspirin"
    
    def test_atualizar_medicamento(self):
        """Testa atualização de medicamento"""
        # Criar
        create_response = client.post(
            "/api/medicamentos",
            json={
                "nome": "Vitamina C",
                "principio_ativo": "Ácido Ascórbico",
                "preco": 10.00,
                "estoque": 200,
                "lote": "LOT789",
                "data_validade": "2025-12-31"
            }
        )
        med_id = create_response.json()["id"]
        
        # Atualizar
        response = client.put(
            f"/api/medicamentos/{med_id}",
            json={"preco": 9.99, "estoque": 150}
        )
        assert response.status_code == 200
        assert response.json()["preco"] == 9.99
        assert response.json()["estoque"] == 150
    
    def test_deletar_medicamento(self):
        """Testa deleção de medicamento"""
        # Criar
        create_response = client.post(
            "/api/medicamentos",
            json={
                "nome": "Ibuprofen",
                "principio_ativo": "Ibuprofeno",
                "preco": 4.50,
                "estoque": 75,
                "lote": "LOT999",
                "data_validade": "2025-12-31"
            }
        )
        med_id = create_response.json()["id"]
        
        # Deletar
        response = client.delete(f"/api/medicamentos/{med_id}")
        assert response.status_code == 204
        
        # Verificar se foi deletado
        response = client.get(f"/api/medicamentos/{med_id}")
        assert response.status_code == 404
    
    def test_medicamento_nome_duplicado(self):
        """Testa validação de nome duplicado"""
        # Criar primeiro
        client.post(
            "/api/medicamentos",
            json={
                "nome": "Medicamento Único",
                "principio_ativo": "Princípio X",
                "preco": 5.00,
                "estoque": 100,
                "lote": "LOT111",
                "data_validade": "2025-12-31"
            }
        )
        
        # Tentar criar com mesmo nome
        response = client.post(
            "/api/medicamentos",
            json={
                "nome": "Medicamento Único",
                "principio_ativo": "Princípio Y",
                "preco": 6.00,
                "estoque": 50,
                "lote": "LOT222",
                "data_validade": "2025-12-31"
            }
        )
        assert response.status_code == 400

# ==================== TESTES CLIENTES ====================

class TestClientes:
    
    def test_criar_cliente(self):
        """Testa criação de cliente"""
        response = client.post(
            "/api/clientes",
            json={
                "cpf": "12345678901",
                "nome": "João Silva",
                "email": "joao@example.com",
                "telefone": "11987654321"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["cpf"] == "12345678901"
        assert data["nome"] == "João Silva"
    
    def test_cliente_cpf_duplicado(self):
        """Testa validação de CPF duplicado"""
        # Criar primeiro
        client.post(
            "/api/clientes",
            json={
                "cpf": "11111111111",
                "nome": "Cliente Um",
                "email": "cliente1@example.com"
            }
        )
        
        # Tentar criar com mesmo CPF
        response = client.post(
            "/api/clientes",
            json={
                "cpf": "11111111111",
                "nome": "Cliente Dois",
                "email": "cliente2@example.com"
            }
        )
        assert response.status_code == 400
    
    def test_listar_clientes(self):
        """Testa listagem de clientes"""
        response = client.get("/api/clientes")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

# ==================== TESTES FORNECEDORES ====================

class TestFornecedores:
    
    def test_criar_fornecedor(self):
        """Testa criação de fornecedor"""
        response = client.post(
            "/api/fornecedores",
            json={
                "nome": "Indústria Farmacêutica XYZ",
                "cnpj": "12345678000100",
                "telefone": "1133334444",
                "email": "contato@xyz.com"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["cnpj"] == "12345678000100"
    
    def test_fornecedor_cnpj_duplicado(self):
        """Testa validação de CNPJ duplicado"""
        # Criar primeiro
        client.post(
            "/api/fornecedores",
            json={
                "nome": "Fornecedor A",
                "cnpj": "99999999000100"
            }
        )
        
        # Tentar criar com mesmo CNPJ
        response = client.post(
            "/api/fornecedores",
            json={
                "nome": "Fornecedor B",
                "cnpj": "99999999000100"
            }
        )
        assert response.status_code == 400

# ==================== TESTES HEALTH CHECK ====================

class TestHealth:
    
    def test_health_check(self):
        """Testa endpoint de health check"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "OK"

# ==================== EXECUTAR TESTES ====================

if __name__ == "__main__":
    # Executar: pytest backend/test_app.py -v
    pytest.main([__file__, "-v"])
