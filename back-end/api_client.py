import requests
from typing import List, Optional, Dict
from datetime import date

class APIClient:
    """Cliente HTTP para comunicação com a API FastAPI"""
    
    def __init__(self, base_url: str = "http://localhost:8000/api"):
        self.base_url = base_url
        self.session = requests.Session()
    
    # ==================== MEDICAMENTOS ====================
    
    def listar_medicamentos(self, skip: int = 0, limit: int = 100) -> List[Dict]:
        """Lista todos os medicamentos"""
        try:
            response = self.session.get(f"{self.base_url}/medicamentos", params={"skip": skip, "limit": limit})
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao listar medicamentos: {e}")
            return []
    
    def obter_medicamento(self, med_id: int) -> Optional[Dict]:
        """Obtém um medicamento pelo ID"""
        try:
            response = self.session.get(f"{self.base_url}/medicamentos/{med_id}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao obter medicamento: {e}")
            return None
    
    def criar_medicamento(self, dados: Dict) -> Optional[Dict]:
        """Cria um novo medicamento"""
        try:
            response = self.session.post(f"{self.base_url}/medicamentos", json=dados)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao criar medicamento: {e}")
            return None
    
    def atualizar_medicamento(self, med_id: int, dados: Dict) -> Optional[Dict]:
        """Atualiza um medicamento"""
        try:
            response = self.session.put(f"{self.base_url}/medicamentos/{med_id}", json=dados)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao atualizar medicamento: {e}")
            return None
    
    def deletar_medicamento(self, med_id: int) -> bool:
        """Deleta um medicamento"""
        try:
            response = self.session.delete(f"{self.base_url}/medicamentos/{med_id}")
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Erro ao deletar medicamento: {e}")
            return False
    
    # ==================== CLIENTES ====================
    
    def listar_clientes(self, skip: int = 0, limit: int = 100) -> List[Dict]:
        """Lista todos os clientes"""
        try:
            response = self.session.get(f"{self.base_url}/clientes", params={"skip": skip, "limit": limit})
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao listar clientes: {e}")
            return []
    
    def obter_cliente(self, cliente_id: int) -> Optional[Dict]:
        """Obtém um cliente pelo ID"""
        try:
            response = self.session.get(f"{self.base_url}/clientes/{cliente_id}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao obter cliente: {e}")
            return None
    
    def criar_cliente(self, dados: Dict) -> Optional[Dict]:
        """Cria um novo cliente"""
        try:
            response = self.session.post(f"{self.base_url}/clientes", json=dados)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao criar cliente: {e}")
            return None
    
    def atualizar_cliente(self, cliente_id: int, dados: Dict) -> Optional[Dict]:
        """Atualiza um cliente"""
        try:
            response = self.session.put(f"{self.base_url}/clientes/{cliente_id}", json=dados)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao atualizar cliente: {e}")
            return None
    
    def deletar_cliente(self, cliente_id: int) -> bool:
        """Deleta um cliente"""
        try:
            response = self.session.delete(f"{self.base_url}/clientes/{cliente_id}")
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Erro ao deletar cliente: {e}")
            return False
    
    # ==================== FORNECEDORES ====================
    
    def listar_fornecedores(self, skip: int = 0, limit: int = 100) -> List[Dict]:
        """Lista todos os fornecedores"""
        try:
            response = self.session.get(f"{self.base_url}/fornecedores", params={"skip": skip, "limit": limit})
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao listar fornecedores: {e}")
            return []
    
    def obter_fornecedor(self, fornecedor_id: int) -> Optional[Dict]:
        """Obtém um fornecedor pelo ID"""
        try:
            response = self.session.get(f"{self.base_url}/fornecedores/{fornecedor_id}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao obter fornecedor: {e}")
            return None
    
    def criar_fornecedor(self, dados: Dict) -> Optional[Dict]:
        """Cria um novo fornecedor"""
        try:
            response = self.session.post(f"{self.base_url}/fornecedores", json=dados)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao criar fornecedor: {e}")
            return None
    
    def atualizar_fornecedor(self, fornecedor_id: int, dados: Dict) -> Optional[Dict]:
        """Atualiza um fornecedor"""
        try:
            response = self.session.put(f"{self.base_url}/fornecedores/{fornecedor_id}", json=dados)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao atualizar fornecedor: {e}")
            return None
    
    def deletar_fornecedor(self, fornecedor_id: int) -> bool:
        """Deleta um fornecedor"""
        try:
            response = self.session.delete(f"{self.base_url}/fornecedores/{fornecedor_id}")
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Erro ao deletar fornecedor: {e}")
            return False
    
    # ==================== VENDAS ====================
    
    def listar_vendas(self, skip: int = 0, limit: int = 100) -> List[Dict]:
        """Lista todas as vendas"""
        try:
            response = self.session.get(f"{self.base_url}/vendas", params={"skip": skip, "limit": limit})
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao listar vendas: {e}")
            return []
    
    def obter_venda(self, venda_id: int) -> Optional[Dict]:
        """Obtém uma venda pelo ID"""
        try:
            response = self.session.get(f"{self.base_url}/vendas/{venda_id}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao obter venda: {e}")
            return None
    
    def criar_venda(self, dados: Dict) -> Optional[Dict]:
        """Cria uma nova venda"""
        try:
            response = self.session.post(f"{self.base_url}/vendas", json=dados)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao criar venda: {e}")
            return None
    
    def atualizar_venda(self, venda_id: int, dados: Dict) -> Optional[Dict]:
        """Atualiza uma venda"""
        try:
            response = self.session.put(f"{self.base_url}/vendas/{venda_id}", json=dados)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao atualizar venda: {e}")
            return None
    
    def deletar_venda(self, venda_id: int) -> bool:
        """Deleta uma venda"""
        try:
            response = self.session.delete(f"{self.base_url}/vendas/{venda_id}")
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Erro ao deletar venda: {e}")
            return False
        
